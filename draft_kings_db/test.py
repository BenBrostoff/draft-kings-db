import unittest
from datetime import date
from draft_kings_db import client


class TestClient(unittest.TestCase):

    def test_initializes(self):
        c = client.DraftKingsHistory()
        c.initialize_nba(
            to_date=date(2018, 2, 23),
            from_date=date(2018, 2, 23)
        )
        davis = c.lookup_nba_performances(name='Anthony Davis')
        self.assertEqual(davis[0].draft_kings_points, 90.25)


if __name__ == '__main__':
    unittest.main()
