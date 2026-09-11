"""Narrow Windows common-file-dialog adapter for viewer-owned Open dialogs.

No global keyboard input, clipboard, shell commands or arbitrary-window control.
Unrecognized file dialogs fail closed and require manual selection.
"""
from __future__ import annotations

import os
from pathlib import Path


def _windows():
    if os.name != "nt":
        raise RuntimeError("Native file dialogs currently require Windows")
    import win32api, win32con, win32gui, win32process
    return win32api, win32con, win32gui, win32process


def _text(hwnd):
    # GetWindowText intentionally does not retrieve another process's edit text.
    # WM_GETTEXT is the documented cross-process path for standard controls.
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    send = user32.SendMessageTimeoutW
    send.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM,
                     wintypes.UINT, wintypes.UINT, ctypes.POINTER(ctypes.c_size_t)]
    send.restype = wintypes.LPARAM
    buffer = ctypes.create_unicode_buffer(32768)
    result = ctypes.c_size_t()
    if not send(hwnd, 0x000D, len(buffer), ctypes.addressof(buffer), 2, 2000, ctypes.byref(result)):
        raise RuntimeError("File dialog text read timed out or failed")
    return buffer.value


def dialogs(viewer_dir: Path):
    api, con, gui, process = _windows()
    result = []
    def inspect(hwnd, _):
        if not gui.IsWindowVisible(hwnd) or gui.GetClassName(hwnd) != "#32770":
            return
        _, pid = process.GetWindowThreadProcessId(hwnd)
        try:
            handle = api.OpenProcess(con.PROCESS_QUERY_INFORMATION | con.PROCESS_VM_READ, False, pid)
            try:
                executable = Path(process.GetModuleFileNameEx(handle, 0))
            finally:
                handle.Close()
        except Exception:
            return
        if executable.parent.resolve() != viewer_dir.resolve() or "firestorm" not in executable.name.lower():
            return
        edits = []
        def child(control, _):
            if gui.GetClassName(control) != "Edit" or not gui.IsWindowVisible(control) or not gui.IsWindowEnabled(control):
                return
            parent = gui.GetParent(control)
            ids = {gui.GetDlgCtrlID(control), gui.GetDlgCtrlID(parent)}
            # edt1/cmb13 are the standard filename entry IDs. Never target Search.
            if ids & {0x480, 0x47C}:
                edits.append(control)
        gui.EnumChildWindows(hwnd, child, None)
        ok = gui.GetDlgItem(hwnd, con.IDOK)
        label = gui.GetWindowText(ok).replace("&", "").lower() if ok else ""
        if len(edits) == 1 and label in ("open", "load", "import"):
            result.append({"dialog_id": hwnd, "pid": pid, "title": gui.GetWindowText(hwnd),
                           "filename_control": edits[0], "filename": _text(edits[0])})
    gui.EnumWindows(inspect, None)
    return result


def choose_file(viewer_dir: Path, dialog_id: int, filename: str):
    path = Path(filename).resolve(strict=True)
    if not path.is_file():
        raise ValueError("Expected an existing file")
    matches = [d for d in dialogs(viewer_dir) if d["dialog_id"] == dialog_id]
    if len(matches) != 1:
        raise ValueError("Expected a currently recognized Firestorm Open dialog; inspect native_file_dialogs first")
    _, con, gui, _ = _windows()
    edit = matches[0]["filename_control"]
    gui.SendMessageTimeout(edit, con.WM_SETTEXT, 0, str(path), con.SMTO_ABORTIFHUNG, 2000)
    if _text(edit) != str(path):
        raise RuntimeError("Filename readback did not match; Open was not invoked")
    gui.SendMessageTimeout(dialog_id, con.WM_COMMAND, con.IDOK, gui.GetDlgItem(dialog_id, con.IDOK), con.SMTO_ABORTIFHUNG, 2000)
    return {"status": "file_selection_submitted", "path": str(path), "import_verified": False,
            "note": "Inspect viewer state for import completion. Opening a texture/animation/sound upload dialog may start its normal upload workflow; choose the originating action deliberately."}
