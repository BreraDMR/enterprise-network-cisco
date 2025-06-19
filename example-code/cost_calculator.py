"""
Equipment/cabling cost roll-up for the enterprise network design.

Example code written for the GitHub portfolio version -- see the editor's
note in docs/report.md section 3.3. The original coursework computed this
by hand and the arithmetic doesn't fully reconcile:
    - it uses 37 seats for both floor 1 and floor 2, but the per-room table
      it derives seats from (Table 1.3) actually gives 37 / 31 / 35;
    - 21 691 UAH x 37 seats is written as "801 567", the correct product is
      "802 567";
    - floor 1's equipment subtotal ("178 210") already includes the floor's
      cabling cost, which then gets added a second time in the floor total,
      inflating it by 7 310 UAH.
This script recomputes the same bill of materials with the per-room seat
counts from network_plan.py and plain arithmetic, so the numbers in
docs/cost-estimate.md are checkable by re-running it.
"""
from __future__ import annotations

from dataclasses import dataclass

from network_plan import seats_per_floor

UNIT_PRICES_UAH = {
    "PC (HP ProDesk 400 G6)": 13_902,
    "Monitor (Samsung LF24T350FHR)": 4_000,
    "Keyboard (Royal Kludge R75)": 1_289,
    "Mouse (Logitech G Pro X Superlight)": 2_500,
}

CABLE_PRICE_PER_M_UAH = 17
# Cable run estimates per floor, as given in the original coursework
# (riser + ceiling-height allowance); these are physical-layout estimates,
# independent of the seat-count correction, so they're kept as-is.
CABLE_LENGTH_M = {1: 430, 2: 450, 3: 440}

ACCESS_SWITCH_PRICE_UAH = 3_800       # Cisco CBS110-8T-D, 2 per floor
ACCESS_SWITCHES_PER_FLOOR = 2

# Core equipment lives on floor 1 only.
CORE_EQUIPMENT_UAH = {
    "Router (MikroTik hEX S)": 3_300,
    "Core switch (Ubiquiti UniFi Switch 24)": 40_000,
    "Server (HPE ProLiant DL380 Gen10)": 120_000,
}
CORE_EQUIPMENT_FLOOR = 1


def seat_cost_uah() -> int:
    return sum(UNIT_PRICES_UAH.values())


def access_switch_cost_uah() -> int:
    return ACCESS_SWITCH_PRICE_UAH * ACCESS_SWITCHES_PER_FLOOR


def cabling_cost_uah(floor: int) -> int:
    return CABLE_LENGTH_M[floor] * CABLE_PRICE_PER_M_UAH


def core_equipment_cost_uah() -> int:
    return sum(CORE_EQUIPMENT_UAH.values())


@dataclass(frozen=True)
class FloorCost:
    floor: int
    seats: int
    seats_cost: int
    cabling_cost: int
    switches_cost: int
    core_equipment_cost: int

    @property
    def total(self) -> int:
        return (
            self.seats_cost
            + self.cabling_cost
            + self.switches_cost
            + self.core_equipment_cost
        )


def floor_costs() -> list[FloorCost]:
    per_seat = seat_cost_uah()
    out = []
    for floor, seats in sorted(seats_per_floor().items()):
        out.append(
            FloorCost(
                floor=floor,
                seats=seats,
                seats_cost=seats * per_seat,
                cabling_cost=cabling_cost_uah(floor),
                switches_cost=access_switch_cost_uah(),
                core_equipment_cost=(
                    core_equipment_cost_uah() if floor == CORE_EQUIPMENT_FLOOR else 0
                ),
            )
        )
    return out


def grand_total_uah() -> int:
    return sum(f.total for f in floor_costs())


def render_markdown_table() -> str:
    lines = [
        "| Floor | Seats | Workstations | Cabling | Access switches | Core equipment | Floor total |",
        "|---|---|---|---|---|---|---|",
    ]
    for f in floor_costs():
        lines.append(
            f"| {f.floor} | {f.seats} | {f.seats_cost:,} | {f.cabling_cost:,} | "
            f"{f.switches_cost:,} | {f.core_equipment_cost:,} | **{f.total:,}** |"
        )
    lines.append(
        f"| | | | | | **Grand total** | **{grand_total_uah():,} UAH** |"
    )
    return "\n".join(lines).replace(",", " ")


if __name__ == "__main__":
    print(render_markdown_table())
