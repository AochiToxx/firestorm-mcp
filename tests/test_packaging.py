import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from firestorm_mcp import launcher
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


@pytest.mark.skipif(launcher.os.name != 'nt', reason='Windows launcher')
def test_busy_viewer_is_never_restarted(tmp_path, monkeypatch):
    viewer = tmp_path / 'Firestorm.exe'
    viewer.touch()
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [{'pid': 1, 'name': 'Firestorm.exe'}])
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **k: pytest.fail('Must not launch'))
    with pytest.raises(RuntimeError, match='already running'):
        launcher.launch(viewer, tmp_path / 'state')
    assert not (tmp_path / 'state').exists()


@pytest.mark.skipif(launcher.os.name != 'nt', reason='Windows launcher')
def test_dry_run_does_not_write_or_launch(tmp_path, monkeypatch):
    viewer = tmp_path / 'Firestorm.exe'
    viewer.touch()
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [])
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **k: pytest.fail('Must not launch'))
    result = launcher.launch(viewer, tmp_path / 'state', login_screen=True, dry_run=True)
    assert result['viewer_started'] is False
    assert result['arguments'][-3:] == ['--set', 'AutoLogin', 'false']
    assert Path(result['helper']).is_file()
    assert not (tmp_path / 'state').exists()


@pytest.mark.skipif(launcher.os.name != 'nt', reason='Windows launcher')
def test_existing_launch_lock_is_preserved(tmp_path, monkeypatch):
    viewer = tmp_path / 'Firestorm.exe'
    viewer.touch()
    runtime = tmp_path / 'state/runtime'
    runtime.mkdir(parents=True)
    (runtime / 'launch.lock').write_text('another launcher')
    monkeypatch.setattr(launcher, 'running_viewers', lambda: [])
    monkeypatch.setattr(launcher.subprocess, 'Popen', lambda *a, **k: pytest.fail('Must not launch'))
    with pytest.raises(FileExistsError):
        launcher.launch(viewer, tmp_path / 'state')
    assert (runtime / 'launch.lock').read_text() == 'another launcher'
