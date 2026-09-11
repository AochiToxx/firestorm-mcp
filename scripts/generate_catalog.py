"""Generate tool docs from code and a historical API reference; never connect live."""
import hashlib
import json
from pathlib import Path
import re
import tempfile

from firestorm_mcp.server import Tools

root = Path(__file__).resolve().parents[1]
reference = json.loads((root / 'docs/viewer-api-reference.json').read_text())
with tempfile.TemporaryDirectory() as state:
    tools = Tools(Path(state))
    for api, descriptor in reference.items():
        for op in descriptor.get('ops', []):
            name = re.sub(r'[^a-zA-Z0-9_]', '_', f"viewer_{api}_{op['name']}")
            if len(name) > 64:
                name = name[:53] + '_' + hashlib.sha256(name.encode()).hexdigest()[:10]
            tools.dynamic[name] = (api, op)
    definitions = [entry.model_dump(exclude_none=True, by_alias=True) for entry in tools.definitions_list()]
    (root / 'docs/tool-catalog.json').write_text(json.dumps(definitions, indent=2) + '\n', encoding='utf-8')
    lines = ['# Tool reference', '',
        'Generated from the current workflow definitions and historical Firestorm 7.2.4.80712 API discovery. '
        'Refresh the running viewer before relying on a dynamic operation. Counts are not test coverage.', '',
        f'{len(tools.local)} workflow tools; {len(tools.dynamic)} historical viewer operations.', '',
        '## Workflow tools', '', '| Tool | Description |', '| --- | --- |']
    lines += [f'| `{name}` | {definition.description.replace(chr(10), " ").replace("|", "/")} |'
              for name, definition in tools.definitions.items()]
    lines += ['', '## Viewer operations', '', '| API | Operations |', '| --- | --- |']
    lines += [f'| `{name}` | ' + ', '.join('`' + op['name'] + '`' for op in entry['ops']) + ' |'
              for name, entry in reference.items()]
    lines += ['', 'See [exact input schemas](tool-catalog.json) and [viewer descriptors](viewer-api-reference.json).', '']
    (root / 'docs/TOOLS.md').write_text('\n'.join(lines), encoding='utf-8')
print(f'Generated {len(definitions)} tool definitions without a viewer connection.')
