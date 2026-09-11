# Tool reference

Generated from the current workflow definitions and historical Firestorm 7.2.4.80712 API discovery. Refresh the running viewer before relying on a dynamic operation. Counts are not test coverage.

42 workflow tools; 94 historical viewer operations.

## Workflow tools

| Tool | Description |
| --- | --- |
| `control_acquire` | Acquire exclusive bridge control for a multi-step workflow. Other clients can still read connection status/events. Renew before expiry and release in finally. |
| `control_release` | Release this client's exclusive control lease. |
| `native_file_dialogs` | List recognized Windows Open-file dialogs owned by this Firestorm installation. English common dialogs only; unsupported layouts require manual selection. |
| `native_file_choose` | Select an existing file in a freshly discovered Firestorm Open dialog. Verifies window ownership and filename readback. Import success must be checked in viewer state. Know which import/upload action opened the picker first. |
| `connection_status` | Check whether the local Firestorm LEAP helper is connected. Does not log in or change the viewer. |
| `capabilities_refresh` | Discover all APIs and operations exposed by this running viewer; refresh dynamic MCP tool discovery. |
| `viewer_api_inspect` | Read the live description and required arguments for an API or operation. Discover before calling unfamiliar operations. |
| `viewer_call` | Invoke any discovered viewer API operation. arguments can contain typed LLSD values: {$uuid: string}, {$uri: string}, {$binary_base64: string}. Read state after writes; timeouts must not be blindly retried. |
| `events_subscribe` | Subscribe to a named viewer event stream, such as StartupState or LLAutopilot. Events are bounded and remain local until read. |
| `events_unsubscribe` | Stop subscribing to a viewer event stream. |
| `events_read` | Read subscribed viewer events after a cursor. The dropped flag identifies buffer overflow; do not infer missing events. |
| `ui_find` | Find UI control paths inside an explicit subtree, for example /main_view/menu_stack/world_panel/Floater View/Local Mesh. floater_open supplies the panel's ui_path when resolvable. Narrow scope avoids enumerating an entire loaded inventory. |
| `ui_get_value` | Read the value of a specific discovered UI control. Use targeted paths to avoid unrelated chat or private fields. |
| `ui_click` | Click a visible, enabled discovered control by path. Returns input handling status, not proof of a simulator-side effect. |
| `ui_set_text` | Replace text in a discovered edit control using viewer input, then read back its value. Does not press Enter. |
| `ui_select` | Select a discovered combobox item by its actual value. |
| `ui_inspect` | Inspect a known UI path's geometry and enabled/visible state. Use floater_open and ui_find to discover panel controls. |
| `ui_press_key` | Press and release a viewer key, with optional CTL/ALT/SHIFT modifiers. A focused form may act on Enter. |
| `ui_list_menus` | List viewer menu entries from this installation's XUI, filter by name/label/function. These describe menus, not guaranteed enabled actions. |
| `ui_invoke_menu` | Invoke an actual menu entry from installed XUI by exact name; unknown callback names are never dispatched. This may open a native file picker. |
| `floater_list` | List registered viewer floaters and their XUI files. |
| `floater_open` | Open a registered viewer floater and check its visibility. |
| `avatar_position` | Read avatar position/orientation from the viewer. |
| `avatar_walk_to` | Start walking to GLOBAL coordinates. Poll avatar_movement_status and verify position; this is not pathfinding success. |
| `avatar_movement_status` | Read autopilot progress and current avatar position. |
| `avatar_stop` | Cancel automatic movement and read its resulting state. |
| `world_objects` | List nearby objects as reported by the viewer. Availability depends on simulator interest and viewer loading. |
| `inventory_search` | Search a specific inventory folder recursively, returning item metadata. Does not rez, purchase or upload anything. |
| `setting_get` | Read a named viewer setting; default group is Global. |
| `setting_set` | Change a viewer setting and return before/after readback. Some settings persist across restarts. |
| `camera_set` | Set a fixed camera and focus in REGION coordinates. Viewport capture is needed to verify composition. |
| `camera_release` | Release scripted camera control. This returns to viewer camera behavior, not an exact saved manual camera pose. |
| `snapshot` | Capture Firestorm's rendered image and return an MCP image plus saved PNG and hash. Render evidence alone does not prove upload or visibility to others. |
| `capture_orbit` | Capture repeatable orbit views around a REGION-coordinate focus and save a manifest. Releases scripted camera in finally. Caller must identify whether the subject is local preview or a server asset. |
| `asset_inspect` | Inspect a local COLLADA/glTF/GLB/texture export and record its SHA256. This checks file metadata, not upload eligibility, LOD quality, land impact or in-world appearance. |
| `image_compare` | Compare two same-size images and save an absolute-difference PNG. Metrics do not establish semantic or material correctness. |
| `local_mesh_open` | Open Firestorm's Local Mesh panel. Its local replacements are visible only in this viewer and do not prove server upload. |
| `local_mesh_auto_reload` | Set local mesh automatic reload so Blender exports can refresh in the viewer. Returns the previous settings for restoration. |
| `mesh_upload_open` | Open the standard mesh upload preview workflow. Does not submit an upload or authorize an upload fee. |
| `mesh_upload_status` | Read mesh-import preview LOD sources/files/counts, physics, dimensions, warnings, displayed weights and fee with control visibility. Does not calculate or submit an upload. Quote freshness and file-content bindings remain unverified. |
| `local_mesh_status` | Read Local Mesh's selected item/object and displayed import log. This is local preview evidence, not a simulator upload. |
| `capture_manifest_read` | Read a saved capture manifest created by this server. |

## Viewer operations

| API | Operations |
| --- | --- |
| `GroupChat` | `leaveGroupChat`, `sendGroupIM`, `startGroupChat` |
| `LLAgent` | `getAgentScreenPos`, `getAnimationInfo`, `getAutoPilot`, `getGroups`, `getID`, `getNearbyAvatarsList`, `getNearbyObjectsList`, `getPosition`, `lookAt`, `playAnimation`, `removeCameraParams`, `requestSit`, `requestStand`, `requestTeleport`, `requestTouch`, `resetAxes`, `setAutoPilotTarget`, `setCameraParams`, `setFollowCamActive`, `startAutoPilot`, `startFollowPilot`, `stopAnimation`, `stopAutoPilot` |
| `LLAppViewer` | `forceQuit`, `requestQuit` |
| `LLAppearance` | `detachItems`, `getOutfitItems`, `getOutfitsList`, `wearItems`, `wearOutfit` |
| `LLCommandDispatcher` | `dispatch`, `enumerate` |
| `LLFloaterAbout` | `getInfo` |
| `LLFloaterReg` | `clickButton`, `getBuildMap`, `hideInstance`, `instanceVisible`, `showInstance`, `toggleInstance` |
| `LLGesture` | `getActiveGestures`, `isGesturePlaying`, `startGesture`, `stopGesture` |
| `LLInventory` | `collectDescendantsIf`, `getAssetTypeNames`, `getBasicFolderID`, `getDirectDescendants`, `getFolderTypeNames`, `getItemsInfo` |
| `LLNotifications` | `cancel`, `forward`, `ignore`, `listChannelNotifications`, `listChannels`, `requestAdd`, `respond` |
| `LLPipeline` | `disableAllRenderFeatures`, `disableAllRenderInfoDisplays`, `disableAllRenderTypes`, `enableAllRenderFeatures`, `enableAllRenderInfoDisplays`, `enableAllRenderTypes`, `hasRenderFeature`, `hasRenderInfoDisplay`, `hasRenderType`, `toggleRenderFeatures`, `toggleRenderInfoDisplays`, `toggleRenderTypes` |
| `LLStartUp` | `getStateTable`, `postStartupState` |
| `LLTeleportHandler` | `teleport` |
| `LLURLDispatcher` | `dispatch`, `dispatchFromTextEditor`, `dispatchRightClick` |
| `LLViewerControl` | `get`, `groups`, `set`, `toggle`, `vars` |
| `LLViewerWindow` | `requestReshape`, `saveSnapshot` |
| `LLWindow` | `getInfo`, `getPaths`, `keyDown`, `keyUp`, `mouseDown`, `mouseMove`, `mouseScroll`, `mouseUp` |
| `UI` | `call`, `getValue` |

See [exact input schemas](tool-catalog.json) and [viewer descriptors](viewer-api-reference.json).
