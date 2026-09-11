"""Consumer regressions with synthetic UI replies; never contact a viewer."""
import pytest
from PIL import Image

from firestorm_mcp.assets import capture_quality
from firestorm_mcp.server import Tools


def test_search_names_depth_and_complete_pages(tmp_path):
    tools = Tools(tmp_path)
    base = "/panel/Physics"
    paths = [base, base + "/Physics tab"] + [base + f"/hidden/child{i:03}" for i in range(240)]
    tools.client.call = lambda *a, **k: {"paths": paths[::-1]}
    names = tools.call("ui_find", {"query": "physics", "under": base, "search_in": "name", "max_depth": 1})
    assert names["paths"] == [base, base + "/Physics tab"]
    first = tools.call("ui_find", {"query": "", "under": base, "limit": 200})
    assert first["truncated"] and first["next_offset"] == 200 and first["total_matches"] == 242
    last = tools.call("ui_find", {"query": "", "under": base, "offset": first["next_offset"]})
    assert not last["truncated"] and last["next_offset"] is None
    assert first["paths"] + last["paths"] == sorted(paths)
    exact = tools.call("ui_find", {"query": "PHYSICS TAB", "under": base, "match": "exact", "search_in": "name"})
    assert exact["paths"] == [base + "/Physics tab"]
    glob = tools.call("ui_find", {"query": "child00?", "under": base, "match": "glob", "search_in": "name"})
    assert len(glob["paths"]) == 10


def test_keys_require_target_and_hidden_target_never_receives_input(tmp_path):
    tools = Tools(tmp_path)
    calls = []
    def reply(api, op, args, **kw):
        calls.append(op)
        return {"visible_chain": False, "enabled_chain": True}
    tools.client.call = reply
    with pytest.raises(Exception, match="path.*required"):
        tools.call("ui_press_key", {"keysym": "Enter"})
    assert not calls
    with pytest.raises(ValueError, match="hidden"):
        tools.call("ui_press_key", {"keysym": "Enter", "path": "/hidden"})
    assert calls == ["getInfo"]


def test_keys_target_both_events_and_return_selection_readback(tmp_path):
    tools = Tools(tmp_path)
    selected = "High"
    sent = []
    def reply(api, op, args, **kw):
        nonlocal selected
        assert args["path"] == "/panel/lod"
        if op.startswith("key"):
            assert kw["expect_reply"] is True
            sent.append(op)
            selected = "Lowest"
        if op == "getValue":
            return {"value": selected}
        return {"visible_chain": True, "enabled_chain": True}
    tools.client.call = reply
    result = tools.call("ui_press_key", {"keysym": "End", "path": "/panel/lod"})
    assert sent == ["keyDown", "keyUp"]
    assert result["before"]["value"] == "High" and result["after"]["value"] == "Lowest"
    assert result["verified_effect"] is False


def test_registry_click_checks_unique_path_and_observes_effect(tmp_path):
    viewer = tmp_path / "viewer"
    xui = viewer / "skins/default/xui/en"
    xui.mkdir(parents=True)
    (xui / "preview.xml").write_text('<floater name="Preview"/>')
    tools = Tools(tmp_path, viewer)
    base = "/main_view/menu_stack/world_panel/Floater View/Preview"
    button, panel = base + "/Physics tab", base + "/physics"
    visible, duplicate = False, False
    clicks = []
    def reply(api, op, args=None, **kw):
        nonlocal visible
        if op == "getBuildMap":
            return {"preview": "preview.xml"}
        if op == "getPaths":
            return {"paths": [button, panel] + ([base + "/duplicate/Physics tab"] if duplicate else [])}
        if op == "clickButton":
            clicks.append(args)
            visible = True
            return {}
        if op == "getValue":
            return {}
        return {"visible_chain": visible if args["path"] == panel else True, "enabled_chain": True}
    tools.client.call = reply
    result = tools.call("ui_click", {"path": button, "floater": "preview", "observe_path": panel})
    assert result["method"] == "registry_callback"
    assert result["before"]["info"]["visible_chain"] is False
    assert result["after"]["info"]["visible_chain"] is True
    assert clicks == [{"name": "preview", "button": "Physics tab"}]
    duplicate = True
    with pytest.raises(ValueError, match="uniquely"):
        tools.call("ui_click", {"path": button, "floater": "preview"})
    assert len(clicks) == 1


@pytest.mark.parametrize("color", [(0, 0, 0), (1, 1, 2), (255, 255, 255), (100, 80, 60)])
def test_uniform_captures_are_flagged(color):
    result = capture_quality(Image.new("RGB", (32, 32), color))
    assert result["blank_detected"] and not result["visual_content_verified"]


def test_nonblank_capture_still_requires_visual_review(tmp_path):
    tools = Tools(tmp_path)
    def reply(api, op, args, **kw):
        frame = Image.new("RGB", (32, 32), "black")
        frame.paste("red", (8, 8, 24, 24))
        frame.save(args["filename"])
        return {"ok": True}
    tools.client.call = reply
    result = tools.call("snapshot", {})
    assert result["quality"]["status"] == "nonblank"
    assert result["quality"]["visual_content_verified"] is False
    assert result["requested_size"] == [1280, 720] and result["width"] == 32
