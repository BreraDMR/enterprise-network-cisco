import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cost_calculator as cc


class TestCostCalculator(unittest.TestCase):
    def test_seat_cost(self):
        self.assertEqual(cc.seat_cost_uah(), 21_691)

    def test_access_switch_cost(self):
        self.assertEqual(cc.access_switch_cost_uah(), 7_600)

    def test_core_equipment_only_on_floor_1(self):
        costs = {f.floor: f.core_equipment_cost for f in cc.floor_costs()}
        self.assertEqual(costs[1], 163_300)
        self.assertEqual(costs[2], 0)
        self.assertEqual(costs[3], 0)

    def test_floor_totals(self):
        totals = {f.floor: f.total for f in cc.floor_costs()}
        self.assertEqual(totals[1], 980_777)
        self.assertEqual(totals[2], 687_671)
        self.assertEqual(totals[3], 774_265)

    def test_grand_total(self):
        self.assertEqual(cc.grand_total_uah(), 2_442_713)

    def test_floor_total_is_sum_of_its_parts(self):
        for f in cc.floor_costs():
            self.assertEqual(
                f.total,
                f.seats_cost + f.cabling_cost + f.switches_cost + f.core_equipment_cost,
            )


if __name__ == "__main__":
    unittest.main()
