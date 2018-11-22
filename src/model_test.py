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
        expected_outcome = (['A', 'B', 'C', 'D'],
                            15,
                            [([], [], 0, {}),
                             ([], [], 0, {}),
                             ([], [], 0, {}),
                             ([], [], 0, {}),
                             ([], [], 0, {}),
                             (['B', 'D', 'C', 'A'],
                              ['B', 'A', 'C', 'D'],
                              17,
                              {'A': 'This candidate was buried',
                               'B': 'Compromised in favor of this candidate'}),
                             ([], [], 0, {}),
                             ([], [], 0, {}),
                             (['B', 'D', 'A', 'C'],
                              ['B', 'A', 'C', 'D'],
                              17,
                              {'A': 'This candidate was buried',
                               'B': 'Compromised in favor of this candidate'}),
                             ([], [], 0, {})],
                            1.2)

        model = Model(self.preferences, VotingSchemeOption.PLURALITY_VOTING)
        actual_outcome = model.calculate(False)

        self.assertEqual(expected_outcome, actual_outcome)

    def test_calculate_function_returns_proper_output_when_using_borda_voting(self):
        expected_outcome = (['B', 'D', 'A', 'C'],
                            17,
                            [([], [], 0, {}),
                             (['A', 'D', 'C', 'B'],
                              ['D', 'B', 'A', 'C'],
                              17,
                              {'B': 'This candidate was buried',
                               'D': 'Compromised in favor of this candidate'}),
                             (['D', 'A', 'C', 'B'],
                              ['D', 'B', 'A', 'C'],
                              17,
                              {'B': 'This candidate was buried',
                               'D': 'Compromised in favor of this candidate'}),
                             ([], [], 0, {}),
                             (['D', 'C', 'A', 'B'],
                              ['D', 'B', 'A', 'C'],
                              17,
                              {'B': 'This candidate was buried',
                               'D': 'Compromised in favor of this candidate'}),
                             (['D', 'C', 'B', 'A'],
                              ['D', 'B', 'A', 'C'],
                              17,
                              {'B': 'This candidate was buried',
                               'D': 'Compromised in favor of this candidate'}),
                             ([], [], 0, {}),
                             ([], [], 0, {}),
                             (['D', 'A', 'B', 'C'],
                              ['D', 'A', 'B', 'C'],
                              17,
                              {'A': 'Compromised in favor of this candidate',
                               'B': 'This candidate was buried',
                               'D': 'Compromised in favor of this candidate'}),
                             ([], [], 0, {})],
                            1.9)

        model = Model(self.preferences, VotingSchemeOption.BORDA)
        actual_outcome = model.calculate(False)

        self.assertEqual(expected_outcome, actual_outcome)

    def test_calculate_function_returns_only_bullet_voting_when_possible(self):
        BULLET = "There was bulet voting in favor of this candidate"

        nVoters = 10
        nCandidates = 4
        candidates = [chr(i) for i in range(ord('A'), ord('A') + nCandidates)]
        different = 0
        for i in range(10000):
            preferences = {}
            for voter in range(nVoters):
                preferences[voter] = random.sample(candidates, len(candidates))
                # print("For voter", voter, "the preferences are:", preferences[voter])
            model = Model(preferences, random.randint(0, 3))
            actual_output = model.calculate(True)
            for new_preferences, new_final_outcome, new_overall_happiness, changes in actual_output[2]:
                for candidate, message in changes.items():
                    if message != BULLET:
                        different += 1
        self.assertEqual(0, different)
