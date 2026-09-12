# Platform support

Install the MCP beside the viewer in the same desktop user session. Package installation, live viewer control and native file picking have separate support levels.

| Target | Automated checks | Live viewer support |
| --- | --- | --- |
| Windows x64 | Python 3.11–3.14; source/wheel/Inspector checks on 3.12 | Tested on Firestorm 7.2.4.80712 with MCP 0.3.0a1. Recognized English file dialogs automated. |
| Linux x64 | Ubuntu 24.04, Python 3.12 | Experimental launcher; manual file picking. |
| macOS Intel / ARM64 | macOS 15, Python 3.12 on both architectures | Experimental app-bundle launcher; manual file picking. |
| Linux ARM64 / Raspberry Pi | Ubuntu ARM64, Python 3.12 | Pi hardware/OS and a compatible Firestorm build unverified. 32-bit ARM is outside the test matrix. |
| Other/headless/remote systems | Untested; offline tools may work if dependencies install | No remote MCP endpoint or headless viewer service. |

CI uses synthetic fixtures and never launches Firestorm. Check the [verification record](VALIDATION.md) for completed runs and the [workflow](../.github/workflows/ci.yml) for the matrix.

## Viewer requirements

Install Firestorm separately for your OS/CPU. On Linux, select its supplied `firestorm` wrapper; the internal binary bypasses library/plugin setup. On macOS, select the `.app`; the MCP derives its executable and `Contents/Resources` paths.

The [official Linux build guide](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/doc/building_linux.md) targets x86_64. The [viewer distribution manifest](https://github.com/FirestormViewer/phoenix-firestorm/blob/master/indra/newview/viewer_manifest.py) documents these layouts. Neither establishes a working Pi viewer.

Use Python 3.11+ matching your OS architecture. Dependencies may need build tools where compatible wheels are unavailable. The installer uses platform-specific package metadata; the old Windows dependency snapshot is not a portable install recipe.

A headless Pi does not gain access to another PC's viewer by installing this package. The helper's loopback `/rpc` URL is internal IPC, not a remote MCP endpoint.

## Agent behavior

Read `connection_status.local_platform.native_file_dialogs`. When false, arrange manual file selection and verify importer state afterward. The native tools remain listed but return unsupported on those systems.

Setup diagnostics check prerequisites without contacting the viewer. The probe checks the bridge connection. Neither replaces visible UI readback or image inspection.

## Test a new platform

1. Record OS/CPU, Python, MCP version, viewer build and host. Install a fresh package without admin/root access and review the doctor report.
2. With the viewer disconnected, verify discovery, a synthetic asset call, structured/image results and useful errors.
3. With the desktop owner's authority, dry-run the launcher, start the viewer normally and check LEAP. Leave running viewers and foreign locks alone.
4. Acquire a bounded lease, inspect a synthetic preview, verify readback and a fresh image, restore temporary state and release control. No paid upload is needed.
5. Report observed results and gaps with a small reproduction. Keep private data out. Native picker adapters need ownership and filename-readback tests plus live acceptance.
