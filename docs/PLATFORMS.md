# Platform requirements and evidence

Firestorm MCP is installed on the machine where the viewer runs. The Python
package, operating-system controls and graphical viewer are three separate
compatibility checks. A skill is portable text, not a replacement for any of them.

## Current matrix

| Target | Automated checks | Live desktop boundary |
| --- | --- | --- |
| Windows x64, Python 3.11–3.14 | Unit/protocol tests; source install, wheel and Inspector on 3.12 | Live Firestorm 7.2.4.80712 evidence inherited from MCP 0.3.0a1. New launch-layout tests are synthetic. Native adapter handles recognized English common dialogs |
| Linux x64, Python 3.12 | Ubuntu 24.04 package/protocol, source install, wheel and Inspector CI | Experimental LEAP launch through the original `firestorm` distribution wrapper; live viewer and desktop integration unverified; manual picker |
| macOS Intel and ARM64, Python 3.12 | macOS 15 package/protocol, source install, wheel and Inspector CI | Experimental `.app` launch, executable derived from Info.plist and XUI from Contents/Resources. Live viewer/Gatekeeper behavior unverified; manual picker |
| Linux ARM64, Python 3.12 / Raspberry Pi | Ubuntu ARM64 package/protocol, source install, wheel and Inspector CI | Actual Pi/Raspberry Pi OS untested; no verified compatible Firestorm ARM Linux build or graphical workflow. ARM64 CI is not Pi hardware certification |
| Other architectures, headless or remote hosts | Not in the current matrix; offline tools may work if dependencies install | No remote MCP endpoint, headless viewer service or native desktop adapter is supplied |

The [CI workflow](../.github/workflows/ci.yml) defines the matrix; check the release's
linked run for passing results. All jobs use synthetic fixtures and a disconnected
viewer. A package installation or dry-run launch plan is not a connected LEAP
session and does not prove UI input or rendering works.

## Viewer dependencies belong to the viewer

Install Firestorm from its official distribution for your OS/CPU. Do not bundle
it or assume that installing this MCP installs it. Firestorm's Linux build guide
targets x86_64; its distribution manifest installs a `firestorm` wrapper and
explicitly marks its internal binary as not for direct execution. We preserve
that wrapper so its own library and plugin setup can run. On macOS the manifest
uses the application's Contents/Resources directory, separate from its executable.
These layouts informed the launcher; they do not establish a live test result.
[Official Linux build guide](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/doc/building_linux.md),
[official viewer distribution manifest](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/indra/newview/viewer_manifest.py).

For a Raspberry Pi, use a Python 3.11+ environment matching the installed OS.
64-bit Linux ARM64 is the tested package architecture; 32-bit ARM is outside the
matrix. Dependencies such as Pillow, psutil and their dependencies may require
native build prerequisites where compatible wheels are unavailable. Do not run
the old Windows dependency snapshot as a Pi installer. Source setup uses the
package metadata and only selects `pywin32` on Windows.

Installing the MCP on a headless Pi does not connect it to a Firestorm session on
another PC. Remote agent orchestration would require a separate supported remote
MCP transport and session/security design. The private helper's loopback `/rpc`
address is not that service and must not be exposed.

## Platform-aware agent behavior

Use `connection_status.local_platform` before desktop work. Native picker tools
stay in the stable catalog, but `native_file_dialogs:false` means an agent must
arrange manual file selection and verify the resulting importer state. Do not
send Windows control identifiers or blindly retry those tools on other systems.
Capabilities discovered through LEAP still depend on the running viewer version.

An installed viewer and an available display variable do not prove a usable
graphical desktop, a compatible GPU, a functioning file picker or granted OS
permissions. Setup diagnostics are offline prechecks. The probe checks an actual
bridge connection; visual readback is still required for claims about effects.

## Contributor acceptance checklist

1. Record OS/version, CPU architecture, Python, MCP version, viewer build and host application. Use a fresh extracted package, install it without admin/root access, then save a reviewed `firestorm-mcp-doctor` report.
2. Test generated stdio configuration in the chosen host with no viewer. Confirm discovery, a synthetic asset metadata call, structured/image results and useful disconnected errors.
3. With the desktop owner's authority, run a dry-run launch plan, then normally launch and check LEAP. Never replace a running viewer or remove another process's lock.
4. Acquire a bounded lease for an original synthetic preview, verify loaded file/counts/UI and a fresh image, restore temporary state and release control. Use manual picking where the adapter is unavailable. No paid upload is required.
5. Report exact observed results and gaps in a focused issue/PR. Keep credentials, generated local config, private paths, raw captures and consumer assets out of it. A new OS's native picker adapter needs ownership/readback tests as well as live acceptance.
