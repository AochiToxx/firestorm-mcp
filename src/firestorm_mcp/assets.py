"""Read-only export checks and comparison evidence. Never claims simulator validation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import struct
import xml.etree.ElementTree as ET

from PIL import Image, ImageChops, ImageStat


def file_record(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return {"path": str(path.resolve()), "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def inspect_asset(filename: str):
    path = Path(filename).resolve(strict=True)
    result = {**file_record(path), "evidence_kind": "local_export_metadata", "simulator_verified": False}
    suffix = path.suffix.lower()
    if suffix == ".dae":
        if path.stat().st_size > 256 * 1024 * 1024:
            raise ValueError("DAE inspection is limited to 256 MiB")
        document = ET.parse(path)
        root = document.getroot()
        ns = {"c": root.tag.split("}")[0].removeprefix("{")} if "}" in root.tag else {}
        def findall(name):
            return root.findall(".//c:" + name, ns) if ns else root.findall(".//" + name)
        unit = findall("unit")
        up = findall("up_axis")
        images = []
        for item in findall("image"):
            source = next((e.text for e in item.iter() if e.tag.rsplit("}", 1)[-1] == "init_from"), None)
            images.append({"id": item.get("id"), "source": source})
        primitives = []
        for kind in ("triangles", "polylist", "polygons", "lines", "trifans", "tristrips"):
            for item in findall(kind):
                primitives.append({"kind": kind, "count": int(item.get("count", 0)), "material_symbol": item.get("material")})
        result.update(format="COLLADA", version=root.get("version"),
                      unit_meter=float(unit[0].get("meter", 1)) if unit else 1,
                      up_axis=up[0].text if up else "Y_UP (COLLADA default)",
                      geometry_count=len(findall("geometry")), primitives=primitives,
                      declared_triangles=sum(p["count"] for p in primitives if p["kind"] == "triangles"),
                      material_count=len(findall("material")), image_references=images)
    elif suffix in (".gltf", ".glb"):
        if path.stat().st_size > 256 * 1024 * 1024:
            raise ValueError("glTF inspection is limited to 256 MiB")
        if suffix == ".glb":
            with path.open("rb") as stream:
                magic, version, total = struct.unpack("<4sII", stream.read(12))
                if magic != b"glTF" or version != 2 or total != path.stat().st_size:
                    raise ValueError("Invalid GLB v2 header")
                length, chunk_type = struct.unpack("<II", stream.read(8))
                if chunk_type != 0x4E4F534A or length > total - 20:
                    raise ValueError("Invalid GLB JSON chunk")
                data = json.loads(stream.read(length))
        else:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        result.update(format="glTF", asset=data.get("asset"), mesh_count=len(data.get("meshes", [])),
                      materials=data.get("materials", []), images=data.get("images", []),
                      extensions_used=data.get("extensionsUsed", []),
                      note="File inspection does not establish support by the viewer's mesh or material importer.")
    else:
        with Image.open(path) as img:
            result.update(format=img.format, width=img.width, height=img.height, mode=img.mode,
                          channels=img.getbands())
    return result


def compare_images(reference: str, observed: str, output: Path):
    with Image.open(reference) as ref, Image.open(observed) as obs:
        a, b = ref.convert("RGB"), obs.convert("RGB")
        if a.size != b.size:
            raise ValueError(f"Image dimensions differ: {a.size} vs {b.size}. Align captures before pixel comparison.")
        difference = ImageChops.difference(a, b)
        difference.save(output)
        stats = ImageStat.Stat(difference)
        return {"reference": file_record(Path(reference)), "observed": file_record(Path(observed)),
                "difference": str(output), "mean_absolute_error_rgb_0_255": stats.mean,
                "evidence_kind": "pixel_comparison", "semantic_match_verified": False,
                "note": "Lighting, camera, tone mapping and renderer differences affect this metric."}
