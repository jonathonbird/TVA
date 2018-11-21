import unittest
from Voting_Scheme import VS
from Model import Model


class ModelTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.nVoters = 10
        self.nCandidates = 4
        self.preferences = {
            0: ['B', 'D', 'C', 'A'],
            1: ['A', 'D', 'B', 'C'],
            2: ['A', 'D', 'C', 'B'],
            3: ['A', 'B', 'D', 'C'],
            4: ['C', 'D', 'A', 'B'],
            5: ['D', 'B', 'C', 'A'],
            6: ['B', 'D', 'C', 'A'],
            7: ['B', 'A', 'C', 'D'],
            8: ['D', 'B', 'A', 'C'],
            9: ['C', 'A', 'B', 'D']
        }

    def test_calculate_function_returns_proper_output_when_using_plurality_voting(self):
        expected_outcome = [{},
                            {},
                            {},
                            {},
                            {},
                            {"A": "This candidate was buried",
                             "B": "There was compromised in favor of this candidate"},
                            {},
                            {},
                            {"A": "This candidate was buried",
                             "B": "There was compromised in favor of this candidate"},
                            {}
                            ]

        model = Model(self.preferences, VS.PLURALITY_VOTING)
        actual_outcome = model.calculate()

        self.assertEqual(expected_outcome, actual_outcome)

    def test_calculate_function_returns_proper_output_when_using_borda_voting(self):
        expected_outcome = [{},
                            {'B': 'This candidate was buried',
                             'D': 'There was compromised in favor of this candidate'},
                            {'B': 'This candidate was buried',
                             'D': 'There was compromised in favor of this candidate'},
                            {},
                            {'B': 'This candidate was buried',
                             'D': 'There was compromised in favor of this candidate'},
                            {'B': 'This candidate was buried',
                             'D': 'There was compromised in favor of this candidate'},
                            {},
                            {},
                            {'A': 'There was compromised in favor of this candidate',
                             'B': 'This candidate was buried',
                             'D': 'There was compromised in favor of this candidate'},
                            {}]

        model = Model(self.preferences, VS.BORDA)
        actual_outcome = model.calculate()

        self.assertEqual(expected_outcome, actual_outcome)
