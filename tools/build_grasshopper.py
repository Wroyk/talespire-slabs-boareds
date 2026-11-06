#!/usr/bin/env python3
"""Build the 'Grasshopper' (Death in Space) deck plan as TaleSpire slabs.

Grid: the deck plan's squares. col = plan column (west -> east), row = plan row (north -> south).
World: x = col, z = NROWS - row  (north is +z), y up.  1 square = 1 TaleSpire unit.

Layers: interior floor/walls/doors/props/details at y=0, interior ceiling at CEIL_Y, a one-cell hull
ring with exterior hull walls around the deck, hull roof plating at ROOF_Y with greebles, a second
hull tier over the mess-hall block, engines at the stern (east) and thrusters on the hull.

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
ROOF_Y = 2.25         # hull plating above the interior ceiling
TIER2_H = 2.0         # height of the superstructure walls on top of the roof
LIGHT_Y = 1.5         # height of corridor light strips on the walls
SIGN_Y = 1.2          # height of wall signs / screens
WALL_INSET = 0.12     # how far wall-mounted props are pushed into the wall (clipping detail)
OFFSET = 2.0          # shift of the whole slab so hull and engines never get negative coordinates

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
    # floors per room type
    "floor_corr": ("88696045-fa1f-416f-b94c-143f7f9ad229", "scifi floor 1x1 panel hard"),
    "floor_ind1": ("8146433f-6b5f-44f2-bc49-35cd0cd47c36", "industrial_floor_1x1_01"),
    "floor_ind2": ("e0eb866d-529f-498e-8e44-c49536060131", "industrial_floor_2x2_01"),
    "floor_rub1": ("acfe07e1-d352-4b77-b9f8-4632adf84c78", "SciFi floor rubber 1x1"),
    "floor_rub2": ("e835a60b-c4bf-4f0c-9a04-cfb7063f3528", "SciFi floor rubber 2x2"),
    "floor_metal": ("a9226e2f-40e5-4a87-92d8-820169c63f74", "scifi floor 1x1 metal plane"),
    "floor_strip": ("5ea4bd5a-8b0b-484b-b5a4-0bca761ae0fd", "stripped floor 1x1"),
    # hull / exterior
    "hullfloor1": ("0f1c53e1-ca89-4776-bdb7-b4acd726fbbf", "Hull01_floor1x1"),
    "hullfloor2": ("73b12504-0f23-4b3f-b814-50db20c004f0", "Hull01_floor2x2"),
    "hullwall": ("1577ee9a-c50d-490c-8604-8b3194e42131", "Hull_Sidewall_center_1x1"),
    "window": ("6a8f68a5-1eb4-4311-b712-49fc6329d0de", "wall window 1x1"),
    "labwindow": ("ab754a73-69ae-4581-99f0-3d3c969ee8e7", "Lab wall with window 1x1"),
    "jet": ("c4958c89-46fd-4b6a-a042-008c1b4ba8d8", "Jet Engine"),
    "jetbase": ("382afc32-0eef-42dd-a125-68c7f012d4f3", "Jet base ext"),
    "thruster": ("e97166a4-0626-4e31-a107-fd869aec2985", "Thruster static"),
    "engine": ("a6a9d645-01bd-4af6-af95-89f1f233df0c", "Engine"),
    "dish": ("c8e3ea9e-81c0-43fa-a324-6e401366b811", "satellite basic floor"),
    "solar": ("2f9540ea-5f97-42b8-8b6f-89df7225070b", "Solar lock panel 2x1"),
    "fan": ("bab4228b-b105-4218-962a-3fcd8ae26d49", "ventilation fan"),
    "ventbox": ("68a549c3-da1e-4f0c-b883-b4ee740681e1", "vent box mini"),
    "ac": ("f82e658b-133e-4d63-a330-6e48096a0cb9", "AC unit"),
    "pipequad": ("a41f298b-6626-44b0-9674-01c3a2964b52", "scifi pipe medial quad horizontal"),
    "pipecorner": ("804fab69-e4e4-4c04-936d-b68ac85d66e9", "scifi pipe medial Corner 01"),
    "support": ("82e3906e-0634-41f9-b803-0d2625d829fd", "caged boxed support horizontal"),
    "supportv": ("ecf7d82a-eebd-4bc8-93a7-f48346b17b7a", "caged heavy support vert"),
    "strip": ("4ae573f6-952d-4895-ba3a-540bb8b8e03c", "support strip 01"),
    "ventlong": ("8545456a-79fb-4d25-b88e-3a4eeed1bd91", "ventilation long"),
    # interior detail
    "lightstrip": ("ac3d33a3-fd88-4bb6-bdbe-b8f5373d4e68", "cyberpunk light strip 01"),
    "walllamp": ("a105ee67-fbf6-45f6-813f-5f8048f7b0f8", "Light wall 01"),
    "pillar": ("f04681fc-6666-4b30-b2cf-5aeb82d9f63c", "scifi wall pillar"),
    "screen": ("e6bb9005-7211-464c-8587-4502dba4c3db", "Screen v1"),
    "screen3": ("d995da3d-9c6b-490a-b454-bd169443283a", "Screen v3"),
    "security": ("90702c6d-3d53-4770-8409-842da063020e", "scifi_Screen security 01"),
    "cam": ("de6bb830-c21c-4062-aebc-17ad3aa1234f", "SecurityCamWallMount"),
    "caution": ("39776e3d-7f4f-4742-bc19-f33470aa6bc7", "sign caution stripes cyber"),
    "signcockpit": ("7b889f35-0f2e-44ff-97a2-55ca198351fc", "sign cockpit"),
    "signmed": ("738ba71b-437b-4315-968d-be89fb1cfbba", "sign medical"),
    "signplanet": ("d73265e5-257c-410d-b729-a0dc22cdc269", "sign planet"),
    "cableceil": ("b521c4dc-116f-4f4e-a361-f4e7ce70a33f", "Cable ceiling v1"),
    "rackweap": ("3b52af64-f7d5-419e-9a25-8cae11a7d899", "rack_weapons_military_01"),
    "vending": ("7033403b-30bf-4802-9e45-ef77e3573dab", "vanding machine pop"),
    "fridge": ("2df8c6fd-78c5-46c5-9c2c-50dceb756305", "refridgerator_01"),
    "counter": ("8851a702-adea-4c5d-9b51-a85515c03d2b", "cabinet_CounterTop_001"),
    "stove": ("7bbd64f8-38f7-4703-9241-7dc935e8374d", "Stove"),
    "ksink": ("fd365f56-dd8f-43ec-a700-c072af7d42ef", "kitchen_sink_001"),
    "surgery": ("eda4fafa-71ef-4628-8f60-e4bdba9a51b1", "Surgery Bed v1"),
    "surglamp": ("349aed42-a69a-45f6-8d20-0a62381461ed", "Surgery lamp"),
    # adventure dressing (Search & Salvage)
    "candle": ("61c18e99-1d7d-4403-9cab-6fe9fdd8d261", "Candle"),
    "candelabra": ("4db44328-9c09-4eaf-91de-90d895e5a5d8", "Candleabra Triple"),
    "curtain": ("defe3e8d-3382-4559-86bf-c04880433118", "Curtain red 01"),
    "spear": ("03d4d3ec-b37b-46c6-93b5-555cfeb2cd77", "hell_spike_spear"),
    "trash1": ("09e79717-0502-4b64-8ee7-7f3e55578b55", "trash pile 01"),
    "trash2": ("5ffacfc9-436f-4ef0-a59c-5593e7d95942", "trash pile 02"),
    "trash3": ("69330e8e-b726-4cae-9d51-cf4d3da4fcf2", "trash pile 03"),
    "trashmess": ("6588b037-56e6-4a4c-b7cd-0f28f25eb66b", "trash mess 01"),
    "trashbag": ("360c119b-d709-45a0-a32b-6f6a8d25f62d", "trashbag"),
    "debris1": ("377c6159-b7f9-4282-9199-fc0b82ab571a", "concrete debris 01"),
    "debris2": ("de8b707e-589e-45d9-a393-9a75de901b2a", "concrete debris 02"),
    "debris3": ("4a63d89b-04a4-4ab8-97f3-12d91b3c911c", "concrete debris 03"),
    "skeleton": ("737d0f69-857d-481f-949a-e8b4930b11ac", "Skeleton 01"),
    "vendbroken": ("31363cf2-ee8c-42fe-aeb1-3ffdef0ee500", "vanding machine pop broken"),
    "grate": ("35678157-d99e-4506-a995-47675862476b", "Road_grate01_1x1"),
    "floor_white": ("dcb2a873-7d92-4759-90d4-8347d9a173c4", "scifi floor 1x1 metal plane white"),
    "glass1": ("e90f68c2-5767-4642-888e-ef705557eeac", "window 1x1 floor"),
    "glass2": ("715d057d-f4a0-4355-8a9f-4f077af488cb", "window 2x2 floor"),
    "jug": ("06992b02-c00a-4d8f-a85a-719736adabc9", "cyberpunk jug 01"),
    "bin": ("79dbb960-dd77-4f8f-b578-7e189e572a56", "item_bin_001"),
    "jerrycan": ("4b292d0c-19b0-4a6a-86c7-9bfd44ab64af", "jerrycan_01"),
    "cardboard": ("f41e9715-d55a-499b-874e-481bf4f36551", "cardboard box"),
    "tripod": ("aa10feae-a8b6-419e-bb25-b2b7accc5415", "Tripod 01"),
    "gun": ("35026064-127b-414e-9a0d-eaaa7fc041b3", "Gun"),
    "shower": ("ca43c33b-c94a-47fd-a241-90baf2aa88b6", "shower residential"),
    "screenthick": ("a959c3a6-a6bf-46c4-ab7f-ba6936e42a04", "scifi_set_Screen thick 01"),
    # shaped exterior (cockpit / hull sets)
    "hullvarA": ("77017a39-cf6a-488d-a409-cc17880b8ada", "HullSideWall"),
    "hullvarB": ("c2f8a532-e9e9-49ce-acd2-51be2ca2f1dc", "HullSideWall"),
    "hullvarC": ("4a650ee6-b97e-4bc5-ae9c-2b2c852a86ab", "HullSideWall"),
    "exttopA": ("3389fc47-8b6b-496a-bda1-dbe67303ec49", "external top 2x2 A"),
    "exttopB": ("ec695e81-4ae5-4c7b-ab22-0a19f4dec132", "external top 2x2 B"),
    "ceilcurved": ("e7f8f9a7-17ae-462a-8b54-597509d2444f", "space ship ceiling 1x1 curved soft"),
    "topsupA": ("4d26e0db-23d2-41ca-8130-701797833599", "exterior 1x1 top support A"),
    "topsupB": ("5d466139-329e-4014-9aba-67dd57e04085", "exterior 1x1 top support B"),
    "lowsupA": ("f94b8d86-02d0-481c-b164-2ffafe1b5e18", "exterior 1x1 lower support A"),
    "lowsupB": ("d8e2fe6d-ab69-441f-979d-5af5e4b303e9", "exterior 1x1 lower support B"),
    "extwallA": ("e8ff11e1-d229-43b7-8f9f-dfad32fc43b2", "external wall 2x2 unique wall A"),
    "cockpitlow": ("d6396479-8783-42c8-97d2-2c87d51a7d03", "cockpit 2x2 inner window lower"),
    "cockpitup": ("8ea5c367-c01f-4f5a-8d4a-50b6c09c0ea3", "Front 2x2 inner window upper"),
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
ROOMS["closet"] = rect(21, 5, 21, 9)            # small airlock strip with two hatches
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
ROOMS["medbay"] = rect(45, 1, 49, 3) | rect(46, 4, 49, 4) | rect(47, 5, 49, 5) | rect(47, 6, 48, 6)
ROOMS["pod_bay"] = rect(46, 22, 48, 29)        # escape-pod bay behind the starboard corridor
ROOMS["machine"] = rect(44, 17, 48, 21) | rect(45, 16, 48, 16) | rect(41, 18, 43, 21) | rect(40, 20, 40, 21)
ROOMS["reactor"] = rect(49, 16, 50, 18) | {(51, 17)}
ROOMS["vestibule"] = rect(29, 20, 29, 21)
ROOMS["cargo"] = rect(30, 18, 38, 23) | rect(39, 20, 39, 21)
ROOMS["cargo_closet"] = rect(39, 18, 40, 19)
ROOMS["lower"] = (rect(39, 22, 45, 23) | rect(36, 24, 45, 25) | rect(37, 26, 45, 26)
                  | rect(38, 27, 45, 27) | rect(38, 28, 44, 28) | rect(38, 29, 43, 29))
ROOMS["hangar"] = (rect(34, 24, 35, 26) | rect(33, 27, 36, 27) | rect(32, 28, 37, 30)
                   | rect(34, 31, 35, 32))
ROOMS["generator"] = rect(44, 30, 48, 30) | rect(44, 31, 47, 31) | rect(44, 32, 46, 32)   # open to the pod bay

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
    (45, 4), (46, 5),                                                # medbay chamfer
    (44, 16), (43, 17),                                              # machine room
    (51, 16), (51, 18),                                              # reactor bulge
    (45, 28), (44, 29), (36, 26), (37, 27),                          # lower room
    (33, 26), (32, 27),                                              # hangar funnel
    (48, 31), (47, 32),                                              # generator room
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
    ((45, 4), (47, 6)),
    ((43, 18), (45, 16)),
    ((51, 16), (52, 17)), ((52, 18), (51, 19)),
    ((36, 26), (38, 28)), ((34, 26), (32, 28)),
    ((47, 33), (49, 31)),
    ((46, 28), (44, 30), "door"),
]

# Explicit walls between two floor cells ('h', col, row) = north edge of cell (col,row) i.e. the
# boundary at plan row `row`; ('v', col, row) = west edge of cell (col,row), boundary at plan col `col`.
PARTITIONS = (
    [("v", 22, r) for r in range(5, 10)]
    + [("h", c, 5) for c in range(22, 26)] + [("v", 27, r) for r in range(6, 10)]
    + [("h", c, 10) for c in range(22, 27)]
    + [("h", 40, 8), ("h", 40, 14)]
    + [("h", 39, 20), ("h", 40, 20), ("v", 39, 18), ("v", 39, 19), ("v", 41, 18)]
    + [("v", 39, 22), ("v", 39, 23), ("h", 39, 22)]
    + [("h", c, 22) for c in (40, 42, 43, 44, 45)]
    + [("h", 36, 24), ("h", 37, 24), ("h", 38, 24), ("v", 36, 24), ("v", 36, 25)]
    + [("v", 46, r) for r in range(22, 28)]                      # pod bay | engine room
)
# wall edges destroyed by the explosion in the medical bay (hull breach / entry point)
# explosion hole in the medical bay: no floor, no ceiling, no roof (the dashed circle on the plan)
HOLE_CELLS = {(47, 4), (48, 4), (47, 5), (48, 5)}
BREACH_EDGES = set()
BREACH_CELLS = set(HOLE_CELLS)                                       # no ceiling / roof above
BREACH_HULL = set()

# Doors: edge -> kind ('door' single, 'door2' half of a double door, 'hatch' airlock/pod hatch)
DOORS = {
    ("v", 7, 7): "hatch", ("v", 9, 7): "hatch", ("v", 7, 14): "hatch", ("v", 9, 14): "hatch",
    ("v", 12, 10): "door2", ("v", 12, 11): "door2",
    ("h", 15, 15): "door2", ("h", 16, 15): "door2",
    ("v", 20, 10): "door2", ("v", 20, 11): "door2",
    ("h", 21, 5): "hatch", ("h", 21, 10): "hatch",
    ("h", 27, 7): "door2", ("h", 28, 7): "door2",
    ("h", 27, 25): "door2", ("h", 28, 25): "door2",
    ("v", 30, 20): "door2", ("v", 30, 21): "door2",
    ("h", 34, 24): "door2", ("h", 35, 24): "door2",
    ("h", 34, 32): "hatch", ("h", 35, 32): "hatch",
    ("v", 40, 20): "door2", ("v", 40, 21): "door2",
    ("v", 41, 19): "door",
    ("h", 39, 8): "door", ("h", 39, 14): "door",
    ("v", 44, 10): "door2", ("v", 44, 11): "door2",
    ("h", 47, 7): "hatch", ("h", 48, 7): "hatch",          # plastic quarantine airlock
    ("h", 24, 5): "door",                                  # observation room
    ("h", 47, 15): "door2", ("h", 48, 15): "door2",
    ("h", 41, 22): "door",
}

# Special floor tiles replacing the standard floor at given cells
SPECIAL_FLOOR = {
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
prop("locker", 18.5, 19.5, FACE["W"])
prop("terminal", 16.0, 18.5, FACE["N"]); prop("seat", 16.0, 17.5, FACE["S"])
for c in (16, 17, 18):
    prop("console_screen", c + 0.5, 21.5, FACE["N"])
prop("console_main", 15.3, 20.7, 135)
prop("pipe2", 17.5, 16.4, 90)
# -- storage / closet
prop("bench", 23.0, 5.5, FACE["S"]); prop("bench", 25.0, 5.5, FACE["S"])
prop("trash1", 23.5, 8.3, 0); prop("trashmess", 25.6, 7.4, 30); prop("trashbag", 22.6, 6.6, 0)
prop("debris1", 24.4, 9.3, 15); prop("trash2", 26.3, 9.2, 0)
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
prop("rubble", 46.2, 12.3, 0); prop("debris1", 47.6, 11.2, 0)
for (x, ry) in [(45.4, 10.2), (46.3, 9.6), (47.2, 10.9), (48.1, 9.3), (48.6, 11.6), (45.6, 12.9), (47.0, 12.2), (49.3, 11.0)]:
    prop("candle", x, ry, 0)
prop("candelabra", 46.5, 11.0, 0)
# -- engine room (lower): the dead engine with EMP spears, candle light, garbage
prop("engine", 41.5, 25.5, 90)
for (x, ry, r) in [(40.6, 25.0, 20), (42.3, 26.2, 300), (41.8, 24.3, 45), (40.9, 26.4, 330)]:
    prop("spear", x, ry, r)
for (x, ry) in [(39.6, 23.4), (43.8, 23.2), (44.5, 26.6), (39.4, 27.4), (42.6, 28.6)]:
    prop("candle", x, ry, 0)
prop("candelabra", 44.3, 24.6, 0); prop("trash2", 39.8, 28.6, 0); prop("cardboard", 44.0, 22.6, 10)
# -- crew quarters: drapes, blood-stained shower, broken vending machine
prop("curtain", 33.0, 9.2, FACE["S"]); prop("curtain", 37.0, 9.2, FACE["S"]); prop("curtain", 35.0, 12.9, FACE["N"])
prop("shower", 40.5, 14.5, FACE["N"])
# -- medical bay (exploded): surgery bed, debris, body in EVA suit floating outside the breach
prop("surgery", 48.0, 2.6, 90); prop("surglamp", 48.0, 2.6, 0); prop("medkit", 46.6, 2.4, 0)
prop("debris2", 46.6, 4.4, 0); prop("debris3", 49.3, 5.6, 30); prop("debris1", 47.2, 6.6, 0); prop("chest", 49.3, 2.4, 40)
prop("debris2", 48.9, 3.5, 70); prop("rubble", 46.4, 5.8, 0)
prop("skeleton", 47.9, 5.1, 60); prop("helm", 48.4, 4.3, 0)      # floating in the hole
# -- boltgun trap at the cargo bay door, computer panel in the vent tunnel
prop("tripod", 34.6, 25.4, FACE["S"])
# -- top-right block
prop("terminal", 45.6, 1.5, 135)
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
prop("cable", 26.6, 25.8, 0); prop("cable", 27.4, 27.2, 90); prop("jug", 26.3, 27.4, 0); prop("jug", 27.7, 25.5, 20)
prop("bin", 26.2, 26.6, 0); prop("jerrycan", 27.6, 26.6, 40); prop("cardboard", 26.8, 28.2, 0)
prop("trash3", 27.3, 26.2, 0); prop("trashbag", 25.9, 25.4, 0)
# -- hangar
prop("bed", 36.6, 27.4, 45)
prop("bench", 32.5, 29.0, FACE["E"]); prop("bench", 37.5, 29.0, FACE["W"])
prop("casemini", 33.8, 30.4, 20); prop("helm", 33.2, 30.7, 0); prop("boots", 34.6, 30.6, 0)
# -- generator room
prop("generator", 46.0, 31.9, 0); prop("pipe2", 44.5, 31.5, 90)
# -- escape pods (outside the starboard corridor)
for r in (22, 24, 26, 28):
    prop("cryo", 48.0, r + 0.5, 270)

# Floor type per room (1x1 key, optional 2x2 key); default is the plain space ship floor
ROOM_FLOOR = {
    "corr_top_w": ("floor_corr", None), "corr_top_e": ("floor_corr", None), "corr_central": ("grate", None),
    "pod_bay": ("floor_metal", None), "medbay": ("floor_white", None),
    "corr_hex_east": ("floor_corr", None),
    "closet": ("floor_corr", None), "bridge_link": ("floor_corr", None), "hex_east": ("floor_corr", None),
    "hex_south": ("floor_corr", None), "vestibule": ("floor_corr", None), "mess_rw_link": ("floor_corr", None),
    "rw_north": ("floor_corr", None), "rw_south": ("floor_corr", None),
    "cargo": ("floor_rub1", "floor_rub2"), "hangar": ("floor_ind1", "floor_ind2"), "cargo_closet": ("floor_rub1", None),
    "storage": ("floor_strip", None), "lower": ("floor_ind1", "floor_ind2"),
    "engineering": ("floor_white", None), "machine": ("floor_rub1", "floor_rub2"),
    "reactor": ("floor_metal", None), "generator": ("floor_metal", None),
    "airlock_n": ("floor_metal", None), "airlock_s": ("floor_metal", None),
    "hydroponics": ("floor_strip", None), "bath_n": ("floor_strip", None), "bath_s": ("floor_strip", None),
}
# corridors: every third cell gets a glowing floor tile, and light strips go on their walls
GLOW_CORRIDORS = ("corr_top_e", "corr_hex_east", "corr_top_w")
LIT_ROOMS = GLOW_CORRIDORS + ("corr_central", "hex_south", "hex_east", "bridge_link",
                              "mess_rw_link", "rw_south", "pod_bay")
# ventilation duct (adventure): a crawl duct on top of the hull from the medbay to the observation
# room, entered through hatches in those rooms' ceilings
DUCT_CELLS = rect(24, 3, 46, 3) | {(24, 4), (24, 5)}
DUCT_HATCHES = {(46, 3), (24, 5)}
# bow: the nose's west wall is the two-part cockpit window front instead of plain window walls
COCKPIT_EDGES = {("v", 1, 10), ("v", 1, 11)}

# Wall edges that become windows instead of plain walls
WINDOW_EDGES = {
    ("v", 1, 10), ("v", 1, 11),                                   # bow
    ("h", 14, 8), ("h", 15, 8), ("h", 16, 8), ("h", 17, 8),       # observation room north
    ("h", 14, 14), ("h", 17, 14),                                 # observation room south
    ("v", 13, 9), ("v", 13, 10), ("v", 13, 11), ("v", 13, 12),    # observation room west
    ("v", 19, 9), ("v", 19, 12),                                  # observation room east
    ("h", 15, 7), ("h", 16, 7),                                   # apse
    ("h", 33, 6), ("h", 34, 6), ("h", 36, 6), ("h", 37, 6),       # bunk alcoves
    ("h", 33, 16), ("h", 34, 16), ("h", 36, 16), ("h", 37, 16),
    ("h", 26, 2), ("h", 27, 2),                                   # corridor arch
    ("v", 25, 25), ("v", 25, 26),                                 # hydroponics (lab window)
    ("h", 47, 1),                                                 # medbay
    ("h", 22, 5), ("h", 23, 5), ("h", 25, 5), ("v", 27, 6), ("v", 27, 7), ("v", 27, 8), ("v", 27, 9),
    ("h", 22, 10), ("h", 23, 10), ("h", 24, 10), ("h", 25, 10), ("h", 26, 10),
    ("v", 22, 5), ("v", 22, 6), ("v", 22, 7), ("v", 22, 8), ("v", 22, 9),   # observation room
    ("v", 51, 10), ("v", 51, 11), ("v", 51, 12),                  # starboard hall
}
LAB_WINDOWS = {("v", 25, 25), ("v", 25, 26)}
DIAG_WINDOWS = {((5, 8), (3, 10)), ((3, 12), (5, 14)), ((14, 8), (13, 9)), ((18, 8), (19, 9)),
                ((13, 13), (14, 14)), ((19, 13), (18, 14))}

# Extra props with explicit height: (key, x, row_y, rot, y)
X = []


def xprop(key, x, ry, rot=0, y=0.0):
    X.append((key, x, ry, rot, y))


# -- engines at the stern (east) and manoeuvring thrusters
for (x, ry) in [(52.3, 17.5), (50.3, 24.5), (50.3, 30.5)]:
    xprop("jetbase", x, ry, FACE["E"]); xprop("jet", x + 1.2, ry, FACE["E"])
xprop("engine", 48.3, 25.5, FACE["E"], ROOF_Y)
for (x, ry, f) in [(35.5, 34.0, "S"), (33.5, 34.0, "S")]:
    xprop("thruster", x, ry, FACE[f], 0.5)
# -- roof greebles (on the hull plating)
for (x, ry) in [(29.0, 6.0), (23.0, 13.0), (41.0, 19.5), (32.0, 27.0), (16.0, 19.0), (6.5, 7.0)]:
    xprop("fan", x, ry, 0, ROOF_Y)
for (x, ry, r) in [(27.5, 14.0, 0), (27.5, 17.0, 0), (27.5, 20.0, 0), (27.5, 23.0, 0),
                   (47.5, 21.0, 0), (47.5, 28.5, 0)]:
    xprop("pipequad", x, ry, r, ROOF_Y)
xprop("pipecorner", 27.5, 11.5, 0, ROOF_Y); xprop("pipecorner", 47.5, 18.5, 90, ROOF_Y)
for (x, ry) in [(22.5, 7.5), (25.0, 7.5), (44.5, 19.5), (46.5, 19.5), (45.0, 24.5), (42.0, 24.5)]:
    xprop("ac", x, ry, FACE["S"], ROOF_Y)
for (x, ry) in [(14.5, 9.0), (17.5, 9.0), (14.5, 12.5), (17.5, 12.5), (36.0, 26.5), (33.0, 30.0)]:
    xprop("ventbox", x, ry, 0, ROOF_Y)
for (x, ry, r) in [(5.0, 9.5, 90), (5.0, 12.5, 90), (9.0, 9.5, 90), (9.0, 12.5, 90)]:
    xprop("ventlong", x, ry, r, ROOF_Y)
xprop("dish", 49.0, 2.5, FACE["E"], ROOF_Y)
for (x, ry, r) in [(12.5, 8.5, 0), (19.5, 8.5, 0), (12.5, 12.5, 0), (19.5, 12.5, 0)]:
    xprop("solar", x, ry, r, ROOF_Y)
xprop("dish", 46.5, 10.5, FACE["N"], ROOF_Y + TIER2_H)
for (x, ry) in [(33.0, 9.0), (36.0, 9.0), (39.0, 9.0), (33.0, 12.5), (36.0, 12.5), (39.0, 12.5)]:
    xprop("solar", x, ry, 90, ROOF_Y + TIER2_H)
for (x, ry, r) in [(21.0, 10.5, 0), (26.0, 10.5, 0), (10.0, 6.5, 90), (10.0, 15.5, 90)]:
    xprop("support", x, ry, r, ROOF_Y)
for (x, ry) in [(13.0, 7.5), (19.0, 7.5), (13.0, 14.5), (19.0, 14.5), (30.5, 16.5), (38.5, 16.5), (30.5, 5.5), (38.5, 5.5)]:
    xprop("supportv", x, ry, 0, ROOF_Y)
for (x, ry, r) in [(2.0, 8.5, 0), (2.0, 13.5, 0), (24.0, 3.0, 90), (34.0, 17.0, 90)]:
    xprop("strip", x, ry, r, ROOF_Y)
# -- wall screens, signs, cameras
xprop("screen", 7.0, 8.1, FACE["S"], SIGN_Y); xprop("screen", 9.0, 8.1, FACE["S"], SIGN_Y)
xprop("screen3", 11.5, 9.9, FACE["S"], SIGN_Y); xprop("signcockpit", 12.5, 9.9, FACE["S"], SIGN_Y + 0.4)
xprop("screen", 32.5, 8.1, FACE["S"], SIGN_Y); xprop("screen3", 38.5, 8.1, FACE["S"], SIGN_Y)
xprop("security", 27.1, 12.5, FACE["E"], SIGN_Y); xprop("security", 28.9, 18.5, FACE["W"], SIGN_Y)
xprop("security", 44.9, 9.5, FACE["E"], SIGN_Y)
xprop("signplanet", 16.0, 7.1, FACE["S"], SIGN_Y + 0.5)
xprop("terminal", 36.5, 3.5, FACE["S"], ROOF_Y)                 # AIKO's panel inside the roof duct
xprop("signmed", 47.5, 6.1, FACE["N"], SIGN_Y + 0.4)
for (x, ry, k) in [(14.1, 16.5, "screen"), (14.1, 17.5, "screen3"), (14.1, 18.5, "screenthick"), (14.1, 19.5, "screen"),
                   (18.9, 16.5, "screen3"), (18.9, 17.5, "screen"), (18.9, 18.5, "screenthick")]:
    xprop(k, x, ry, FACE["E"] if x < 15 else FACE["W"], SIGN_Y)
for (x, ry, f) in [(6.6, 7.0, "E"), (9.4, 7.0, "W"), (6.6, 14.9, "E"), (9.4, 14.9, "W"),
                   (33.9, 31.9, "N"), (35.1, 31.9, "N"), (48.9, 23.5, "W"), (48.9, 27.5, "W")]:
    xprop("caution", x, ry, FACE[f], SIGN_Y)
for (x, ry, f) in [(27.1, 5.5, "E"), (28.9, 9.5, "W"), (29.1, 10.1, "S"), (43.9, 11.5, "W"), (21.1, 10.1, "S"),
                   (46.1, 21.9, "S")]:
    xprop("cam", x, ry, FACE[f], 1.8)
# -- galley corner of the mess hall (west wall), med-bay corner (north-east), weapon racks, cabling
xprop("counter", 31.9, 11.5, FACE["E"]); xprop("ksink", 31.9, 10.5, FACE["E"]); xprop("stove", 31.9, 12.5, FACE["E"])
xprop("fridge", 32.5, 8.4, FACE["S"]); xprop("vendbroken", 38.5, 8.4, FACE["S"])
xprop("gun", 34.6, 25.4, FACE["S"], 0.6)
xprop("rackweap", 46.0, 20.9, FACE["N"])
xprop("cableceil", 27.5, 16.0, 0, CEIL_Y - 0.1); xprop("cableceil", 16.0, 18.5, 90, CEIL_Y - 0.1)
xprop("cableceil", 46.0, 19.0, 0, CEIL_Y - 0.1)
for (x, ry, f) in [(5.5, 11.0, "E"), (10.5, 11.0, "W"), (16.0, 13.9, "N"), (23.5, 9.9, "N"), (36.0, 13.9, "N"),
                   (47.5, 13.9, "N"), (34.5, 23.9, "N"), (47.5, 21.9, "N"), (27.0, 28.9, "N"), (46.0, 32.9, "N")]:
    xprop("walllamp", x, ry, FACE[f], 1.6)

# ----------------------------------------------------------------------------- BUILD


def wz(row):
    """world z of the north edge of plan row `row` (boundary line)."""
    return NROWS - row


def neighbours4(c, r):
    return {("h", c, r): (c, r - 1), ("h", c, r + 1): (c, r + 1),
            ("v", c, r): (c - 1, r), ("v", c + 1, r): (c + 1, r)}


def dilate8(cells):
    out = set()
    for (c, r) in cells:
        for dc in (-1, 0, 1):
            for dr in (-1, 0, 1):
                out.add((c + dc, r + dr))
    return out


def main(out_dir):
    floor = set().union(*ROOMS.values())
    assert not (floor & DIAG_CELLS), floor & DIAG_CELLS
    all_cells = floor | DIAG_CELLS
    cell_room = {cell: name for name, cells in ROOMS.items() for cell in cells}

    # --- walls from floor edges
    edges = {}  # ('h'|'v', col, row) -> kind
    for (c, r) in floor:
        for key, nb in neighbours4(c, r).items():
            if nb not in all_cells:
                edges[key] = "wall"
    for key in PARTITIONS:
        edges[key] = "wall"
    for key, kind in DOORS.items():
        edges[key] = kind
    for key in BREACH_EDGES:
        edges.pop(key, None)

    # --- slabs
    s_floor, s_walls, s_props, s_ceil, s_detail, s_hull = (Slab() for _ in range(6))

    def add(slab, key, x, y, z, rot):
        u, n = A[key]
        slab.add(u, round(x + OFFSET, 2), round(y, 2), round(z + OFFSET, 2), rot, n)

    def plate(slab, cells, y, kind_of, skip=frozenset()):
        """Lay 1x1 / 2x2 tiles over `cells`; kind_of(cell) -> (key1x1, key2x2 or None)."""
        done = set()
        for (c, r) in sorted(cells):
            if (c, r) in done or (c, r) in skip:
                continue
            k1, k2 = kind_of((c, r))
            block = {(c, r), (c + 1, r), (c, r + 1), (c + 1, r + 1)}
            if (k2 and block <= cells and not (block & done) and not (block & skip)
                    and all(kind_of(b) == (k1, k2) for b in block)):
                add(slab, k2, c, y, wz(r + 2), 0)
                done |= block
            else:
                add(slab, k1, c, y, wz(r + 1), 0)
                done.add((c, r))

    # floors: per-room kinds, glow tiles in corridors, special tiles
    glow = {(c, r) for name in GLOW_CORRIDORS for (c, r) in ROOMS[name]
            if (c + r) % 3 == 0 and (c, r) not in SPECIAL_FLOOR}
    plate(s_floor, all_cells, 0, lambda cell: ROOM_FLOOR.get(cell_room.get(cell), ("floor1", "floor2")),
          skip=frozenset(SPECIAL_FLOOR) | glow | HOLE_CELLS)
    for (c, r) in sorted(glow):
        add(s_floor, "floorglow", c, 0, wz(r + 1), 0)
    for (c, r), key in SPECIAL_FLOOR.items():
        add(s_floor, key, c, 0, wz(r + 1), 0)

    # walls / doors / windows along cell edges
    rot_x = WALL_ALONG_X_ROT % 360
    rot_z = (WALL_ALONG_X_ROT + 90) % 360

    def place_edge(slab, asset, axis, c, r, length=1, y=0.0):
        if axis == "h":   # runs along x, boundary at plan row r -> z = wz(r)
            add(slab, asset, c, y, wz(r) - WALL_T / 2, rot_x)
        else:             # runs along z, boundary at plan col c, cells rows r..r+length-1
            add(slab, asset, c - WALL_T / 2, y, wz(r + length), rot_z)

    handled = set(COCKPIT_EDGES)
    place_edge(s_walls, "cockpitlow", "v", 1, 10, length=2)
    place_edge(s_walls, "cockpitup", "v", 1, 10, length=2, y=1.0)
    for (axis, c, r), kind in sorted(edges.items()):
        if (axis, c, r) in handled:
            continue
        asset = {"wall": "wall", "door": "door", "hatch": "hatch", "door2": "door2"}[kind]
        if kind == "wall" and (axis, c, r) in WINDOW_EDGES:
            asset = "labwindow" if (axis, c, r) in LAB_WINDOWS else "window"
        length = 1
        if kind == "door2":  # pair the two halves of a double door
            nxt = (axis, c + 1, r) if axis == "h" else (axis, c, r + 1)
            if edges.get(nxt) == "door2" and nxt not in handled:
                handled.add(nxt)
                length = 2
            else:
                asset = "door"
        place_edge(s_walls, asset, axis, c, r, length)

    # diagonal walls (interior) + matching exterior hull diagonals one cell further out
    for seg in DIAG_WALLS:
        (c0, r0), (c1, r1) = seg[0], seg[1]
        is_door = len(seg) > 2 and seg[2] == "door"
        x0, z0, x1, z1 = c0, wz(r0), c1, wz(r1)
        length = math.hypot(x1 - x0, z1 - z0)
        n = max(1, math.ceil(length - 1e-6))
        ang = math.degrees(math.atan2(z1 - z0, x1 - x0))
        rot = (WALL_ALONG_X_ROT + DIAG_SIGN * ang) % 360
        mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
        nx, nz = -(z1 - z0) / length, (x1 - x0) / length   # normal; flip so it points outward
        probe = (int(math.floor(mx + nx * 0.6)), int(math.floor(NROWS - (mz + nz * 0.6))))
        if probe in floor:
            nx, nz = -nx, -nz
        for i in range(n):
            t = (i + 0.5) / n
            cx, cz = x0 + (x1 - x0) * t, z0 + (z1 - z0) * t
            key = "door" if (is_door and i != n // 2) else "wall"
            if key == "wall" and (seg[0], seg[1]) in DIAG_WINDOWS:
                key = "window"
            add(s_walls, key, cx - 0.5, 0, cz - WALL_T / 2, rot)   # tiles turn about their footprint centre
        if not is_door:
            for i in range(n + 1):
                t = (i + 0.5) / (n + 1) * 1.3 - 0.15
                cx, cz = x0 + (x1 - x0) * t + nx, z0 + (z1 - z0) * t + nz
                add(s_hull, "hullwall", cx - 0.5, 0, cz - WALL_T / 2, rot)

    # corner pillars where two wall lines meet (clipped into the corner)
    pts = {}
    for (axis, c, r) in edges:
        a, b = ((c, r), (c + 1, r)) if axis == "h" else ((c, r), (c, r + 1))
        for p_ in (a, b):
            pts.setdefault(p_, set()).add(axis)
    for (c, r), axes in sorted(pts.items()):
        if len(axes) == 2 and any(nb in floor for nb in ((c, r), (c - 1, r), (c, r - 1), (c - 1, r - 1))):
            add(s_detail, "pillar", c, 0, wz(r), 0)

    # light strips along corridor walls, pushed slightly into the wall
    for name in LIT_ROOMS:
        for (c, r) in sorted(ROOMS[name]):
            if (c + r) % 2:
                continue
            for key, (dx, dz, rot) in {("h", c, r): (0.5, -WALL_INSET, FACE["S"]),
                                       ("h", c, r + 1): (0.5, 1 + WALL_INSET, FACE["N"]),
                                       ("v", c, r): (-WALL_INSET, 0.5, FACE["E"]),
                                       ("v", c + 1, r): (1 + WALL_INSET, 0.5, FACE["W"])}.items():
                if edges.get(key) == "wall":
                    add(s_detail, "lightstrip", c + dx, LIGHT_Y, wz(r + 1) + dz, rot)

    # props
    for key, x, ry, rot in P:
        add(s_props, key, x, PROP_Y, NROWS - ry, rot)
    for key, x, ry, rot, y in X:
        target = s_hull if (y >= ROOF_Y or key in ("jet", "jetbase", "thruster", "engine")) else s_detail
        add(target, key, x, y, NROWS - ry, rot)

    # interior ceiling
    skylight = ROOMS["hex"] | ROOMS["hex_apse"]
    for (c, r) in sorted(all_cells - BREACH_CELLS - DUCT_HATCHES):
        add(s_ceil, "glass1" if (c, r) in skylight else "ceil", c, CEIL_Y, wz(r + 1), 0)

    # --- hull: one ring of cells around every room plus all enclosed voids (found by flooding
    # from outside), exterior hull walls, chamfered corners, solid filling, roof plating.
    shell = dilate8(all_cells)
    outside, stack = set(), [(-2, -2)]
    while stack:
        cell = stack.pop()
        if cell in outside or cell in shell:
            continue
        c, r = cell
        if not (-2 <= c <= NCOLS + 1 and -2 <= r <= NROWS + 1):
            continue
        outside.add(cell)
        stack += [(c + 1, r), (c - 1, r), (c, r + 1), (c, r - 1)]
    hull_cells = {(c, r) for c in range(-1, NCOLS + 1) for r in range(-1, NROWS + 1)} - outside

    # exterior chamfer lines: interior diagonals pushed one cell outward
    ext_lines = []
    for seg in DIAG_WALLS:
        if len(seg) > 2:
            continue
        (c0, r0), (c1, r1) = seg[0], seg[1]
        x0, z0, x1, z1 = c0, wz(r0), c1, wz(r1)
        length = math.hypot(x1 - x0, z1 - z0)
        nx, nz = -(z1 - z0) / length, (x1 - x0) / length
        mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
        probe = (int(math.floor(mx + nx * 0.6)), int(math.floor(NROWS - (mz + nz * 0.6))))
        if probe in floor:
            nx, nz = -nx, -nz
        ext_lines.append(((x0 + nx, z0 + nz), (x1 + nx, z1 + nz), (nx, nz)))

    def beyond(px, pz, margin):
        """distance of a point past an exterior chamfer line (outward side), or None."""
        best = None
        for (ax, az), (bx, bz), (nx, nz) in ext_lines:
            dx, dz = bx - ax, bz - az
            L = math.hypot(dx, dz)
            t = ((px - ax) * dx + (pz - az) * dz) / (L * L)
            if -0.6 / L <= t <= 1 + 0.6 / L:
                d = (px - ax) * nx + (pz - az) * nz
                if d > margin and (best is None or d > best):
                    best = d
        return best

    ring = hull_cells - all_cells
    ring = {(c, r) for (c, r) in ring if beyond(c + 0.5, wz(r + 1) + 0.5, 0.25) is None} - BREACH_HULL
    hull_cells = all_cells | ring
    for (c, r) in sorted(ring):
        for key, nb in neighbours4(c, r).items():
            if nb in hull_cells:
                continue
            axis, ec, er = key
            mx = ec + (0.5 if axis == "h" else 0)
            mz = wz(er) - (0.5 if axis == "v" else 0)
            if beyond(mx, mz, -0.45) is not None:   # covered by the chamfer piece
                continue
            variant = ("hullwall", "hullvarA", "hullwall", "hullvarB", "hullwall", "hullvarC")[(c + 2 * r) % 6]
            place_edge(s_hull, variant, *key)
            # shaped edge pieces: a support rail on top of the hull edge and a skirt at the bottom
            ox, oz = nb[0] - c, -(nb[1] - r)        # outward direction in world x/z
            sup = ("topsupA", "topsupB")[(c + r) % 2]
            low = ("lowsupA", "lowsupB")[(c + r) % 2]
            if axis == "h":
                add(s_hull, sup, c, ROOF_Y, wz(er) - WALL_T / 2 + 0.25 * oz, rot_x)
                add(s_hull, low, c, 0, wz(er) - WALL_T / 2 + 0.5 * oz, rot_x)
            else:
                add(s_hull, sup, ec - WALL_T / 2 + 0.25 * ox, ROOF_Y, wz(er + 1), rot_z)
                add(s_hull, low, ec - WALL_T / 2 + 0.5 * ox, 0, wz(er + 1), rot_z)
        add(s_hull, "hullfloor1", c, 0, wz(r + 1), 0)
        # fill the between-hull space with crossed hull blocks so it reads as solid structure
        add(s_hull, "hullwall", c, 0, wz(r + 1) + 0.5 - WALL_T / 2, rot_x)
        add(s_hull, "hullwall", c + 0.5 - WALL_T / 2, 0, wz(r + 1), rot_z)
    roof_cells = hull_cells - BREACH_CELLS
    curved = {}
    for (c, r) in ring:
        outs = [(nb[0] - c, nb[1] - r) for key, nb in neighbours4(c, r).items() if nb not in hull_cells]
        if len(outs) == 1:
            dc, dr = outs[0]
            curved[(c, r)] = {(0, -1): FACE["N"], (0, 1): FACE["S"], (1, 0): FACE["E"], (-1, 0): FACE["W"]}[(dc, dr)]
    for (c, r), rot in sorted(curved.items()):
        add(s_hull, "ceilcurved", c, ROOF_Y, wz(r + 1), rot)
    plate(s_hull, roof_cells - skylight - DUCT_HATCHES - set(curved), ROOF_Y,
          lambda cell: ("floor1", "exttopA" if (cell[0] // 2 + cell[1] // 2) % 2 == 0 else "exttopB"))
    plate(s_hull, skylight, ROOF_Y, lambda cell: ("glass1", "glass2"))
    for (c, r) in sorted(DUCT_HATCHES):
        add(s_hull, "hatchfloor", c, ROOF_Y, wz(r + 1), 0)
    for (c, r) in sorted(DUCT_CELLS):
        for key, nb in neighbours4(c, r).items():
            if nb not in DUCT_CELLS:
                place_edge(s_hull, "hullwall", *key, y=ROOF_Y)
        if (c + r) % 3 == 0:
            add(s_hull, "lightstrip", c + 0.5, ROOF_Y + LIGHT_Y, wz(r + 1) + 1 + WALL_INSET, FACE["N"])
    plate(s_hull, DUCT_CELLS, ROOF_Y + TIER2_H, lambda cell: ("floor1", "floor2"))

    # --- superstructure (tier 2) over the mess-hall block, with its own hull walls and plating
    core = set().union(*(ROOMS[n] for n in ("mess", "alcove_nw", "alcove_ne", "alcove_sw", "alcove_se",
                                             "bath_n", "bath_s", "mess_rw_link")))
    core |= {(42, 8), (43, 9), (42, 13), (43, 12)}
    tier = dilate8(core)
    for (c, r) in sorted(tier):
        for key, nb in neighbours4(c, r).items():
            if nb not in tier:
                place_edge(s_hull, "hullwall", *key, y=ROOF_Y)
    plate(s_hull, tier, ROOF_Y + TIER2_H, lambda cell: ("hullfloor1", "hullfloor2"))

    # --- write
    os.makedirs(out_dir, exist_ok=True)

    def merge(*slabs):
        m = Slab()
        for s in slabs:
            for u, lst in s.layouts.items():
                for x, y, z, rot in lst:
                    m.add(u, x, y, z, rot * 15, s.names.get(u))
        return m

    full = merge(s_floor, s_walls, s_props, s_detail, s_ceil, s_hull)
    interior = merge(s_floor, s_walls, s_props, s_detail)
    # Every partial slab gets one anchor floor tile at the common minimum corner, so that all
    # layers line up when pasted at the same cursor position/height. Delete it afterwards.
    (ax, ay, az), _ = full.bounds()
    for s in (s_floor, s_walls, s_props, s_detail, s_ceil, s_hull, interior):
        add(s, "floor1", ax - OFFSET, ay, az - OFFSET, 0)
    outputs = {
        "grasshopper_full.slab.txt": full,
        "grasshopper_A_interior.slab.txt": interior,
        "grasshopper_B_ceiling.slab.txt": s_ceil,
        "grasshopper_C_hull_roof_engines.slab.txt": s_hull,
        "grasshopper_layer_floor.slab.txt": s_floor,
        "grasshopper_layer_walls_doors.slab.txt": s_walls,
        "grasshopper_layer_props.slab.txt": s_props,
        "grasshopper_layer_details_lights.slab.txt": s_detail,
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
    return floor, DIAG_CELLS, edges, DIAG_WALLS, ring, tier


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "grasshopper")
    main(os.path.abspath(out))
