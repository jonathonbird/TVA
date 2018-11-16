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
            voter_strategic_votes = {}
            for new_voter_preference in itertools.permutations(self.preferences[voter]):
                new_voter_preference = list(new_voter_preference)
                new_preference = self.preferences.copy()
                new_preference[voter] = new_voter_preference
                new_voting_scheme = VotingScheme(new_preference, len(new_preference[0]))
                new_voting_scheme.execute_voting(self.vs)

                new_outcome = new_voting_scheme.get_outcome()
                if new_outcome[0] is self.outcome[0]:
                    continue
                new_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome)
                if new_happiness <= voter_hap:
                    continue
                voter_strategic_votes[new_voting_scheme] = new_outcome

                print("For the voter", voter, "The new outcome is", new_outcome, " and the new preference is", new_voter_preference)

            self.evaluate_outcome(voter, voter_strategic_votes)

    def evaluate_outcome(self, voter, voter_strategic_votes):
        best_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, self.outcome)

        for new_voting_scheme, new_outcome in voter_strategic_votes.items():

            if self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome) <= best_happiness:
                continue
            best_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome)
            changes = ""
            # Position is the index in the array and candidate the value
            for old_position, candidate in enumerate(self.outcome):

                if new_outcome.index(candidate) < old_position:
                    # Compromising
                    if len(changes) > 0:
                        changes += ", "
                    changes += "compromised in favor of candidate " + str(candidate)
                elif new_outcome.index(candidate) > old_position:
                    # Burying
                    if len(changes) > 0:
                        changes += ", "
                    changes += "buried the candidate " + str(candidate)
                # else:
                    # nothing
            if len(changes) > 0:
                changes = "Voter " + str(voter) + " " + changes + "."
                print(changes + "voter original happiness was", self.voting_scheme.get_happiness_by_voter(voter), "and now is", self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome))
                a = 1
            # print("The changes with the new preferences", preferences, changes)
            # for candidate, situation in changes_list.items():
            #     print("The candidate", candidate, "was", situation)