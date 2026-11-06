#!/usr/bin/env python3
"""Build the 'Grasshopper' (Death in Space) deck plan as TaleSpire slabs.

Grid: the deck plan's squares. col = plan column (west -> east), row = plan row (north -> south).
World: x = col, z = NROWS - row  (north is +z), y up.  1 square = 1 TaleSpire unit.

Placement conventions (from TaleSpire's own data model, see README):
  * tiles (floors, walls, doors, ceilings): stored position = min corner of the axis-aligned
    footprint; for 90/270 degree rotations TaleSpire swaps the x/z size.
  * props: stored position = pivot (roughly footprint centre at the base).
  * y: floors, walls and props on the same deck share y = 0 (floor origin = its top surface).

Tunable assumptions are collected in the CONFIG block; change them if walls/doors look offset
or rotated the wrong way in game and re-run the script.
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from slab_encoder import Slab  # noqa: E402

# ----------------------------------------------------------------------------- CONFIG
WALL_T = 0.5          # assumed footprint thickness of 'space ship wall 1x1 basic' (walls are
                      # centred on the plan's wall lines; error <= 0.25 for any real thickness)
WALL_ALONG_X_ROT = 0  # rotation at which a wall tile runs along the x axis (0 or 90)
DIAG_SIGN = -1        # +1 or -1: flips which way 45-degree pieces turn (Unity: +Y rot is clockwise)
CEIL_Y = 2.0          # height of the ceiling layer (wall height)
PROP_Y = 0.0          # props sit on the floor plane
FACE = {"N": 0, "E": 90, "S": 180, "W": 270}  # prop 'front' at rot 0 assumed to face +z (north)

# ----------------------------------------------------------------------------- ASSETS
A = {
    "floor1": ("36147fe1-3850-4662-a95e-1a56be8a14b4", "space ship floor 1x1"),
    "floor2": ("f095ea12-0e41-4a79-bf3b-9fa0b4400369", "space ship floor 2x2"),
    "floorglow": ("bd4507ba-85ba-4748-9142-b4857a8d8f89", "scifi floor glow 1x1"),
    "hatchfloor": ("d58e27d0-3a41-4cb7-b6c8-c389ca16360b", "space ship hatch horizontal 01"),
    "wall": ("09f8bec6-263d-4e96-bef5-eba63f27a114", "space ship wall 1x1 basic"),
    "door": ("f56d891a-ed49-4e6e-910e-81827e8eac37", "space ship door 1x1"),
    "door2": ("ae40e42f-2a00-4b99-97e1-c3d41baadc27", "space ship door double"),
    "hatch": ("cac3888c-f04b-4da9-b0b3-db6e2d4b7b75", "space ship hatch Vertical 01"),
    "ceil": ("c6619e55-11f4-4a20-b790-8970917c23ab", "space ship ceiling 1x1"),
    # props
    "console": ("e9e64ec2-f473-46da-8267-107eaee37495", "sci fi console_  mid"),
    "console_main": ("a4857731-d982-4c81-95fa-50791b404b68", "Interstellar Console main"),
    "console_screen": ("52d56d1a-772a-47d9-97be-9c8f824f3e6f", "Interstellar Console base w screen"),
    "terminal": ("9c4c8b19-379f-4c9e-9add-5bca941e0def", "sci fi terminal"),
    "holotable": ("6e5804b7-381e-42b6-ae8d-3f2923025cab", "Interstellar travel ON_OFF mech"),
    "pilot": ("c928a5e6-c479-47d7-984c-4254f8780338", "scifi chair pilot"),
    "chair": ("9d4ea828-db15-48fc-8ebe-65734ed4c722", "Interstellar chair"),
    "seat": ("db61b415-d7bb-41bb-bfd1-d3fc2404c7e9", "scifi seat terminal"),
    "table": ("fd24e8e2-b4d4-4627-8573-4d06980db53e", "scifi_table 01 A"),
    "conftable": ("224d71a4-136f-431d-ae57-803d2de31a77", "ConferenceTable_Office"),
    "bed": ("6e2c7f4e-c1f0-41a9-9e7b-24ec6076ec8b", "unit bed"),
    "cryo": ("3a5512c2-c266-44fc-8ba2-bf4e805745b0", "Cryo sleep lux"),
    "locker": ("e5446734-1eec-45f0-9aff-7cdddf6a459e", "Locker v1"),
    "locker2": ("4abd32cc-01b3-43ba-a748-222f8449c85d", "Locker v2"),
    "bench": ("fe2fa079-9bba-4b07-a008-0c1ef85531c3", "bench locker large"),
    "benchs": ("532dea3c-26df-48f7-9b8d-29fc1271db87", "bench locker small"),
    "crate": ("da125361-6adc-4d02-9805-bebf22dc340f", "sci fi crate L 01"),
    "chest": ("84d38667-a961-4562-93b4-ec38aeb81c55", "sci fi chest 02"),
    "case": ("abf5a41b-606e-4aa9-87ba-5964dbda73f8", "case of supplies 01"),
    "casemini": ("721fea1e-ca6e-4b00-b32e-178883774c23", "case of supplies 01 mini B"),
    "casemini2": ("6fe3a290-76ba-4f37-a484-77a520310643", "case of supplies 02 mini A"),
    "cable": ("26bc0db4-0c94-46ef-a64f-71e4b5a9a996", "Cable floor v1"),
    "rubble": ("ac288dec-372b-4c7a-b70f-3a48115920ab", "Rubble pebbles spread out"),
    "plant1": ("8fcd4b46-c6f3-4d50-b950-ef4557ffe7b4", "Jungle plant 01"),
    "plant2": ("ec794aa6-27da-4e8e-a122-4042a27f2c3f", "Jungle plant 02"),
    "pitcher": ("6e5af318-1737-4bf3-a35f-a3530f6fd2de", "Pitcher plant"),
    "bucket": ("0e3f8516-9ef8-46c2-a0f3-f9584c294c9f", "grass bucket v1"),
    "toilet": ("d857a8c6-15b1-4102-8470-275574e8b2bc", "toilette residential"),
    "sink": ("6dd89e0f-27f6-45f8-85ff-799dc03d1e67", "sink residential"),
    "reactor": ("f3439bf0-9619-43fa-b516-768945d72a36", "Interstellar battery mech"),
    "cooler": ("1c380641-1d35-4bd2-9c31-51593cf83179", "battery cooler with battery"),
    "generator": ("3becaf94-92d4-425e-b870-8ce345a453a4", "Interstellar egg mech"),
    "pipe": ("4da1b40b-f0cf-44eb-8e38-aa742f21a0b8", "machine pipe 01"),
    "pipe2": ("eb23f5c6-8646-4374-8505-aaecf8faaaa4", "scifi pipe medial 01"),
    "helm": ("c8250950-a9f6-4d74-986c-3943cc39d6d4", "Astronaut helm"),
    "boots": ("28a6c1fd-edc2-4a71-8ca1-06e783da6c0e", "Astronaut boots"),
    "medkit": ("a341f6d2-f769-41b4-8afc-e9f9eecd0768", "medkit chest 01"),
    "lamp": ("bfc0bcfa-3df5-4890-9654-6138c27b6e13", "Lamp Small"),
    "wallcase": ("d7c23080-3aa2-42bc-8e0a-392b406990b8", "wall case 01"),
}

# ----------------------------------------------------------------------------- LAYOUT
NROWS = 36
NCOLS = 53


def rect(c0, r0, c1, r1):
    return {(c, r) for c in range(c0, c1 + 1) for r in range(r0, r1 + 1)}


ROOMS = {}  # name -> set of full floor cells (col,row)

# Bridge (west)
ROOMS["nose"] = rect(1, 10, 2, 11)
ROOMS["bridge"] = rect(3, 8, 10, 13) - {(3, 8), (4, 8), (3, 9), (3, 12), (3, 13), (4, 13), (10, 8), (10, 13)}
ROOMS["airlock_n"] = rect(7, 6, 8, 7)
ROOMS["airlock_s"] = rect(7, 14, 8, 15)
ROOMS["bridge_link"] = rect(11, 10, 12, 11)
# Observation / mess room (round) with apse
ROOMS["hex"] = rect(14, 8, 17, 8) | rect(13, 9, 18, 12) | rect(14, 13, 17, 13)
ROOMS["hex_apse"] = rect(15, 7, 16, 7)
ROOMS["hex_south"] = rect(15, 14, 16, 15)
ROOMS["hex_east"] = rect(19, 10, 19, 11)
# Engineering below the round room
ROOMS["engineering"] = rect(14, 16, 18, 21) - {(14, 20), (14, 21), (15, 21)}
# Top-left block
ROOMS["passage20"] = rect(20, 4, 20, 9)
ROOMS["closet"] = rect(21, 5, 21, 9)
ROOMS["corr_top_w"] = (rect(20, 3, 28, 4) - {(20, 3)}) | rect(26, 2, 27, 2)
ROOMS["storage"] = rect(22, 5, 26, 9) - {(26, 5)}
ROOMS["corr_central"] = rect(27, 5, 28, 24)
ROOMS["corr_hex_east"] = rect(20, 10, 26, 11) | rect(29, 10, 30, 11)
ROOMS["hydroponics"] = rect(25, 25, 28, 28) - {(25, 27), (25, 28), (26, 28)}
ROOMS["corr_top_e"] = rect(29, 3, 44, 3)
# Mess hall
ROOMS["mess"] = rect(31, 8, 43, 13) - {(42, 8), (43, 8), (43, 9), (42, 13), (43, 13), (43, 12)}
ROOMS["alcove_nw"] = rect(33, 6, 34, 7)
ROOMS["alcove_ne"] = rect(36, 6, 37, 7)
ROOMS["alcove_sw"] = rect(33, 14, 34, 15)
ROOMS["alcove_se"] = rect(36, 14, 37, 15)
ROOMS["bath_n"] = rect(39, 7, 40, 7)
ROOMS["bath_s"] = rect(39, 14, 40, 14)
ROOMS["mess_rw_link"] = rect(44, 10, 44, 11)
# Right wing
ROOMS["rw_hall"] = rect(45, 8, 49, 13) | rect(50, 10, 50, 12)
ROOMS["rw_north"] = rect(47, 7, 48, 7)
ROOMS["rw_south"] = rect(47, 14, 48, 15)
ROOMS["topright"] = {(45, 3), (46, 2), (46, 3), (46, 4)} | rect(47, 1, 49, 5) | rect(47, 6, 48, 6)
ROOMS["machine"] = rect(44, 17, 48, 21) | rect(45, 16, 48, 16) | rect(41, 18, 43, 21) | rect(40, 20, 40, 21)
ROOMS["reactor"] = rect(49, 16, 50, 18) | {(51, 17)}
ROOMS["corr_right"] = rect(49, 19, 50, 29)
ROOMS["vestibule"] = rect(29, 20, 29, 21)
ROOMS["cargo"] = rect(30, 18, 38, 23) | rect(39, 20, 39, 21)
ROOMS["cargo_closet"] = rect(39, 18, 40, 19)
ROOMS["lower"] = (rect(39, 22, 45, 23) | rect(36, 24, 45, 25) | rect(37, 26, 45, 26)
                  | rect(38, 27, 45, 27) | rect(38, 28, 44, 28) | rect(38, 29, 43, 29))
ROOMS["hangar"] = (rect(34, 24, 35, 26) | rect(33, 27, 36, 27) | rect(32, 28, 37, 30)
                   | rect(34, 31, 35, 32))
ROOMS["generator"] = rect(44, 30, 48, 30) | rect(44, 31, 47, 31) | rect(44, 32, 46, 32)

# Cells cut by a 45-degree wall: floor + ceiling are laid, but no straight walls are generated
# around them; the diagonal wall pieces below take over.
DIAG_CELLS = {
    (4, 8), (3, 9), (4, 13), (3, 12), (10, 8), (10, 13),            # bridge chamfers
    (13, 8), (18, 8), (13, 13), (18, 13),                            # round room corners
    (14, 20), (15, 21),                                              # engineering chamfer
    (20, 3), (26, 5),                                                # top-left chamfers
    (25, 27), (26, 28),                                              # hydroponics chamfer
    (42, 8), (43, 9), (42, 13), (43, 12),                            # mess hall east chamfers
    (50, 9), (50, 13),                                               # right wing
    (45, 2), (46, 1), (45, 4), (46, 5),                              # top-right block
    (44, 16), (43, 17),                                              # machine room
    (51, 16), (51, 18),                                              # reactor bulge
    (45, 28), (44, 29), (36, 26), (37, 27),                          # lower room
    (33, 26), (32, 27),                                              # hangar funnel
    (49, 30), (48, 31), (47, 32),                                    # generator room
}

# Diagonal walls: ((col, row) -> (col, row)) in grid-point coordinates, optional 'door' flag.
DIAG_WALLS = [
    ((5, 8), (3, 10)), ((3, 12), (5, 14)), ((10, 8), (11, 9)), ((11, 13), (10, 14)),
    ((14, 8), (13, 9)), ((18, 8), (19, 9)), ((13, 13), (14, 14)), ((19, 13), (18, 14)),
    ((14, 20), (16, 22)),
    ((20, 4), (21, 3)), ((26, 5), (27, 6)),
    ((25, 27), (27, 29)),
    ((42, 8), (44, 10)), ((44, 12), (42, 14)),
    ((50, 9), (51, 10)), ((51, 13), (50, 14)),
    ((45, 3), (47, 1)), ((45, 4), (47, 6)),
    ((43, 18), (45, 16)),
    ((51, 16), (52, 17)), ((52, 18), (51, 19)),
    ((36, 26), (38, 28)), ((34, 26), (32, 28)),
    ((47, 33), (50, 30)),
    ((46, 28), (44, 30), "door"),
]

# Explicit walls between two floor cells ('h', col, row) = north edge of cell (col,row) i.e. the
# boundary at plan row `row`; ('v', col, row) = west edge of cell (col,row), boundary at plan col `col`.
PARTITIONS = (
    [("v", 21, r) for r in range(5, 10)] + [("v", 22, r) for r in range(5, 10)]
    + [("h", c, 5) for c in range(22, 26)] + [("v", 27, r) for r in range(6, 10)]
    + [("h", c, 10) for c in range(22, 27)]
    + [("h", 40, 8), ("h", 40, 14)]
    + [("h", 39, 20), ("h", 40, 20), ("v", 39, 18), ("v", 39, 19), ("v", 41, 18)]
    + [("v", 39, 22), ("v", 39, 23), ("h", 39, 22)]
    + [("h", c, 22) for c in (40, 42, 43, 44, 45)]
    + [("h", 36, 24), ("h", 37, 24), ("h", 38, 24), ("v", 36, 24), ("v", 36, 25)]
)

# Doors: edge -> kind ('door' single, 'door2' half of a double door, 'hatch' airlock/pod hatch)
DOORS = {
    ("v", 7, 7): "hatch", ("v", 9, 7): "hatch", ("v", 7, 14): "hatch", ("v", 9, 14): "hatch",
    ("v", 12, 10): "door2", ("v", 12, 11): "door2",
    ("h", 15, 15): "door2", ("h", 16, 15): "door2",
    ("v", 20, 10): "door2", ("v", 20, 11): "door2",
    ("h", 21, 5): "door", ("h", 21, 10): "door",
    ("h", 27, 7): "door2", ("h", 28, 7): "door2",
    ("h", 27, 25): "door2", ("h", 28, 25): "door2",
    ("v", 30, 20): "door2", ("v", 30, 21): "door2",
    ("h", 34, 24): "door2", ("h", 35, 24): "door2",
    ("h", 34, 32): "hatch", ("h", 35, 32): "hatch",
    ("v", 40, 20): "door2", ("v", 40, 21): "door2",
    ("v", 41, 19): "door",
    ("h", 39, 8): "door", ("h", 39, 14): "door",
    ("v", 44, 10): "door2", ("v", 44, 11): "door2",
    ("h", 47, 7): "door2", ("h", 48, 7): "door2",
    ("h", 47, 15): "door2", ("h", 48, 15): "door2",
    ("h", 41, 22): "door",
    ("v", 49, 22): "hatch", ("v", 49, 24): "hatch", ("v", 49, 26): "hatch", ("v", 49, 28): "hatch",
}

# Special floor tiles replacing the standard floor at given cells
SPECIAL_FLOOR = {
    (47, 4): "floorglow", (48, 4): "floorglow", (47, 5): "floorglow", (48, 5): "floorglow",  # lift pad
    (39, 9): "hatchfloor",                                                                   # deck hatch
}

# Props: (asset key, x, row_y, rot_deg).  x/row_y are plan coordinates (fractional allowed),
# rot via FACE[...] for facing or explicit degrees (0 = long axis along north/south).
P = []


def prop(key, x, ry, rot=0):
    P.append((key, x, ry, rot))


# -- bridge
prop("console", 1.45, 11.0, FACE["E"]); prop("pilot", 2.4, 11.0, FACE["W"])
prop("console", 5.3, 8.6, 135); prop("console", 4.4, 9.5, 135); prop("pilot", 5.5, 9.6, 315)
prop("console", 5.3, 13.4, 45); prop("console", 4.4, 12.5, 45); prop("pilot", 5.5, 12.4, 225)
prop("holotable", 8.0, 11.0, 0)
prop("chair", 6.5, 11.0, FACE["E"]); prop("chair", 9.5, 11.0, FACE["W"])
prop("terminal", 10.5, 9.5, FACE["W"]); prop("seat", 9.6, 9.5, FACE["E"])
prop("terminal", 10.5, 12.5, FACE["W"]); prop("seat", 9.6, 12.5, FACE["E"])
# -- round room
prop("table", 16.0, 11.0, 0)
for (x, ry, f) in [(15.3, 9.6, "S"), (16.7, 9.6, "S"), (15.3, 12.4, "N"), (16.7, 12.4, "N")]:
    prop("chair", x, ry, FACE[f])
prop("console", 16.0, 7.4, FACE["S"]); prop("chair", 16.0, 8.4, FACE["N"])
prop("plant1", 13.6, 9.5, 0); prop("plant2", 18.4, 12.5, 0)
# -- engineering
for r in (16, 17, 18):
    prop("locker", 14.5, r + 0.5, FACE["E"])
for r in (16, 17, 18, 19):
    prop("locker", 18.5, r + 0.5, FACE["W"])
prop("terminal", 16.0, 18.5, FACE["N"]); prop("seat", 16.0, 17.5, FACE["S"])
for c in (16, 17, 18):
    prop("console_screen", c + 0.5, 21.5, FACE["N"])
prop("console_main", 15.3, 20.7, 135)
prop("pipe2", 17.5, 16.4, 90)
# -- storage / closet
prop("bench", 23.0, 5.5, FACE["S"]); prop("bench", 25.0, 5.5, FACE["S"])
prop("crate", 23.5, 8.5, 0); prop("case", 25.5, 7.5, 15)
prop("wallcase", 21.5, 7.5, FACE["E"])
# -- central corridor clutter
prop("casemini2", 28.5, 22.5, 15); prop("casemini2", 28.4, 23.6, 345)
# -- mess hall
prop("conftable", 35.5, 11.0, 90)
for (x, ry, f) in [(34.0, 9.6, "S"), (36.0, 9.6, "S"), (33.1, 11.0, "E"), (37.9, 11.0, "W"),
                   (34.0, 12.4, "N"), (36.0, 12.4, "N")]:
    prop("chair", x, ry, FACE[f])
prop("locker", 31.5, 8.5, FACE["E"]); prop("locker", 31.5, 9.5, FACE["E"])
prop("bed", 32.0, 13.0, 90)
prop("bench", 41.1, 9.0, 135); prop("bench", 41.1, 13.0, 45)
prop("medkit", 39.5, 10.6, 0)
prop("bed", 34.0, 7.0, 0); prop("bed", 37.0, 7.0, 0); prop("bed", 34.0, 15.0, 0); prop("bed", 37.0, 15.0, 0)
prop("toilet", 39.5, 7.5, FACE["S"]); prop("sink", 40.5, 7.5, FACE["S"])
prop("toilet", 39.5, 14.5, FACE["N"]); prop("sink", 40.5, 14.5, FACE["N"])
# -- right wing hall (cryo)
prop("cryo", 46.0, 8.5, 90); prop("cryo", 46.0, 13.5, 90)
prop("cryo", 49.5, 9.4, 315); prop("cryo", 49.5, 12.6, 45)
prop("locker2", 50.6, 11.0, FACE["W"])
prop("rubble", 46.2, 12.3, 0)
# -- top-right block
prop("terminal", 48.6, 1.4, 315)
prop("lamp", 49.5, 4.5, 0)
# -- machine room / reactor
prop("bench", 42.0, 18.5, FACE["S"]); prop("bench", 46.0, 16.5, FACE["S"]); prop("bench", 45.0, 21.5, FACE["N"])
prop("casemini", 44.0, 21.3, 20); prop("casemini", 46.0, 21.3, 340)
prop("reactor", 50.0, 17.6, FACE["W"]); prop("cooler", 50.6, 16.6, FACE["W"])
prop("pipe", 49.3, 16.6, 0); prop("pipe", 49.3, 18.8, 0)
prop("benchs", 49.5, 16.4, FACE["S"]); prop("benchs", 49.2, 19.8, FACE["E"])
# -- cargo bay
prop("cable", 30.6, 18.6, 0)
prop("case", 32.3, 19.3, 15); prop("case", 33.5, 19.0, 0); prop("case", 34.7, 18.5, 0)
prop("chest", 35.7, 18.4, 0); prop("crate", 37.6, 18.9, 30)
prop("case", 31.6, 22.6, 15); prop("case", 33.0, 22.7, 0); prop("crate", 32.1, 23.5, 345)
prop("casemini", 33.9, 23.3, 0); prop("casemini", 34.6, 23.2, 20)
prop("rubble", 33.0, 20.3, 0); prop("rubble", 36.2, 19.6, 0)
prop("chest", 38.6, 21.6, 10); prop("locker2", 38.6, 23.2, FACE["W"]); prop("chest", 39.5, 21.0, 0)
# -- hydroponics
prop("bench", 25.5, 26.0, FACE["E"]); prop("bench", 27.3, 28.5, FACE["N"])
prop("plant1", 26.6, 25.6, 0); prop("plant2", 27.5, 27.4, 0); prop("bucket", 26.4, 27.3, 0)
prop("pitcher", 27.6, 25.6, 0); prop("casemini2", 26.1, 26.9, 30)
# -- hangar
prop("bed", 36.6, 27.4, 45)
prop("bench", 32.5, 29.0, FACE["E"]); prop("bench", 37.5, 29.0, FACE["W"])
prop("casemini", 33.8, 30.4, 20); prop("helm", 33.2, 30.7, 0); prop("boots", 34.6, 30.6, 0)
# -- generator room
prop("generator", 46.0, 31.9, 0); prop("pipe2", 44.5, 31.5, 90)
# -- escape pods (outside the starboard corridor)
for r in (22, 24, 26, 28):
    prop("cryo", 48.0, r + 0.5, 90)

# ----------------------------------------------------------------------------- BUILD


def wz(row):
    """world z of the north edge of plan row `row` (boundary line)."""
    return NROWS - row


def main(out_dir):
    floor = set().union(*ROOMS.values())
    assert not (floor & DIAG_CELLS), floor & DIAG_CELLS
    all_cells = floor | DIAG_CELLS

    # --- walls from floor edges
    edges = {}  # ('h'|'v', col, row) -> kind
    for (c, r) in floor:
        for key, (nc, nr) in {("h", c, r): (c, r - 1), ("h", c, r + 1): (c, r + 1),
                              ("v", c, r): (c - 1, r), ("v", c + 1, r): (c + 1, r)}.items():
            if (nc, nr) in all_cells:
                continue
            edges[key] = "wall"
    for key in PARTITIONS:
        edges[key] = "wall"
    for key, kind in DOORS.items():
        edges[key] = kind

    # --- slabs
    s_floor, s_walls, s_props, s_ceil = Slab(), Slab(), Slab(), Slab()

    def add(slab, key, x, y, z, rot):
        u, n = A[key]
        slab.add(u, round(x, 2), round(y, 2), round(z, 2), rot, n)

    # floors: greedy 2x2 where possible
    done = set()
    for (c, r) in sorted(all_cells):
        if (c, r) in done or (c, r) in SPECIAL_FLOOR:
            continue
        block = {(c, r), (c + 1, r), (c, r + 1), (c + 1, r + 1)}
        if block <= all_cells and not (block & done) and not (block & set(SPECIAL_FLOOR)):
            add(s_floor, "floor2", c, 0, wz(r + 2), 0)
            done |= block
        else:
            add(s_floor, "floor1", c, 0, wz(r + 1), 0)
            done.add((c, r))
    for (c, r), key in SPECIAL_FLOOR.items():
        add(s_floor, key, c, 0, wz(r + 1), 0)

    # walls / doors along cell edges
    rot_x = WALL_ALONG_X_ROT % 360
    rot_z = (WALL_ALONG_X_ROT + 90) % 360
    handled = set()
    for (kind_axis, c, r), kind in sorted(edges.items()):
        if (kind_axis, c, r) in handled:
            continue
        asset = {"wall": "wall", "door": "door", "hatch": "hatch", "door2": "door2"}[kind]
        length = 1
        if kind == "door2":  # pair the two halves of a double door
            nxt = (kind_axis, c + 1, r) if kind_axis == "h" else (kind_axis, c, r + 1)
            if edges.get(nxt) == "door2" and nxt not in handled:
                handled.add(nxt)
                length = 2
            else:
                asset = "door"
        if kind_axis == "h":  # runs along x, boundary at plan row r -> z = wz(r)
            z0 = wz(r) - WALL_T / 2
            add(s_walls, asset, c, 0, z0, rot_x)
        else:                 # runs along z, boundary at plan col c, cells rows r..r+length-1
            x0 = c - WALL_T / 2
            add(s_walls, asset, x0, 0, wz(r + length), rot_z)

    # diagonal walls
    for seg in DIAG_WALLS:
        (c0, r0), (c1, r1) = seg[0], seg[1]
        is_door = len(seg) > 2 and seg[2] == "door"
        x0, z0, x1, z1 = c0, wz(r0), c1, wz(r1)
        length = math.hypot(x1 - x0, z1 - z0)
        n = max(1, math.ceil(length - 1e-6))
        ang = math.degrees(math.atan2(z1 - z0, x1 - x0))  # 45 or -45 (mod 180)
        rot = (WALL_ALONG_X_ROT + DIAG_SIGN * ang) % 360
        for i in range(n):
            t = (i + 0.5) / n
            cx, cz = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
            key = "door" if (is_door and i != n // 2) else "wall"
            # tiles rotate about the centre of their (unswapped) footprint at 45 degrees
            add(s_walls, key, cx - 0.5, 0, cz - WALL_T / 2, rot)

    # props
    for key, x, ry, rot in P:
        add(s_props, key, x, PROP_Y, NROWS - ry, rot)

    # ceiling
    for (c, r) in sorted(all_cells):
        add(s_ceil, "ceil", c, CEIL_Y, wz(r + 1), 0)

    # --- write
    os.makedirs(out_dir, exist_ok=True)
    full = Slab()
    for s in (s_floor, s_walls, s_props, s_ceil):
        for u, lst in s.layouts.items():
            for x, y, z, rot in lst:
                full.add(u, x, y, z, rot * 15, s.names.get(u))
    no_ceiling = Slab()
    for s in (s_floor, s_walls, s_props):
        for u, lst in s.layouts.items():
            for x, y, z, rot in lst:
                no_ceiling.add(u, x, y, z, rot * 15, s.names.get(u))
    # Every partial slab gets one anchor floor tile at the common minimum corner, so that all
    # layers line up when pasted at the same cursor position/height. Delete it afterwards.
    (ax, ay, az), _ = full.bounds()
    for s in (s_floor, s_walls, s_props, s_ceil):
        add(s, "floor1", ax, ay, az, 0)
    outputs = {
        "grasshopper_full.slab.txt": full,
        "grasshopper_no_ceiling.slab.txt": no_ceiling,
        "grasshopper_layer1_floor.slab.txt": s_floor,
        "grasshopper_layer2_walls_doors.slab.txt": s_walls,
        "grasshopper_layer3_props.slab.txt": s_props,
        "grasshopper_layer4_ceiling.slab.txt": s_ceil,
    }
    report = []
    for name, slab in outputs.items():
        code = slab.encode()
        with open(os.path.join(out_dir, name), "w") as f:
            f.write(code + "\n")
        report.append((name, len(slab), len(slab.layouts), len(code)))
    for name, n, k, ln in report:
        print(f"{name:45s} assets={n:5d} kinds={k:3d} chars={ln}")
    lo, hi = full.bounds()
    print("bounds", lo, hi)
    return floor, DIAG_CELLS, edges, DIAG_WALLS


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "grasshopper")
    main(os.path.abspath(out))
