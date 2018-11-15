from Voting_Scheme import VotingScheme
import collections
import itertools

class Model:
    """
    Voting a Candidate that is easy to beat insincerely high in the first round so that the second round is easy to win
    """
    def __init__(self, preferences, vs):

        self.preferences = preferences
        self.vs = vs

        self.voting_scheme = VotingScheme(preferences, len(preferences[0]))
        self.points_outcome = self.voting_scheme.execute_voting(vs)
        self.outcome = self.voting_scheme.get_outcome()
        self.happiness = self.voting_scheme.calc_happiness(self.outcome)
        # self.hate = self.calculate_hate()
        # self.hate_list = self.calculate_hated_candidates()
        print("The winning list is", self.outcome)
        self.calculate()
        # self.change_voter_votes_borda(1)

    def calculate(self):
        for voter in range(len(self.preferences)):
            voter_hap = self.voting_scheme.calc_happiness(self.outcome)[voter]
            for new_voter_preference in itertools.permutations(self.preferences[voter]):
                new_voter_preference = list(new_voter_preference)
                new_preference = self.preferences.copy()
                new_preference[voter] = new_voter_preference
                new_voting_scheme = VotingScheme(new_preference, len(new_preference[0]))
                new_voting_scheme.execute_voting(self.vs)

                new_outcome = new_voting_scheme.get_outcome()
                if new_outcome[0] is self.outcome[0]:
                    continue
                new_happiness = new_voting_scheme.get_new_happiness_by_voter(voter, self.outcome)
                if new_happiness <= voter_hap:
                    continue

                print("For the voter", voter, "The new outcome is", new_outcome, " and the new preference is", new_voter_preference)