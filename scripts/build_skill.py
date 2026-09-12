"""Build the optional workflow skill ZIP using an explicit, private-data-free file list."""
import argparse
import hashlib
from pathlib import Path
import re
import zipfile

SKILL_NAME = 'firestorm-mesh-preview'
SKILL_FILES = ('SKILL.md', 'references/importer.md')


def build_skill(root: Path, destination: Path):
    root = root.resolve()
    skill = root / 'skills' / SKILL_NAME
    sources = [(skill / name, f'{SKILL_NAME}/{name}') for name in SKILL_FILES]
    sources.append((root / 'LICENSE', f'{SKILL_NAME}/LICENSE'))
    records = []
    for source, name in sources:
        if source.is_symlink() or any(parent.is_symlink() for parent in source.parents if parent != root):
            raise ValueError(f'Symlink cannot enter a skill release: {name}')
        data = source.read_bytes()
        content = data.decode('utf-8')
        if re.search(r'(?i)[A-Z]:[/\\]+Users[/\\]+[^/\\\s]+', content):
            raise ValueError(f'Personal profile path in {name}')
        if re.search(r'gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', content):
            raise ValueError(f'Credential-like content in {name}')
        records.append((name, data))
    entrypoint = records[0][1].decode('utf-8')
    # This repository owns this simple frontmatter shape; this is not a YAML parser.
    versions = re.findall(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"\s*$', entrypoint, re.MULTILINE)
    if len(versions) != 1 or f'\nname: {SKILL_NAME}\n' not in entrypoint.replace('\r\n', '\n'):
        raise ValueError('Expected the skill name and one quoted metadata version')
    destination = destination.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f'{SKILL_NAME}-{versions[0]}.zip'
    with zipfile.ZipFile(archive, 'w') as bundle:
        for name, data in records:
            info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            bundle.writestr(info, data)
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise ValueError('Skill archive integrity check failed')
    checksum = destination / f'{SKILL_NAME}-{versions[0]}-SHA256SUMS.txt'
    checksum.write_text(f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n', encoding='utf-8')
    return archive, checksum


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'dist')
    args = parser.parse_args()
    archive, checksum = build_skill(Path(__file__).resolve().parents[1], args.output_dir)
    print(f'Created {archive.name} and {checksum.name}; no viewer or agent configuration was changed.')
