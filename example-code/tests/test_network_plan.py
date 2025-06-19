import ipaddress
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import network_plan as np


class TestNetworkPlan(unittest.TestCase):
    def test_usable_hosts(self):
        self.assertEqual(np.usable_hosts(27), 30)
        self.assertEqual(np.usable_hosts(24), 254)
        self.assertEqual(np.usable_hosts(30), 2)
        self.assertEqual(np.usable_hosts(31), 0)

    def test_vlan_id_matches_floor_and_room(self):
        self.assertEqual(np.vlan_id(1, 1), 101)
        self.assertEqual(np.vlan_id(2, 6), 206)
        self.assertEqual(np.vlan_id(3, 4), 304)

    def test_vlan_id_rejects_bad_room(self):
        for bad_room in (0, 7, -1):
            with self.assertRaises(ValueError):
                np.vlan_id(1, bad_room)

    def test_room_subnet_capacity_covers_seat_count(self):
        for r in np.build_plan():
            net = ipaddress.ip_network(r.subnet)
            self.assertEqual(net.prefixlen, np.ROOM_SUBNET_PREFIX)
            usable = np.usable_hosts(net.prefixlen)
            self.assertLessEqual(
                r.seats, usable,
                f"floor {r.floor} room {r.room} has {r.seats} seats "
                f"but subnet {r.subnet} only fits {usable}",
            )

    def test_no_overlapping_subnets(self):
        plan = np.build_plan()
        nets = [ipaddress.ip_network(r.subnet) for r in plan]
        nets.append(ipaddress.ip_network(np.SERVER_SUBNET))
        nets.append(ipaddress.ip_network(np.MGMT_SUBNET))
        for i, a in enumerate(nets):
            for b in nets[i + 1:]:
                self.assertFalse(a.overlaps(b), f"{a} overlaps {b}")

    def test_gateway_is_first_usable_address_in_subnet(self):
        for r in np.build_plan():
            net = ipaddress.ip_network(r.subnet)
            first_usable = list(net.hosts())[0]
            self.assertEqual(r.gateway, str(first_usable))

    def test_seats_per_floor_matches_original_room_table(self):
        # From the original "Кількість комп'ютерів в кімнатах" table
        # (Table 1.3 in the source coursework) -- see docs/report.md.
        self.assertEqual(np.seats_per_floor(), {1: 37, 2: 31, 3: 35})

    def test_total_seats(self):
        self.assertEqual(np.total_seats(), 103)


if __name__ == "__main__":
    unittest.main()
