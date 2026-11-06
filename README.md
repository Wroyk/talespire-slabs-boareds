# TaleSpire Slabs & Boards

## Grasshopper – begehbares Raumschiff (Death in Space Deckplan)

Die **Grasshopper** aus *Death in Space* (Vorlagen: Deckplan `Grasshopper-PrinterFriendly-A3.pdf` und das Abenteuer „Search and Salvage“) als komplettes,
begehbares Raumschiff für TaleSpire: 1 Planquadrat = 1 TaleSpire-Einheit, 53 × 36 Felder Innenraum, dazu Hülle,
Dach, Aufbauten und Triebwerke. Alles ist in Ebenen aufgeteilt, sodass man mit TaleSpires Höhen-Clipping
(Hide Volumes / Clipping-Ebene für GM und Spieler) durch Dach und Decke in die Räume schneiden kann.

![Layout](grasshopper/grasshopper_layout.png)

*Blau = Innenraum, grau = Hülle, rot = Wände, grün = Türen, lila = Luken, gelb = Diagonalzellen, orange = Aufbauten
auf dem Dach und Umriss des zweiten Hüllenstockwerks, Kreise = Props, grüne Kästchen = Wand-Details.*

### Räume nach dem Abenteuer „Search and Salvage“

| Nr. | Abenteuer | Umsetzung im Slab |
|---|---|---|
| 0 | Airlock | Hangar-Trichter mit Bodenluftschleuse, Boltgun-Falle (Gewehr auf Stativ) an der Frachtraumtür |
| 1 | Small Cargo Bay | Frachtraum mit Gummiboden, Kisten, Containern, Glasscherben, Vorraum zum Hauptkorridor |
| 2 | Engine Room | Großer Maschinenraum mit totem Triebwerk, vier EMP-Speeren darin, Kerzen, Müll; Reaktornische mit Rohren |
| 3 | Cryopod Room | Steuerbord-Halle mit vier Kryokapseln, Dutzende Kerzen, Trümmer |
| 4 | Medical Bay | Krankenstation mit OP-Tisch und Trümmern; der gestrichelte Kreis des Plans ist das **Explosionsloch**: dort fehlen Boden, Decke und Dach, die Leiche im EVA-Anzug schwebt im Loch; Plastik-Quarantäneschleuse zum Kryoraum |
| – | Ventilation Tunnel | **Nicht auf dem Deckplan:** Lüftungskanal als geschlossener Kasten **auf dem Dach** des oberen Korridors, von der Krankenstation bis über den Beobachtungsraum; Einstieg durch Luken in der Decke beider Räume, Computerpanel (AIKO) und Lichtleisten im Kanal |
| 5 | Crew Quarters | Messe mit Konferenztisch, Kombüse, vier Kojen-Nischen, Vorhänge, Bodenluke, zwei Bäder (Dusche), kaputter Automat |
| 6 | Main Corridor | Zentralkorridor mit Metallgitterboden, Lichtleisten, Kameras, Schotttüren |
| 7 | Maintenance Shaft | Verschlossener Raum am Südende des Korridors: Kabelstränge, Kanister, Tonnen, Kartons, Müll |
| 8 | Empty Observation Room | Raum neben dem oberen Korridor, rundum Fensterwände, Müll und Trümmer, eigene Tür; daneben der schmale Schleusenstreifen mit zwei Luken |
| 9 | Tactical Stations | Runder Raum mit Sechskanttisch, Stühlen, Apsis-Konsole, **Glasdecke** und Solarpaneelen daneben auf dem Dach |
| 10 | Computer Room | Weißer Raum mit schrägen Ecken, Bildschirme an den Wänden, Konsolenreihe, Hauptkonsole |
| 11 | Commander Bridge | Brücke mit Bug-Pilotenstation, zwei Konsolenbänken, Holo-Tisch, Luftschleusen |
| – | Rettungskapsel-Bucht | Raum an der Steuerbord-Außenwand mit vier Kapseln (Luke zum Raum hin), offen zum Maschinen- und Generatorraum, Diagonal-Luke vom großen Maschinenraum |

### Aufbau

- **Innenraum (y = 0):** Böden nach Raumtyp, Wände, Türen, Fenster, Möbel, Lichtleisten, Säulen, Schilder, Kameras.
- **Decke (y = 2.0):** Schiffsdecke, über dem Taktikraum Glas, über der Krankenstation offen.
- **Hülle (y = 0 bis 2.25):** Genau ein Zellring um die echten Räume (die Flächen, die im Plan mit schwarzen
  Plus-Zeichen markiert sind, bleiben Außenraum), gebaut aus derselben Raumschiff-Wand wie innen, an jeder Schräge
  45°-Stücke statt Treppen; der Ring selbst ist mit gekreuzten Wandstücken massiv gefüllt.
- **Dach:** flache Schiffsplatten, Glas über dem Taktikraum, Loch über der Explosion in der Krankenstation,
  Lüftungskanal als Kasten obenauf.
- **Dachaufbauten (y = 2.25):** Lüfter, Rohrleitungen, Klimageräte, Luftauslässe, Träger, Antenne, Solarpaneele.
- **Zweites Hüllenstockwerk (y = 2.25 bis 4.25):** Aufbau über dem Crew-Quartier mit Antenne und Solarpaneelen.
- **Antrieb:** Drei Triebwerke mit Sockeln an der Heckwand (Osten), Haupttriebwerk auf dem Dach der Kapsel-Bucht, zwei Bremsdüsen am Hangar.

### Dateien

| Datei | Inhalt | Assets |
|---|---|---|
| `grasshopper/grasshopper_full.slab.txt` | **Alles in einem** | 3324 |
| `grasshopper/grasshopper_A_interior.slab.txt` | Boden, Wände, Türen, Fenster, Props, Details, Lichter | 1202 |
| `grasshopper/grasshopper_B_ceiling.slab.txt` | Decke (y = 2.0), Glasdecke Taktikraum | 601 |
| `grasshopper/grasshopper_C_hull_roof_engines.slab.txt` | Hülle, Dachplatten, Aufbauten, 2. Stockwerk, Triebwerke | 1524 |
| `grasshopper/grasshopper_layer_floor.slab.txt` | nur Boden | 366 |
| `grasshopper/grasshopper_layer_walls_doors.slab.txt` | nur Wände, Türen, Fenster, Luken | 441 |
| `grasshopper/grasshopper_layer_props.slab.txt` | nur Möbel | 157 |
| `grasshopper/grasshopper_layer_details_lights.slab.txt` | nur Lichtleisten, Säulen, Schilder, Bildschirme | 241 |

Der volle Slab ist rund 14 KB komprimiert, TaleSpire erlaubt 30 KB.

### Einfügen in TaleSpire

1. Den kompletten Inhalt einer `.slab.txt` kopieren (die ``` am Anfang und Ende dürfen mit).
2. In TaleSpire im Baumodus **Strg+V**, Slab platzieren, bestätigen.
3. Entweder `grasshopper_full` in einem Stück, oder nacheinander **A → B → C an derselben Cursorposition und
   Höhe**. Jeder Teil-Slab enthält eine „Anker“-Bodenkachel an der gemeinsamen Südwest-Ecke (links unten außerhalb
   des Schiffs), damit alle Ebenen exakt übereinander landen. Die Ankerkachel danach löschen.
4. Spielen: Clipping-Höhe auf knapp unter 2.0 setzen, dann sieht man von oben in die Räume; auf 4.5 für das ganze
   Schiff von außen.

### Annahmen und Stellschrauben

Die Slabs wurden ohne laufendes TaleSpire erzeugt. Das Binärformat ist gegen den offiziellen Referenz-Slab von
Bouncyrock byteidentisch geprüft, die Asset-IDs stammen aus TaleSpires eigener `index.json`. Nicht prüfbar waren die
genauen Modellmaße einzelner Assets. Dafür gibt es im Generator `tools/build_grasshopper.py` einen `CONFIG`-Block:

| Parameter | Bedeutung | Wenn in TaleSpire … |
|---|---|---|
| `WALL_T = 0.5` | angenommene Dicke der Wandkacheln; Wände sitzen mittig auf den Wandlinien des Plans | … Wände um bis zu 0.25 neben der Bodenkante stehen → 0.25 oder 1.0 |
| `WALL_ALONG_X_ROT = 0` | Drehung, bei der eine Wandkachel in x-Richtung verläuft | … alle Wände um 90° verdreht sind → 90 |
| `DIAG_SIGN = -1` | Drehrichtung der 45°-Stücke | … Diagonalwände spiegelverkehrt liegen → +1 |
| `CEIL_Y = 2.0`, `ROOF_Y = 2.25`, `TIER2_H = 2.0` | Höhen von Decke, Dach und Aufbau | … Decke schwebt oder in Wänden steckt → anpassen |
| `LIGHT_Y`, `SIGN_Y`, `WALL_INSET` | Höhe und Einschub der Wand-Details | … Lichtleisten zu hoch/tief oder vor der Wand → anpassen |
| `PROP_Y = 0.0` | Höhe der Props über dem Bodenursprung | … Props im Boden versinken → 0.25 |
| `FACE` | welche Drehung „Blickrichtung“ ist | … Stühle vom Tisch wegschauen → Werte um 180 drehen |

Neu bauen:

```bash
python3 tools/build_grasshopper.py
python3 tools/render_preview.py grasshopper/grasshopper_layout.png
```

Das Layout (Räume als Zellmengen, Diagonalwände, Türen, Fenster, Props, Dachaufbauten) steht in
`tools/build_grasshopper.py`; `tools/slab_encoder.py` ist ein eigenständiger Encoder/Decoder für Slab-Format v2.

### Verwendete TaleSpire-Assets

| Schlüssel | Asset | UUID |
|---|---|---|
| `floor1` | space ship floor 1x1 | `36147fe1-3850-4662-a95e-1a56be8a14b4` |
| `floor2` | space ship floor 2x2 | `f095ea12-0e41-4a79-bf3b-9fa0b4400369` |
| `floorglow` | scifi floor glow 1x1 | `bd4507ba-85ba-4748-9142-b4857a8d8f89` |
| `hatchfloor` | space ship hatch horizontal 01 | `d58e27d0-3a41-4cb7-b6c8-c389ca16360b` |
| `wall` | space ship wall 1x1 basic | `09f8bec6-263d-4e96-bef5-eba63f27a114` |
| `door` | space ship door 1x1 | `f56d891a-ed49-4e6e-910e-81827e8eac37` |
| `door2` | space ship door double | `ae40e42f-2a00-4b99-97e1-c3d41baadc27` |
| `hatch` | space ship hatch Vertical 01 | `cac3888c-f04b-4da9-b0b3-db6e2d4b7b75` |
| `ceil` | space ship ceiling 1x1 | `c6619e55-11f4-4a20-b790-8970917c23ab` |
| `console` | sci fi console_  mid | `e9e64ec2-f473-46da-8267-107eaee37495` |
| `console_main` | Interstellar Console main | `a4857731-d982-4c81-95fa-50791b404b68` |
| `console_screen` | Interstellar Console base w screen | `52d56d1a-772a-47d9-97be-9c8f824f3e6f` |
| `terminal` | sci fi terminal | `9c4c8b19-379f-4c9e-9add-5bca941e0def` |
| `holotable` | Interstellar travel ON_OFF mech | `6e5804b7-381e-42b6-ae8d-3f2923025cab` |
| `pilot` | scifi chair pilot | `c928a5e6-c479-47d7-984c-4254f8780338` |
| `chair` | Interstellar chair | `9d4ea828-db15-48fc-8ebe-65734ed4c722` |
| `seat` | scifi seat terminal | `db61b415-d7bb-41bb-bfd1-d3fc2404c7e9` |
| `table` | scifi_table 01 A | `fd24e8e2-b4d4-4627-8573-4d06980db53e` |
| `conftable` | ConferenceTable_Office | `224d71a4-136f-431d-ae57-803d2de31a77` |
| `bed` | unit bed | `6e2c7f4e-c1f0-41a9-9e7b-24ec6076ec8b` |
| `cryo` | Cryo sleep lux | `3a5512c2-c266-44fc-8ba2-bf4e805745b0` |
| `locker` | Locker v1 | `e5446734-1eec-45f0-9aff-7cdddf6a459e` |
| `locker2` | Locker v2 | `4abd32cc-01b3-43ba-a748-222f8449c85d` |
| `bench` | bench locker large | `fe2fa079-9bba-4b07-a008-0c1ef85531c3` |
| `benchs` | bench locker small | `532dea3c-26df-48f7-9b8d-29fc1271db87` |
| `crate` | sci fi crate L 01 | `da125361-6adc-4d02-9805-bebf22dc340f` |
| `chest` | sci fi chest 02 | `84d38667-a961-4562-93b4-ec38aeb81c55` |
| `case` | case of supplies 01 | `abf5a41b-606e-4aa9-87ba-5964dbda73f8` |
| `casemini` | case of supplies 01 mini B | `721fea1e-ca6e-4b00-b32e-178883774c23` |
| `casemini2` | case of supplies 02 mini A | `6fe3a290-76ba-4f37-a484-77a520310643` |
| `cable` | Cable floor v1 | `26bc0db4-0c94-46ef-a64f-71e4b5a9a996` |
| `rubble` | Rubble pebbles spread out | `ac288dec-372b-4c7a-b70f-3a48115920ab` |
| `plant1` | Jungle plant 01 | `8fcd4b46-c6f3-4d50-b950-ef4557ffe7b4` |
| `plant2` | Jungle plant 02 | `ec794aa6-27da-4e8e-a122-4042a27f2c3f` |
| `pitcher` | Pitcher plant | `6e5af318-1737-4bf3-a35f-a3530f6fd2de` |
| `bucket` | grass bucket v1 | `0e3f8516-9ef8-46c2-a0f3-f9584c294c9f` |
| `toilet` | toilette residential | `d857a8c6-15b1-4102-8470-275574e8b2bc` |
| `sink` | sink residential | `6dd89e0f-27f6-45f8-85ff-799dc03d1e67` |
| `reactor` | Interstellar battery mech | `f3439bf0-9619-43fa-b516-768945d72a36` |
| `cooler` | battery cooler with battery | `1c380641-1d35-4bd2-9c31-51593cf83179` |
| `generator` | Interstellar egg mech | `3becaf94-92d4-425e-b870-8ce345a453a4` |
| `pipe` | machine pipe 01 | `4da1b40b-f0cf-44eb-8e38-aa742f21a0b8` |
| `pipe2` | scifi pipe medial 01 | `eb23f5c6-8646-4374-8505-aaecf8faaaa4` |
| `helm` | Astronaut helm | `c8250950-a9f6-4d74-986c-3943cc39d6d4` |
| `boots` | Astronaut boots | `28a6c1fd-edc2-4a71-8ca1-06e783da6c0e` |
| `medkit` | medkit chest 01 | `a341f6d2-f769-41b4-8afc-e9f9eecd0768` |
| `lamp` | Lamp Small | `bfc0bcfa-3df5-4890-9654-6138c27b6e13` |
| `wallcase` | wall case 01 | `d7c23080-3aa2-42bc-8e0a-392b406990b8` |
| `floor_corr` | scifi floor 1x1 panel hard | `88696045-fa1f-416f-b94c-143f7f9ad229` |
| `floor_ind1` | industrial_floor_1x1_01 | `8146433f-6b5f-44f2-bc49-35cd0cd47c36` |
| `floor_ind2` | industrial_floor_2x2_01 | `e0eb866d-529f-498e-8e44-c49536060131` |
| `floor_rub1` | SciFi floor rubber 1x1 | `acfe07e1-d352-4b77-b9f8-4632adf84c78` |
| `floor_rub2` | SciFi floor rubber 2x2 | `e835a60b-c4bf-4f0c-9a04-cfb7063f3528` |
| `floor_metal` | scifi floor 1x1 metal plane | `a9226e2f-40e5-4a87-92d8-820169c63f74` |
| `floor_strip` | stripped floor 1x1 | `5ea4bd5a-8b0b-484b-b5a4-0bca761ae0fd` |
| `hullfloor1` | Hull01_floor1x1 | `0f1c53e1-ca89-4776-bdb7-b4acd726fbbf` |
| `hullfloor2` | Hull01_floor2x2 | `73b12504-0f23-4b3f-b814-50db20c004f0` |
| `hullwall` | space ship wall 1x1 basic | `09f8bec6-263d-4e96-bef5-eba63f27a114` |
| `window` | wall window 1x1 | `6a8f68a5-1eb4-4311-b712-49fc6329d0de` |
| `labwindow` | Lab wall with window 1x1 | `ab754a73-69ae-4581-99f0-3d3c969ee8e7` |
| `jet` | Jet Engine | `c4958c89-46fd-4b6a-a042-008c1b4ba8d8` |
| `jetbase` | Jet base ext | `382afc32-0eef-42dd-a125-68c7f012d4f3` |
| `thruster` | Thruster static | `e97166a4-0626-4e31-a107-fd869aec2985` |
| `engine` | Engine | `a6a9d645-01bd-4af6-af95-89f1f233df0c` |
| `dish` | satellite basic floor | `c8e3ea9e-81c0-43fa-a324-6e401366b811` |
| `solar` | Solar lock panel 2x1 | `2f9540ea-5f97-42b8-8b6f-89df7225070b` |
| `fan` | ventilation fan | `bab4228b-b105-4218-962a-3fcd8ae26d49` |
| `ventbox` | vent box mini | `68a549c3-da1e-4f0c-b883-b4ee740681e1` |
| `ac` | AC unit | `f82e658b-133e-4d63-a330-6e48096a0cb9` |
| `pipequad` | scifi pipe medial quad horizontal | `a41f298b-6626-44b0-9674-01c3a2964b52` |
| `pipecorner` | scifi pipe medial Corner 01 | `804fab69-e4e4-4c04-936d-b68ac85d66e9` |
| `support` | caged boxed support horizontal | `82e3906e-0634-41f9-b803-0d2625d829fd` |
| `supportv` | caged heavy support vert | `ecf7d82a-eebd-4bc8-93a7-f48346b17b7a` |
| `strip` | support strip 01 | `4ae573f6-952d-4895-ba3a-540bb8b8e03c` |
| `ventlong` | ventilation long | `8545456a-79fb-4d25-b88e-3a4eeed1bd91` |
| `lightstrip` | cyberpunk light strip 01 | `ac3d33a3-fd88-4bb6-bdbe-b8f5373d4e68` |
| `walllamp` | Light wall 01 | `a105ee67-fbf6-45f6-813f-5f8048f7b0f8` |
| `pillar` | scifi wall pillar | `f04681fc-6666-4b30-b2cf-5aeb82d9f63c` |
| `screen` | Screen v1 | `e6bb9005-7211-464c-8587-4502dba4c3db` |
| `screen3` | Screen v3 | `d995da3d-9c6b-490a-b454-bd169443283a` |
| `security` | scifi_Screen security 01 | `90702c6d-3d53-4770-8409-842da063020e` |
| `cam` | SecurityCamWallMount | `de6bb830-c21c-4062-aebc-17ad3aa1234f` |
| `caution` | sign caution stripes cyber | `39776e3d-7f4f-4742-bc19-f33470aa6bc7` |
| `signcockpit` | sign cockpit | `7b889f35-0f2e-44ff-97a2-55ca198351fc` |
| `signmed` | sign medical | `738ba71b-437b-4315-968d-be89fb1cfbba` |
| `signplanet` | sign planet | `d73265e5-257c-410d-b729-a0dc22cdc269` |
| `cableceil` | Cable ceiling v1 | `b521c4dc-116f-4f4e-a361-f4e7ce70a33f` |
| `rackweap` | rack_weapons_military_01 | `3b52af64-f7d5-419e-9a25-8cae11a7d899` |
| `vending` | vanding machine pop | `7033403b-30bf-4802-9e45-ef77e3573dab` |
| `fridge` | refridgerator_01 | `2df8c6fd-78c5-46c5-9c2c-50dceb756305` |
| `counter` | cabinet_CounterTop_001 | `8851a702-adea-4c5d-9b51-a85515c03d2b` |
| `stove` | Stove | `7bbd64f8-38f7-4703-9241-7dc935e8374d` |
| `ksink` | kitchen_sink_001 | `fd365f56-dd8f-43ec-a700-c072af7d42ef` |
| `surgery` | Surgery Bed v1 | `eda4fafa-71ef-4628-8f60-e4bdba9a51b1` |
| `surglamp` | Surgery lamp | `349aed42-a69a-45f6-8d20-0a62381461ed` |
| `candle` | Candle | `61c18e99-1d7d-4403-9cab-6fe9fdd8d261` |
| `candelabra` | Candleabra Triple | `4db44328-9c09-4eaf-91de-90d895e5a5d8` |
| `curtain` | Curtain red 01 | `defe3e8d-3382-4559-86bf-c04880433118` |
| `spear` | hell_spike_spear | `03d4d3ec-b37b-46c6-93b5-555cfeb2cd77` |
| `trash1` | trash pile 01 | `09e79717-0502-4b64-8ee7-7f3e55578b55` |
| `trash2` | trash pile 02 | `5ffacfc9-436f-4ef0-a59c-5593e7d95942` |
| `trash3` | trash pile 03 | `69330e8e-b726-4cae-9d51-cf4d3da4fcf2` |
| `trashmess` | trash mess 01 | `6588b037-56e6-4a4c-b7cd-0f28f25eb66b` |
| `trashbag` | trashbag | `360c119b-d709-45a0-a32b-6f6a8d25f62d` |
| `debris1` | concrete debris 01 | `377c6159-b7f9-4282-9199-fc0b82ab571a` |
| `debris2` | concrete debris 02 | `de8b707e-589e-45d9-a393-9a75de901b2a` |
| `debris3` | concrete debris 03 | `4a63d89b-04a4-4ab8-97f3-12d91b3c911c` |
| `skeleton` | Skeleton 01 | `737d0f69-857d-481f-949a-e8b4930b11ac` |
| `vendbroken` | vanding machine pop broken | `31363cf2-ee8c-42fe-aeb1-3ffdef0ee500` |
| `grate` | Road_grate01_1x1 | `35678157-d99e-4506-a995-47675862476b` |
| `floor_white` | scifi floor 1x1 metal plane white | `dcb2a873-7d92-4759-90d4-8347d9a173c4` |
| `glass1` | window 1x1 floor | `e90f68c2-5767-4642-888e-ef705557eeac` |
| `glass2` | window 2x2 floor | `715d057d-f4a0-4355-8a9f-4f077af488cb` |
| `jug` | cyberpunk jug 01 | `06992b02-c00a-4d8f-a85a-719736adabc9` |
| `bin` | item_bin_001 | `79dbb960-dd77-4f8f-b578-7e189e572a56` |
| `jerrycan` | jerrycan_01 | `4b292d0c-19b0-4a6a-86c7-9bfd44ab64af` |
| `cardboard` | cardboard box | `f41e9715-d55a-499b-874e-481bf4f36551` |
| `tripod` | Tripod 01 | `aa10feae-a8b6-419e-bb25-b2b7accc5415` |
| `gun` | Gun | `35026064-127b-414e-9a0d-eaaa7fc041b3` |
| `shower` | shower residential | `ca43c33b-c94a-47fd-a241-90baf2aa88b6` |
| `screenthick` | scifi_set_Screen thick 01 | `a959c3a6-a6bf-46c4-ab7f-ba6936e42a04` |

---

## English summary

The Death in Space **Grasshopper** as a complete walkable TaleSpire ship: interior deck (floors by room type,
walls, doors, windows, furniture, light strips, pillars, signs), interior ceiling, a closed hull ring with exterior
hull walls, roof plating with greebles, a second hull tier over the mess hall, stern engines and thrusters.
Paste `grasshopper/grasshopper_full.slab.txt`, or the A/B/C slabs at the same cursor position (each carries one anchor
tile at the shared minimum corner, delete it afterwards). The generator `tools/build_grasshopper.py` holds the layout
and a `CONFIG` block for the conventions that could not be verified without a running game.
