from types import SimpleNamespace

import pytest

from firestorm_mcp import native


def test_wrong_dialog_never_receives_input(tmp_path, monkeypatch):
    mesh = tmp_path / "model.dae"
    mesh.write_text("test")
    monkeypatch.setattr(native, "dialogs", lambda _: [])
    with pytest.raises(ValueError, match="currently recognized"):
        native.choose_file(tmp_path, 42, str(mesh))


def test_filename_mismatch_does_not_submit(tmp_path, monkeypatch):
    mesh = tmp_path / "model.dae"
    mesh.write_text("test")
    monkeypatch.setattr(native, "dialogs", lambda _: [{"dialog_id": 42, "filename_control": 43}])
    calls = []
    constants = SimpleNamespace(WM_SETTEXT=12, WM_COMMAND=273, IDOK=1, SMTO_ABORTIFHUNG=2)
    gui = SimpleNamespace(SendMessageTimeout=lambda *args: calls.append(args), GetDlgItem=lambda *args: 44)
    monkeypatch.setattr(native, "_windows", lambda: (None, constants, gui, None))
    monkeypatch.setattr(native, "_text", lambda _: "wrong filename")
    with pytest.raises(RuntimeError, match="Open was not invoked"):
        native.choose_file(tmp_path, 42, str(mesh))
    assert [call[1] for call in calls] == [constants.WM_SETTEXT]
