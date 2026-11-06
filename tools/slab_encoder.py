"""Minimal TaleSpire slab v2 encoder.

Format (official Bouncyrock spec, DumbSlabStats/format.md):
  u32 magic 0xD1CEFACE, u16 version=2, u16 layoutCount, u16 creatureCount=0
  layoutCount x { uuid (16 bytes, .NET Guid mixed-endian), u16 assetCount, u16 reserved }
  assets packed as u64: x(18 bits) | y(18)<<18 | z(18)<<36 | rot(5)<<54   (positions in 1/100 units,
  rot in 15-degree steps), grouped per layout, then an undocumented trailing u16 0.
  Whole thing gzip-compressed and base64-encoded; TaleSpire accepts it wrapped in ``` fences.
"""
import base64
import gzip
import struct
import uuid
from collections import OrderedDict

MAGIC = 0xD1CEFACE
COMPRESSED_LIMIT = 30720  # bytes after gzip, enforced by TaleSpire


class Slab:
    def __init__(self):
        self.layouts = OrderedDict()  # uuid str -> list of (x, y, z, rot_deg)
        self.names = {}

    def add(self, asset_uuid, x, y, z, rot_deg=0, name=None):
        if x < 0 or y < 0 or z < 0:
            raise ValueError(f"negative coordinate for {name or asset_uuid}: {(x, y, z)}")
        rot = int(round((rot_deg % 360) / 15.0)) % 24
        self.layouts.setdefault(asset_uuid, []).append((x, y, z, rot))
        if name:
            self.names[asset_uuid] = name

    def __len__(self):
        return sum(len(v) for v in self.layouts.values())

    def bounds(self):
        xs = [a[0] for v in self.layouts.values() for a in v]
        ys = [a[1] for v in self.layouts.values() for a in v]
        zs = [a[2] for v in self.layouts.values() for a in v]
        return (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))

    def to_bytes(self):
        out = bytearray()
        out += struct.pack("<IHHH", MAGIC, 2, len(self.layouts), 0)
        for u, assets in self.layouts.items():
            out += uuid.UUID(u).bytes_le
            out += struct.pack("<HH", len(assets), 0)
        for u, assets in self.layouts.items():
            for x, y, z, rot in assets:
                sx, sy, sz = (int(round(v * 100)) for v in (x, y, z))
                for v in (sx, sy, sz):
                    if not 0 <= v < (1 << 18):
                        raise ValueError(f"coordinate out of range: {(x, y, z)}")
                packed = sx | (sy << 18) | (sz << 36) | (rot << 54)
                out += struct.pack("<Q", packed)
        out += struct.pack("<H", 0)
        return bytes(out)

    def encode(self, fenced=True):
        raw = self.to_bytes()
        gz = gzip.compress(raw, compresslevel=9, mtime=0)
        if len(gz) > COMPRESSED_LIMIT:
            raise ValueError(f"slab too large: {len(gz)} bytes compressed (limit {COMPRESSED_LIMIT})")
        b64 = base64.b64encode(gz).decode("ascii")
        return f"```{b64}```" if fenced else b64


def decode(text):
    """Decode a slab string back to [(uuid, x, y, z, rot_deg)], for round-trip checks."""
    text = text.strip().strip("`")
    raw = gzip.decompress(base64.b64decode(text))
    magic, ver, nl, nc = struct.unpack_from("<IHHH", raw, 0)
    assert magic == MAGIC and ver == 2 and nc == 0
    off = 10
    layouts = []
    for _ in range(nl):
        u = uuid.UUID(bytes_le=raw[off:off + 16])
        cnt, _res = struct.unpack_from("<HH", raw, off + 16)
        off += 20
        layouts.append((str(u), cnt))
    out = []
    for u, cnt in layouts:
        for _ in range(cnt):
            (p,) = struct.unpack_from("<Q", raw, off)
            off += 8
            out.append((u, (p & 0x3FFFF) / 100, ((p >> 18) & 0x3FFFF) / 100,
                        ((p >> 36) & 0x3FFFF) / 100, ((p >> 54) & 31) * 15))
    return out
