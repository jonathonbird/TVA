import unittest
from voting_scheme_option import VotingSchemeOption
from Model import Model
import random


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
                             "B": "Compromised in favor of this candidate"},
                            {},
                            {},
                            {"A": "This candidate was buried",
                             "B": "Compromised in favor of this candidate"},
                            {}
                            ]

        model = Model(self.preferences, VotingSchemeOption.PLURALITY_VOTING)
        actual_outcome = model.calculate(False)

        self.assertEqual(expected_outcome, actual_outcome)

    def test_calculate_function_returns_proper_output_when_using_borda_voting(self):
        expected_outcome = [{},
                            {'B': 'This candidate was buried',
                             'D': 'Compromised in favor of this candidate'},
                            {'B': 'This candidate was buried',
                             'D': 'Compromised in favor of this candidate'},
                            {},
                            {'B': 'This candidate was buried',
                             'D': 'Compromised in favor of this candidate'},
                            {'B': 'This candidate was buried',
                             'D': 'Compromised in favor of this candidate'},
                            {},
                            {},
                            {'A': 'Compromised in favor of this candidate',
                             'B': 'This candidate was buried',
                             'D': 'Compromised in favor of this candidate'},
                            {}]

        model = Model(self.preferences, VotingSchemeOption.BORDA)
        actual_outcome = model.calculate(False)

        self.assertEqual(expected_outcome, actual_outcome)

    def test_calculate_function_returns_only_bullet_voting_when_possible(self):
        COMPROMISE = "Compromised in favor of this candidate"
        BURYING = "This candidate was buried"

        nVoters = 10
        nCandidates = 4
        candidates = [chr(i) for i in range(ord('A'), ord('A') + nCandidates)]
        different = 0
        for i in range(100):
            preferences = {}
            for voter in range(nVoters):
                preferences[voter] = random.sample(candidates, len(candidates))
                # print("For voter", voter, "the preferences are:", preferences[voter])
            model = Model(preferences, random.randint(0, 3))
            actualOutput = model.calculate(True)
            for voting_output in actualOutput:
                for candidate, value in voting_output.items():
                    if value == COMPROMISE or value == BURYING:
                        different += 1
        self.assertEqual(0, different)
