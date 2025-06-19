# Example code

The original coursework (`docs/report.md`) is a technology survey and an
equipment/cost study for a 3-floor office network. It picks a topology
("extended star"), a router, two switch models, a server, and workstations,
and prices them out -- but it never works out an actual VLAN plan, IP
addressing scheme, or device configuration. Everything in this folder was
**written for this GitHub version, after the original coursework was
submitted** -- it is not a transcription of anything that was handed in for
a grade.

## What's here

- [`network_plan.py`](network_plan.py) -- derives a per-room VLAN ID and
  `/27` subnet from the original room-seat-count table.
- [`cost_calculator.py`](cost_calculator.py) -- recomputes the equipment/
  cabling/workstation cost roll-up from the same seat counts and the unit
  prices given in the original report. `docs/cost-estimate.md` is this
  script's output.
- [`cisco-configs/`](cisco-configs/) -- Cisco IOS configuration for a core
  switch, three floor access switches, and an edge router, implementing the
  VLAN plan above (VLAN-per-room, port security on access ports, OSPF
  between the core switch and the router, NAT + a basic inbound ACL on the
  WAN side).
- [`tests/`](tests/) -- unit tests for both scripts.

## Running it

No third-party dependencies -- standard library only.

```sh
cd example-code
python3 -m unittest discover -s tests -v   # 14/14 pass
python3 network_plan.py                    # prints the VLAN/subnet table
python3 cost_calculator.py                 # prints the cost table
```

The `.cfg` files are plain text meant to be read or pasted into a lab
(Packet Tracer / GNS3 / a real IOS device); they are not executable and
nothing here tests them against real or simulated hardware.

## Why Cisco IOS, when the bill of materials isn't Cisco

Of the equipment actually chosen in the original report, none of it is
configured via Cisco IOS CLI:

- **MikroTik hEX S** (router) runs RouterOS, not IOS.
- **Ubiquiti UniFi Switch 24** (core switch) is normally managed through the
  UniFi controller GUI, not a CLI.
- **Cisco CBS110-8T-D** (access switches) is an unmanaged switch in this
  product line -- no CLI or web UI at all, despite the Cisco badge.

The course these configs are written for is taught around Cisco IOS and
Packet Tracer (see the NetAcademy reference in the original bibliography),
which is the skill this example code is meant to demonstrate. So instead of
writing RouterOS/UniFi-GUI instructions that don't show that skill, the
configs below show how the *same* room/VLAN/addressing design would be
implemented if the core switch and router were IOS-capable (e.g. a
Catalyst-class switch and an ISR-class router) -- a reasonable like-for-like
swap, not a rewrite of the design itself.

## Findings from writing these configs

Working out the addressing plan surfaced a hardware sizing problem in the
original BOM that's easy to miss when the report only talks about port
*counts* in the abstract: each floor's plan calls for two Cisco CBS110-8T-D
switches (8 ports each) to serve three rooms apiece, but those rooms have up
to 8 seats each -- e.g. floor 1's first switch would need to fit rooms with
6 + 8 + 7 = 21 workstations onto 7 free ports (one port is the uplink). The
configs in `cisco-configs/` use `interface range` blocks sized to the actual
seat counts rather than to 8-port switches, and `cisco-configs/access-floor*.cfg`
say so explicitly in a comment -- so a reader who copies the VLAN/port-security
pattern onto real, adequately-sized switches gets a working config, but
isn't misled into thinking the original 8-port switch choice was sufficient.
