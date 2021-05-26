from django.test import TestCase
from .service import DB
class Test(TestCase):
    def setUp(self) -> None:
        self.database = DB()

    def test(self):
        data = {
            'id': 1,
            'team_one': 'team_one',
            'team_two': 'team_two',
            'date': '2021-05-27 00:00:00',
            'town': 'Rivne'
        }
        self.assertEqual(self.database.match_create(data), None)
        self.assertEqual(len(self.database.match_schedule()), 1)
        self.assertEqual(len(self.database.match_schedule_team('team_one')), 1)
        self.assertEqual(len(self.database.match_id(1)), 5)
        self.assertEqual(self.database.match_delete({'id': 1}), None)
