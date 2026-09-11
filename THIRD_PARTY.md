# Dependencies and upstream references

Firestorm MCP's Python bridge and synthetic test fixture are distributed under the MIT licence in LICENSE. Dependencies retain their own licences and are installed from their package distributions; preserve their notices when redistributing bundled dependencies.

| Dependency | Licence reported by the inspected distribution |
| --- | --- |
| MCP Python SDK | MIT |
| jsonschema | MIT |
| llsd | MIT |
| Pillow | MIT-CMU |
| pywin32 | PSF |
| psutil | BSD-3-Clause |

Consult installed package metadata and bundled notices for the exact version you distribute, including transitive dependencies. This file is an attribution inventory, not a replacement for those notices.

The [Firestorm source repository](https://github.com/FirestormViewer/phoenix-firestorm) is upstream reference material for LEAP/XUI behavior and is LGPL licensed. The Windows APR duplicate-block workaround was informed by the documented behavior in [llprocess.cpp at the tested release](https://github.com/FirestormViewer/phoenix-firestorm/blob/Firestorm_Release_7.2.4.80712/indra/llcommon/llprocess.cpp). The bridge implements local transport recovery in Python; it does not bundle the Firestorm viewer, its C++ sources, skins, Havok, FMOD or other viewer components.

The historical API descriptor JSON contains interface names and descriptions emitted by the viewer. It is included as compatibility documentation with upstream attribution, not as a promise of support on every release. Install the viewer from [its official website](https://www.firestormviewer.org/).
