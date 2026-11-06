#!/usr/bin/env python3
"""Calibration slab: shaped exterior pieces in a numbered row, each with a 1x1 floor tile as a
size reference one unit behind it (north). Paste it once, look at it from above and from the side,
and note which pieces are which size and which way they face."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from slab_encoder import Slab  # noqa: E402

PIECES = [
    ("Hull_Sidewall_center_1x1", "1577ee9a-c50d-490c-8604-8b3194e42131"),
    ("HullSideWall A", "77017a39-cf6a-488d-a409-cc17880b8ada"),
    ("HullSideWall B", "c2f8a532-e9e9-49ce-acd2-51be2ca2f1dc"),
    ("Hull_Sidewall_top_1x2", "9941b2ab-bf37-46e6-9404-51d1c9d90d31"),
    ("Hull_Sidewall_bottom_1x2", "f8c71f78-6bd3-4c97-8692-a87f3d593b49"),
    ("space ship wall 2x2 ribbed", "3d415700-51fd-443b-bc45-d0189e66f3c0"),
    ("space ship wall 2x2 compact", "1ae589b7-1cfb-4b63-80df-08319cdb246b"),
    ("space ship wall 2x2 window", "9a3fac1c-2df5-40e8-9d24-07c79970eee6"),
    ("space ship wall 1x1 corner curved", "dddb8739-297a-49b2-a348-38fbd2add877"),
    ("space ship wall 1x1 curved curved bottom", "71042cce-badb-461d-94fa-ea6d8dc0f137"),
    ("space ship wall 1x1 basic corner", "33b7dac3-42b8-4fdd-b8c8-d56d7cd1c866"),
    ("space ship ceiling 1x1 curved", "daa74875-45aa-4443-b131-3357d2e96045"),
    ("space ship ceiling 1x1 curved soft", "e7f8f9a7-17ae-462a-8b54-597509d2444f"),
    ("space ship floor 2x2 metal plane curved", "226468f3-88c6-4cb0-a608-3128fb2baa96"),
    ("external top 2x2 A", "3389fc47-8b6b-496a-bda1-dbe67303ec49"),
    ("external top 2x2 B", "ec695e81-4ae5-4c7b-ab22-0a19f4dec132"),
    ("external top 1x2", "bb40173f-c197-480c-8f52-84dbf538ea8d"),
    ("external wall 2x2 unique wall A", "e8ff11e1-d229-43b7-8f9f-dfad32fc43b2"),
    ("external wall 1x1 exterior side", "3d3d335a-18ed-4377-b1d9-166b77028cb6"),
    ("exterior 1x1 top support A", "4d26e0db-23d2-41ca-8130-701797833599"),
    ("exterior 1x1 lower support A", "f94b8d86-02d0-481c-b164-2ffafe1b5e18"),
    ("cockpit 2x2 inner window lower", "d6396479-8783-42c8-97d2-2c87d51a7d03"),
    ("Front 2x2 inner window upper", "8ea5c367-c01f-4f5a-8d4a-50b6c09c0ea3"),
    ("cockpit 1x1 wall window upper", "c088b36e-6f4d-4bd7-91fb-3a9c85782d98"),
    ("cockpit 2x2 corner A window lower", "10f5184c-0cf2-4df9-abe1-e8f5083afb8b"),
    ("Front 2x2 corner A window upper", "0eafbf16-11dc-44c5-922f-b03b40a85a4a"),
    ("cockpit 2x2 floor corner A", "8fc69a82-0007-40fd-b4a8-4c685af8683c"),
    ("caged tunnel upper wall 01", "00ee5cc5-e27b-4d60-8048-99c1b1c4ef8b"),
    ("caged tunnel lower deck wall 01", "dddcc2ac-4eb3-4058-9065-ae5fcbb6de7f"),
    ("scifi Caged tunnel ceiling 01", "ea99742b-22dc-4995-8541-46d7855235da"),
    ("station wall 2x2", "e3750f74-2b5a-4fd7-a103-329b4fad17ec"),
    ("tech wall 2x2", "b056f270-f907-41b5-9044-ada24ce804a0"),
    ("Hull01_floor2x2", "73b12504-0f23-4b3f-b814-50db20c004f0"),
    ("Thruster static", "e97166a4-0626-4e31-a107-fd869aec2985"),
    ("Jet Engine", "c4958c89-46fd-4b6a-a042-008c1b4ba8d8"),
    ("Engine", "a6a9d645-01bd-4af6-af95-89f1f233df0c"),
]
FLOOR = ("space ship floor 1x1", "36147fe1-3850-4662-a95e-1a56be8a14b4")
GLOW = ("scifi floor glow 1x1", "bd4507ba-85ba-4748-9142-b4857a8d8f89")

PER_ROW, STEP, ROW_GAP = 12, 5, 8


def main(out_path):
    s = Slab()
    for i, (name, u) in enumerate(PIECES):
        x = 2 + (i % PER_ROW) * STEP
        z = 16 + (i // PER_ROW) * ROW_GAP                # rows go north; counters fit south of row 1
        s.add(u, x, 0, z, 0, name)                       # the piece, rotation 0
        s.add(FLOOR[1], x, 0, z + 3, 0, FLOOR[0])        # 1x1 reference tile 3 units north
        for k in range(1, (i % PER_ROW) + 2):            # unary column counter south of the piece
            s.add(GLOW[1], x, 0, z - 1 - k, 0, GLOW[0])
    with open(out_path, "w") as f:
        f.write(s.encode() + "\n")
    print("pieces:")
    for i, (name, u) in enumerate(PIECES):
        print(f"  row {i // PER_ROW + 1}, column {i % PER_ROW + 1:2d}: {name}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "grasshopper", "test_pieces.slab.txt"))
