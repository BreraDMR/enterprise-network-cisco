"""
Addressing/VLAN plan generator for the "enterprise network" coursework design.

This module is example code written for the GitHub portfolio version of the
project. The original coursework (docs/report.md) is a technology survey and
equipment/cost study for a 3-floor, 6-room-per-floor office network -- it
picks hardware (router, switches, server, workstations) and a cabling
topology, but it never works out an actual VLAN or IP addressing scheme.
This script fills that gap: given the seat counts from the original room
table, it derives a per-room VLAN and subnet plan, which is what
example-code/cisco-configs/*.cfg implement and what docs/cost-estimate.md's
device list is cross-checked against.

Scheme:
    - One VLAN per room: VLAN ID = floor * 100 + room (e.g. floor 1, room 3
      -> VLAN 103).
    - One /27 subnet per room: 10.<floor>.<room>.0/27 (30 usable hosts --
      enough for every room's seat count with headroom for printers/APs).
    - VLAN 10, 10.0.1.0/27: servers (the HPE ProLiant lives here).
    - VLAN 1, 10.0.0.0/28: switch/router management.
"""
from __future__ import annotations

from dataclasses import dataclass

ROOMS_PER_FLOOR = 6
SEATS_PER_ROOM_BY_FLOOR = {
    # From the original "Кількість комп'ютерів в кімнатах" table (Table 1.3),
    # which is the most granular source -- see docs/report.md, editor's note
    # in section 3.3 for why this is used instead of the other three
    # mutually-inconsistent totals in the original text.
    1: [6, 8, 7, 5, 6, 5],
    2: [4, 5, 4, 6, 7, 5],
    3: [6, 8, 4, 7, 3, 7],
}

ROOM_SUBNET_PREFIX = 27   # /27 = 30 usable hosts per room
SERVER_SUBNET = "10.0.1.0/27"
SERVER_VLAN = 10
MGMT_SUBNET = "10.0.0.0/28"
MGMT_VLAN = 1


@dataclass(frozen=True)
class RoomPlan:
    floor: int
    room: int
    seats: int
    vlan: int
    subnet: str
    gateway: str


def usable_hosts(prefix_len: int) -> int:
    if not 0 <= prefix_len <= 32:
        raise ValueError(f"invalid prefix length: {prefix_len}")
    if prefix_len >= 31:
        return 0
    return 2 ** (32 - prefix_len) - 2


def vlan_id(floor: int, room: int) -> int:
    if not 1 <= room <= ROOMS_PER_FLOOR:
        raise ValueError(f"room must be 1..{ROOMS_PER_FLOOR}, got {room}")
    return floor * 100 + room


def room_subnet(floor: int, room: int) -> str:
    return f"10.{floor}.{room}.0/{ROOM_SUBNET_PREFIX}"


def room_gateway(floor: int, room: int) -> str:
    # First usable address in the room's /27 is the SVI / gateway on the
    # core switch.
    return f"10.{floor}.{room}.1"


def build_plan() -> list[RoomPlan]:
    plan = []
    for floor, seats_list in SEATS_PER_ROOM_BY_FLOOR.items():
        for room_idx, seats in enumerate(seats_list, start=1):
            plan.append(
                RoomPlan(
                    floor=floor,
                    room=room_idx,
                    seats=seats,
                    vlan=vlan_id(floor, room_idx),
                    subnet=room_subnet(floor, room_idx),
                    gateway=room_gateway(floor, room_idx),
                )
            )
    return plan


def total_seats() -> int:
    return sum(sum(seats) for seats in SEATS_PER_ROOM_BY_FLOOR.values())


def seats_per_floor() -> dict[int, int]:
    return {floor: sum(seats) for floor, seats in SEATS_PER_ROOM_BY_FLOOR.items()}


def render_markdown_table() -> str:
    lines = [
        "| Floor | Room | Seats | VLAN | Subnet | Gateway (SVI) |",
        "|---|---|---|---|---|---|",
    ]
    for r in build_plan():
        lines.append(
            f"| {r.floor} | {r.room} | {r.seats} | {r.vlan} | {r.subnet} | {r.gateway} |"
        )
    lines.append(
        f"| -- | Servers | -- | {SERVER_VLAN} | {SERVER_SUBNET} | 10.0.1.1 |"
    )
    lines.append(
        f"| -- | Management | -- | {MGMT_VLAN} | {MGMT_SUBNET} | 10.0.0.1 |"
    )
    return "\n".join(lines)


if __name__ == "__main__":
    print(render_markdown_table())
    print()
    for floor, seats in seats_per_floor().items():
        print(f"Floor {floor}: {seats} seats")
    print(f"Total: {total_seats()} seats")
