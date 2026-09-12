import hashlib
import importlib.util
from pathlib import Path
import shutil
import zipfile

import pytest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('build_skill', ROOT / 'scripts/build_skill.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


def staged_source(tmp_path):
    root = tmp_path / 'source'
    shutil.copytree(ROOT / 'skills', root / 'skills')
    shutil.copyfile(ROOT / 'LICENSE', root / 'LICENSE')
    return root


def test_skill_archive_is_self_contained_allowlisted_and_reproducible(tmp_path):
    root = staged_source(tmp_path)
    skill = root / 'skills/firestorm-mesh-preview'
    (skill / 'private-notes.txt').write_text('must not enter the package')
    archive, checksum = builder.build_skill(root, tmp_path / 'first')
    second, _ = builder.build_skill(root, tmp_path / 'second')
    assert archive.read_bytes() == second.read_bytes()
    with zipfile.ZipFile(archive) as bundle:
        assert set(bundle.namelist()) == {
            'firestorm-mesh-preview/SKILL.md',
            'firestorm-mesh-preview/references/importer.md',
            'firestorm-mesh-preview/LICENSE',
        }
        assert bundle.read('firestorm-mesh-preview/LICENSE') == (ROOT / 'LICENSE').read_bytes()
        assert bundle.read('firestorm-mesh-preview/references/importer.md') == (skill / 'references/importer.md').read_bytes()
    assert checksum.read_text().strip() == f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}'


@pytest.mark.parametrize('private_text', [
    'C:' + '/' + 'Users' + '/' + 'ExamplePerson/private.txt',
    'gh' + 'p_' + 'a' * 40,
])
def test_skill_archive_rejects_private_content_before_writing(tmp_path, private_text):
    root = staged_source(tmp_path)
    with (root / 'skills/firestorm-mesh-preview/references/importer.md').open('a') as output:
        output.write(private_text)
    destination = tmp_path / 'distribution'
    with pytest.raises(ValueError, match='Personal profile|Credential-like'):
        builder.build_skill(root, destination)
    assert not destination.exists()
