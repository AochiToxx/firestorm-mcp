# Importer procedure for Firestorm MCP 0.3.0a1

Tool names below omit host-specific prefixes. Inspect current tool schemas before
calling them. Paths come from the running viewer; examples using
`/path/from/discovery` describe argument shape and are not executable UI targets.
Version differences or an unavailable operation require a reported limitation,
not an unbound keyboard fallback. These procedures inherit live viewer evidence;
the skill itself has not yet been benchmarked in a new end-to-end agent run.

## Establish and load a preview

Before any open/focus/load action, check `connection_status`. A foreign control
owner means handoff without viewer input. Otherwise acquire the workflow lease
and inspect the existing preview read-only, for example with `viewer_call`:

```json
{"api":"LLFloaterReg","operation":"instanceVisible","arguments":{"name":"upload_model"},"expect_reply":true}
```

This reports visibility, not existence or ownership. A false result alone does
not authorize a new open/load: use supported read-only panel-tree inspection and
`native_file_dialogs` to distinguish an absent preview from a retained hidden
preview or a pending importer picker. If presence or reuse authority cannot be
established from those observations and the task context, release and clarify.

If a preview exists, use read-only scoped discovery/inspection to identify its
contents. Do not use `floater_open` for this check: it focuses the panel. Establish
authority to reuse the preview from the task/session context. If that authority
is unknown, release the lease and clarify before any open/focus/replace/cancel.
Record whether the workflow creates a new preview or reuses an authorized one.
Record initial preview LOD/overlay state and the user's desired final state.
Comparison-only work should retain matching loaded files and skip unrelated
imports, physics Analyze and quote calculation.

For a new requested model preview, call `mesh_upload_open {}`. Discover a fresh
Firestorm-owned picker using `native_file_dialogs {}`, then select the exact file
with `native_file_choose {"dialog_id":123,"filename":"C:/exports/example-high.dae"}`
where the ID and path are replaced with the actual discovered ID and supplied
absolute path. Other upload pickers may advance a transaction when a file is
selected; do not substitute a texture/sound/animation picker. After selection,
read settled importer state rather than treating filename entry as a completed
import. An initially empty picker list may mean the picker is still opening.

For an owned/authorized preview, use an already-discovered path, or the path from
`floater_open` with registered name `upload_model` when focusing it is appropriate.
Search inside that panel, not the entire viewer:

```json
{"query":"lod_source_*","under":"/path/from/discovery","search_in":"name","match":"glob","limit":20,"offset":0}
```

`match:"exact"` still matches the full path unless `search_in:"name"` is supplied.
Follow `next_offset` until null when complete coverage is required. `max_depth`
counts depth relative to `under`. With `include_info:true`, a returned `%`-named
child may have `available:false`; preserve the other results and treat only that
item as unknown. An unavailable child is not evidence that the whole panel failed.

For each provided lower LOD, use its discovered source combo and Browse button.
On the tested viewer, targeted `Home` selects `Load from file`; targeted `Return`
on the same combo commits it. Confirm the label first and the dependent Browse
button's visible/enabled state after commit. If the expected option is not
observed, stop that selection sequence; do not send Return blindly. Example shape:

```json
{"keysym":"Return","path":"/discovered/source-combo","observe_path":"/discovered/browse-button"}
```

Invoke that verified Browse button using the registered-button recipe below,
discover its fresh native picker, select the
corresponding file, and check the settled source/path/count readback. Do not repeat
an import whose completion is merely pending. Use a bounded deadline appropriate
to the task, report pending state, and preserve an unresolved operation on timeout.

## Tabs, physics and checkboxes

For unique importer buttons (tabs, Browse, Analyze, Calculate and Cancel), use
`ui_click` with the discovered button `path`,
`floater:"upload_model"`, and `observe_path` pointing to the expected content
panel or relevant dependent control when it provides useful readback. Accept a
tab switch only when its content becomes visible; for Browse discover the fresh
picker, and for Analyze/Calculate observe the resulting settled state. The
registered callback requires a unique button path; repeated child names must not
bypass the ambiguity guard.

For supplied physics geometry, switch to the Physics tab, inspect the current
source choices, select/commit the requested file mode, and use its verified native
picker. Read physics counts and inspect the overlay. Run Analyze only when the
requested check calls for it, using the user's intended settings; record the
actual options and resulting hull/vertex counts. Do not impose product-specific
physics defaults or cost thresholds. Importer hulls are not simulator collision
verification.

The tested `show_physics/CheckboxCtrl Button` mouse path reported handled input
without changing the checkbox. Read the parent value first. If a toggle is needed,
one `ui_press_key` with `keysym:"Space"`, the visible/enabled child button `path`,
and `observe_path` set to the parent checkbox changed its boolean and overlay.
Verify the parent value and a fresh image. Return is not this checkbox's commit
key. Do not toggle an already-correct value, blindly retry, or use an ambiguous
floater-wide callback.

## LOD and image comparison

Importing a source LOD can change `preview_lod_combo`. After the final file import,
explicitly select and commit the desired preview LOD before naming an image.
On the tested combo, path-targeted Home/Return selected High and End/Return
selected Lowest. Verify the selected value after each sequence. Other LOD choices
need their actual supported selection procedure; do not guess key counts.

The uploader has a separate camera from the world camera. If the subject is too
small, start with `mesh_preview_camera {"mode":"zoom","vertical":0.2}` and inspect
a fresh capture before further movement. Zoom and orbit have live evidence; pan
has synthetic coverage only. These are bounded relative drags, not exact measured
poses. There is no exact prior-pose restoration guarantee.

Use `snapshot` with `label`, not `name`. Example:

```json
{"label":"preview-high","width":1600,"height":1000,"show_ui":true}
```

For a comparison, establish one usable composition, then capture High, Lowest and
High again with actual selected-value readback. The repeated High is a comparison
baseline, not necessarily the user's initial LOD. If keeping a reused preview,
restore its recorded initial LOD/temporary overlay changes unless the user asked
for a different final state. A request to remove the physics overlay should retain
false; do not undo that requested outcome during cleanup. Inspect returned PNGs;
matching labels alone prove nothing. Review `quality.blank_detected` and reject
blank or wrong-subject evidence. Nonblank does not establish freshness, correct
LOD, or asset quality. Identical pixels may be legitimate in a static scene;
do not automatically classify them as a stale capture. Keep capture hashes and
requested/actual dimensions. `image_compare` provides pixel differences, not a
semantic model-quality verdict. Keep captures and surrounding personal UI private.
Whole-frame differences can include unrelated UI/world changes. Attribute a
change to LOD geometry only after inspecting the subject; a numeric difference
alone cannot establish its cause.

## Quotes and efficient readback

`mesh_upload_status {}` provides full source/count/physics/fee checkpoints. It
reads controls sequentially and is not an atomic snapshot. For intermediate
checks, prefer `ui_inspect`, `ui_get_value`, or the existing input tool's
`observe_path` result for the relevant control. Do not cache changing values as
truth; revalidate reused paths after reopening a panel or reconnecting the viewer.

Calculate (`calculate_btn`) and Upload (`ok_btn`) are different actions. Request a
quote only when it belongs to the user's task. Click the verified Calculate
control once with the registered-button recipe and observe pending versus settled
state within a deadline. Scale
changes and even preview LOD commits were observed to invalidate fees. Re-read
quote state after those operations rather than carrying an earlier number forward.

Report numeric fees as `displayed_only`, with `freshness_verified:false` and file
content binding unverified. Preserve unknown fields as unknown; hidden warning
text can be stale. Displayed filenames and locally inspected hashes do not prove
which bytes a simulator would receive. No quote or preview establishes an upload.

## Cleanup and useful feedback

Restore temporary settings only where the earlier value and supported restoration
are known, preserving the user's intended outcome. Close a preview created for
the check unless asked to keep it; leave an authorized reused preview open unless
closing it was agreed. When closing, discover its `cancel_btn` by
basename, verify it, invoke the registered callback and check
`LLFloaterReg.instanceVisible` for `upload_model` is false. Check native pickers,
release this client's lease and finish the persistent client normally. If an
operation/dialog remains unresolved, report it instead of discarding its owner.

A useful contribution identifies the tool and scrubbed arguments, expected and
observed state, viewer/MCP versions, the smallest synthetic reproduction and
whether evidence is source metadata, UI, a rendered preview or simulator state.
Report awkward successful workarounds too; they identify future semantic tools.
