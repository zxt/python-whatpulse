import unittest
import urllib2
import socket
import whatpulse

class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.api = whatpulse.API()

    def test_get_user_by_id(self):
        results = self.api.get_user(1)
        self.assertTrue(len(results))

    def test_get_user_by_username(self):
        results = self.api.get_user('smitmartijn')
        self.assertTrue(len(results))

    def test_get_invalid_user_id(self):
        results = self.api.get_user(-1)
        self.assertFalse(len(results))


class TeamTestCase(unittest.TestCase):
    def setUp(self):
        self.api = whatpulse.API()

    def test_get_team_by_id(self):
        results = self.api.get_team(12986)
        self.assertTrue(len(results))

    def test_get_team_by_username(self):
        results = self.api.get_team('Kongregate')
        self.assertTrue(len(results))

    def test_get_invalid_team_id(self):
        results = self.api.get_team(-1)
        self.assertFalse(len(results))

    def test_get_team_including_members(self):
        results_with_members = self.api.get_team(12986, members=True)
        members = results_with_members.get('Members')
        self.assertIsNotNone(members)
        member0 = members.get('Member0')
        self.assertIsNotNone(member0)


class PulsesTestCase(unittest.TestCase):
    def setUp(self):
        self.api = whatpulse.API()

    def test_get_user_pulses(self):
        results = self.api.get_pulses(user=1)
        for r in results.values():
            self.assertEqual(r['Username'], 'smitmartijn')

    def test_get_team_pulses(self):
        team_results = self.api.get_pulses(team=12986)
        for r in team_results.values()[:5]:
            user_results = self.api.get_user(r['UserID'])
            self.assertEqual(user_results['Team']['Name'], 'Kongregate')

    def test_get_pulses_for_user_only_if_request_both_user_and_team(self):
        results1 = self.api.get_pulses(user=1)
        results2 = self.api.get_pulses(user=1, team=12986)
        self.assertDictEqual(results1, results2)

    def test_get_pulses_invalid_user(self):
        results = self.api.get_pulses(user=-123)
        self.assertFalse(len(results))

    def test_get_pulses_invalid_team_should_timeout(self):
        try:
            result = self.api.get_pulses(team=-123)
        except socket.timeout as err:
            pass
        except urllib2.URLError as err:
            if not isinstance(err.reason, socket.timeout):
                self.fail('raised unexpected exception')
        else:
            self.fail('expected timeout exception not thrown')


if __name__ == '__main__':
    unittest.main(verbosity=2)
