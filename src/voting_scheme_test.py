import unittest
from voting_scheme import VotingScheme


class VotingSchemeShould(unittest.TestCase):

    def setUp(self):
        self.nCandidates = 5
        self.preferences = {0: ['A', 'D', 'E', 'B', 'C'], 1: ['C', 'B', 'E', 'A', 'D'], 2: ['E', 'D', 'A', 'B', 'C'],
                       3: ['C', 'E', 'A', 'D', 'B'], 4: ['E', 'C', 'D', 'A', 'B']}
        self.voting = VotingScheme(self.preferences, self.nCandidates)

    def test_plurality_voting(self):
        expected_outcome = {'A': 1, 'B': 0, 'C': 2, 'D': 0, 'E': 2}

        actual_outcome = self.voting.plurality_voting()

        self.assertEqual(expected_outcome, actual_outcome)

    def test_voting_for_two(self):
        expected_outcome = {'A': 1, 'B': 1, 'C': 3, 'D': 2, 'E': 3}

        actual_outcome = self.voting.voting_for_two()

        self.assertEqual(expected_outcome, actual_outcome)

    def test_anti_plurality_voting(self):
        expected_outcome = {'A': 5, 'B': 3, 'C': 3, 'D': 4, 'E': 5}

        actual_outcome = self.voting.anti_plurality_voting()

        self.assertEqual(expected_outcome, actual_outcome)

    def test_borda_voting(self):
        expected_outcome = {'A': 10, 'B': 5, 'C': 11, 'D': 9, 'E': 15}

        actual_outcome = self.voting.borda_voting()

        self.assertEqual(expected_outcome, actual_outcome)

    def test_get_outcome(self):
        expected_outcome = ['C', 'E', 'A', 'B', 'D']

        self.voting.plurality_voting()
        actual_outcome = self.voting.get_outcome()

        self.assertEqual(expected_outcome, actual_outcome)
