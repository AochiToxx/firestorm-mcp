import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from firestorm_mcp import launcher, paths
from firestorm_mcp.paths import data_root


def test_data_override_is_independent_of_code(monkeypatch, tmp_path):
    target = tmp_path / 'machine state'
    monkeypatch.setenv('FIRESTORM_MCP_HOME', str(target))
    assert data_root() == target.resolve()
    assert not target.exists()  # Resolving configuration has no write side effect.


def test_settings_escape_special_paths_and_preserve_single_leap_command():
    xml = launcher.session_settings(Path('C:/Python & Tools/python.exe'),
        Path('C:/Package/leap_entry.py'), Path('C:/State/run time'), Path('C:/Firestorm'))
    root = ET.fromstring(xml)
    commands = root.findall('./map/map/array/string')
    assert len(commands) == 1
    assert commands[0].text == ('"C:/Python & Tools/python.exe" "C:/Package/leap_entry.py" '
        '--runtime "C:/State/run time" --viewer-dir "C:/Firestorm"')


def synthetic_viewer(tmp_path, system):
    import plistlib
    if system == 'darwin':
        viewer = tmp_path / 'Firestorm Test.app'
        executable = viewer / 'Contents/MacOS/Firestorm'
        resources = viewer / 'Contents/Resources'
        executable.parent.mkdir(parents=True)
        (viewer / 'Contents/Info.plist').write_bytes(plistlib.dumps({'CFBundleExecutable': 'Firestorm'}))
    else:
        viewer = tmp_path / ('Firestorm.exe' if system == 'win32' else 'firestorm')
        executable, resources = viewer, tmp_path
    executable.touch()
    executable.chmod(0o755)
    menu = resources / 'skins/default/xui/en/menu_viewer.xml'
    menu.parent.mkdir(parents=True)
    menu.write_text('<menu/>')
    return viewer


@pytest.mark.parametrize('system', ['win32', 'darwin', 'linux'])
def test_busy_viewer_is_never_restarted(tmp_path, monkeypatch, system):
    viewer = synthetic_viewer(tmp_path, system)
    monkeypatch.setattr(paths, 'host_platform', lambda: system)
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [{'pid': 1, 'name': 'Firestorm.exe'}])
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **k: pytest.fail('Must not launch'))
    with pytest.raises(RuntimeError, match='already running'):
        launcher.launch(viewer, tmp_path / 'state')
    assert not (tmp_path / 'state').exists()


@pytest.mark.parametrize('system', ['win32', 'darwin', 'linux'])
def test_dry_run_does_not_write_or_launch(tmp_path, monkeypatch, system):
    viewer = synthetic_viewer(tmp_path, system)
    monkeypatch.setattr(paths, 'host_platform', lambda: system)
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [])
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **k: pytest.fail('Must not launch'))
    result = launcher.launch(viewer, tmp_path / 'state', login_screen=True, dry_run=True)
    assert result['viewer_started'] is False
    assert result['arguments'][-3:] == ['--set', 'AutoLogin', 'false']
    assert Path(result['helper']).is_file()
    assert Path(result['viewer_resources'], 'skins/default/xui/en/menu_viewer.xml').is_file()
    if system == 'darwin':
        assert 'Contents/MacOS/Firestorm' in result['arguments'][0].replace('\\', '/')
    elif system == 'linux':
        assert Path(result['arguments'][0]).name == 'firestorm'
    assert not (tmp_path / 'state').exists()


@pytest.mark.parametrize('system', ['win32', 'darwin', 'linux'])
def test_existing_launch_lock_is_preserved(tmp_path, monkeypatch, system):
    viewer = synthetic_viewer(tmp_path, system)
    monkeypatch.setattr(paths, 'host_platform', lambda: system)
    runtime = tmp_path / 'state/runtime'
    runtime.mkdir(parents=True)
    (runtime / 'launch.lock').write_text('another launcher')
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [])
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **k: pytest.fail('Must not launch'))
    with pytest.raises(FileExistsError):
        launcher.launch(viewer, tmp_path / 'state')
    assert (runtime / 'launch.lock').read_text() == 'another launcher'


@pytest.mark.parametrize('system', ['win32', 'darwin', 'linux'])
def test_launch_preserves_resource_layout_and_cleans_own_lock(tmp_path, monkeypatch, system):
    from types import SimpleNamespace
    viewer = synthetic_viewer(tmp_path, system)
    monkeypatch.setattr(paths, 'host_platform', lambda: system)
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [])
    calls = []
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *args, **kwargs:
                        calls.append((args, kwargs)) or SimpleNamespace(pid=123))
    report = launcher.launch(viewer, tmp_path / 'state')
    installed = paths.find_viewer(viewer)
    assert report['bridge_connection_verified'] is False
    assert calls[0][1] == {'cwd': installed.cwd}
    xml = (tmp_path / 'state/runtime/session-settings.xml').read_text()
    command = ET.fromstring(xml).find('./map/map/array/string').text
    assert str(installed.resources).replace('\\', '/') in command
    assert not (tmp_path / 'state/runtime/launch.lock').exists()


def test_ambiguous_discovery_requires_an_explicit_choice(tmp_path, monkeypatch):
    a, b = tmp_path / 'a', tmp_path / 'b'
    a.mkdir(); b.mkdir()
    first, second = synthetic_viewer(a, 'linux'), synthetic_viewer(b, 'linux')
    monkeypatch.setattr(paths, 'host_platform', lambda: 'linux')
    monkeypatch.delenv('FIRESTORM_VIEWER', raising=False)
    monkeypatch.delenv('FIRESTORM_VIEWER_DIR', raising=False)
    monkeypatch.setattr(paths, 'viewer_candidates', lambda: [first, second])
    with pytest.raises(ValueError, match='Multiple'):
        paths.find_viewer()
    assert paths.find_viewer(first).target == first.resolve()


def test_linux_internal_binary_and_broken_mac_bundle_are_rejected(tmp_path):
    import plistlib
    binary = tmp_path / 'do-not-directly-run-firestorm-bin'
    binary.touch()
    with pytest.raises(ValueError, match='launcher script'):
        paths.resolve_viewer(binary, 'linux')
    bundle = synthetic_viewer(tmp_path, 'darwin')
    (bundle / 'Contents/Info.plist').write_bytes(plistlib.dumps({'CFBundleExecutable': '../../outside'}))
    with pytest.raises(ValueError, match='CFBundleExecutable'):
        paths.resolve_viewer(bundle, 'darwin')


def test_platform_state_defaults_do_not_create_directories(tmp_path, monkeypatch):
    monkeypatch.delenv('FIRESTORM_MCP_HOME', raising=False)
    monkeypatch.setattr(Path, 'home', classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(paths, 'host_platform', lambda: 'darwin')
    assert paths.data_root() == tmp_path / 'Library/Application Support/FirestormMCP'
    monkeypatch.setattr(paths, 'host_platform', lambda: 'linux')
    monkeypatch.setenv('XDG_STATE_HOME', str(tmp_path / 'state'))
    assert paths.data_root() == tmp_path / 'state/firestorm-mcp'
    monkeypatch.setenv('XDG_STATE_HOME', 'relative-is-invalid')
    assert paths.data_root() == tmp_path / '.local/state/firestorm-mcp'
    assert not list(tmp_path.iterdir())


def test_generated_config_keeps_venv_python_and_matching_resources(tmp_path, monkeypatch):
    from firestorm_mcp import configure
    viewer = synthetic_viewer(tmp_path, 'darwin')
    monkeypatch.setattr(paths, 'host_platform', lambda: 'darwin')
    interpreter = tmp_path / 'env/bin/python'
    monkeypatch.setattr(configure.sys, 'executable', str(interpreter))
    entry = configure.configuration(tmp_path / 'state', viewer)['mcpServers']['firestorm']
    assert entry['command'] == str(interpreter.absolute())
    assert entry['args'][-1] == str(viewer.resolve() / 'Contents/Resources')
    assert entry['args'][entry['args'].index('--data-dir') + 1] == str((tmp_path / 'state').resolve())
    assert not (tmp_path / 'state').exists()


def test_doctor_is_offline_and_contains_no_local_paths(tmp_path, monkeypatch):
    from firestorm_mcp import doctor
    import json
    monkeypatch.setattr(doctor, 'find_viewer', lambda *_: (_ for _ in ()).throw(FileNotFoundError(str(tmp_path))))
    report = doctor.diagnose(root=tmp_path / 'state')
    assert report['viewer_contacted'] is False and report['setup_ready'] is False
    assert str(tmp_path) not in json.dumps(report)
    assert not (tmp_path / 'state').exists()


def test_unsupported_native_selection_fails_before_acquiring_a_lease(tmp_path, monkeypatch):
    from firestorm_mcp.server import Tools
    import firestorm_mcp.server as server
    tools = Tools(tmp_path)
    monkeypatch.setattr(server, 'platform_support', lambda: {'native_file_dialogs': False})
    monkeypatch.setattr(tools.client, 'rpc', lambda *a, **k: pytest.fail('No bridge contact on unsupported OS'))
    with pytest.raises(RuntimeError, match='manually'):
        tools.call('native_file_choose', {'dialog_id': 1, 'filename': 'example.dae'})
