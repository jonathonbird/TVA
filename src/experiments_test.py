import unittest
from Model import Model
from voting_scheme import VotingScheme
from voting_scheme_option import VotingSchemeOption


class experimentTest(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_experiment_borda_voting_voter_5(self):
        # Initiate experiment variables
        number_of_candidates = 4
        voting_scheme = VotingSchemeOption.BORDA

        # Preferences Matrix
        preferences = {
            0: ["C", "A", "D", "B"],
            1: ["B", "D", "C", "A"],
            2: ["C", "D", "A", "B"],
            3: ["B", "D", "C", "A"],
            4: ["B", "C", "D", "A"]
        }

        voting = VotingScheme(preferences, number_of_candidates)
        voting.execute_voting(voting_scheme)

        model = Model(preferences, voting_scheme)
        results = model.calculate(False)

        # true outcome should be
        self.assertEqual(["C", "B", "D", "A"], results[0])

        # Voter 5 (index:4) should bury C
        self.assertEqual('This candidate was buried', results[2][4][3]["C"])
        # and the new outcome should be, making B win instead of C
        self.assertEqual(["B", "C", "D", "A"], results[2][4][1])
        # and his new preferences should be
        self.assertEqual(["B", "D", "C", "A"], results[2][4][0])

        # In the slides example the voter actually swapped C and A candidates instead of
        # B, C, D, A he voted B, A, D, C
        # In our software his new preferences where B, D, C, A

        # The overall happiness is reduced
        new_overall_happiness, old_overall_happiness = results[2][4][2], results[1]
        self.assertTrue(new_overall_happiness < old_overall_happiness)

        # Happiness of voter 5 should be increased
        old_happiness_of_5 = voting.get_happiness_by_voter(4)
        new_happiness_of_5 = voting.get_new_happiness_by_voter(4, ["B", "C", "D", "A"])
        self.assertTrue(new_happiness_of_5 > old_happiness_of_5)
