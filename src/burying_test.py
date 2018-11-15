import unittest
from Burying import Burying
from Voting_Scheme import VotingScheme


class BuryingTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.nVoters = 5
        self.nCandidates = 5
        self.preferences = {
            0: ['A', 'D', 'E', 'B', 'C'],
            1: ['C', 'B', 'E', 'A', 'D'],
            2: ['E', 'D', 'A', 'B', 'C'],
            3: ['C', 'E', 'A', 'D', 'B'],
            4: ['C', 'E', 'A', 'B', 'D']
        }

    def test_get_strategic_voting_ability_for_all_voters_should_return_a_list_of_boolean(self):
        expected_strategic_voting_ability = [True, True, False, False, False]

        self.voting = VotingScheme(self.preferences, self.nCandidates)
        self.burying = Burying(self.voting,
                               candidates=self.nCandidates,
                               preferences=self.preferences,
                               voters=self.nVoters)
        actual_strategic_voting_ability = self.burying.get_strategic_voting_ability_for_all_voters()

        self.assertEqual(expected_strategic_voting_ability, actual_strategic_voting_ability)
