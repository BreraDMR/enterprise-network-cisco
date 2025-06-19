# Network Implementation Cost Estimate

Generated from [`example-code/cost_calculator.py`](../example-code/cost_calculator.py),
which derives seat counts from [`example-code/network_plan.py`](../example-code/network_plan.py)
(the original per-room table, Table 1.3 in [`docs/report.md`](report.md)).
Regenerate with:

```sh
cd example-code
python3 cost_calculator.py
```

See [`docs/report.md`](report.md) section 3.3 and "Editor's notes" item 1
for why this differs from the original document's cost section (it used 37
seats for floor 2 instead of 31, and had two arithmetic slips).

## Per-seat cost

| Item | Cost (UAH) |
|---|---|
| HP ProDesk 400 G6 PC | 13,902 |
| Samsung LF24T350FHR monitor | 4,000 |
| Royal Kludge R75 keyboard | 1,289 |
| Logitech G Pro X Superlight mouse | 2,500 |
| **Total per seat** | **21,691** |

## Cost by floor

| Floor | Seats | Workstations | Cabling | Access switches | Core equipment | Floor total |
|---|---|---|---|---|---|---|
| 1 | 37 | 802 567 | 7 310 | 7 600 | 163 300 | **980 777** |
| 2 | 31 | 672 421 | 7 650 | 7 600 | 0 | **687 671** |
| 3 | 35 | 759 185 | 7 480 | 7 600 | 0 | **774 265** |
| | | | | | **Grand total** | **2 442 713 UAH** |

Core equipment (floor 1 only, in the server room): router (MikroTik hEX S)
3,300 UAH, core switch (Ubiquiti UniFi Switch 24) 40,000 UAH, server (HPE
ProLiant DL380 Gen10) 120,000 UAH.

Cabling cost is cable run length (as estimated in the original report: 430
m / 450 m / 440 m for floors 1/2/3) times 17 UAH/m. Access-switch cost is
two Cisco CBS110-8T-D units per floor at 3,800 UAH each.

## Original vs. recomputed total

| | Total (UAH) |
|---|---|
| Original document | 2,578,169 |
| Recomputed (this page) | 2,442,713 |
| Difference | -135,456 |

The difference is mostly the floor-2 seat-count correction (31 seats
instead of 37 -- 6 x 21,691 = 130,146 UAH), plus the two small arithmetic
fixes described in `docs/report.md`.
