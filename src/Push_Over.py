from Voting_Scheme import VotingScheme
import collections

class PushOver:
    """
    Voting a Candidate that is easy to beat insincerely high in the first round so that the second round is easy to win
    The possible voting_scheme are:
    0 - Plurality voting
    1 - Anti-plurality voting
    2 - Voting for two
    3 - Borda voting
    """
    def __init__(self, preferences, voting_scheme):

        self.preferences = preferences
        self.voting_scheme = voting_scheme

        self.vs = VotingScheme(preferences, len(preferences[0]))
        self.outcome = self.vs.execute_voting(voting_scheme)
        self.winner_list = self.vs.get_outcome()
        self.happiness = self.vs.calc_happiness()
        self.hate = self.calculate_hate()
        self.hate_list = self.calculate_hated_candidates()
        self.calculate()

    def calculate(self):
        print("Outcome", self.outcome)
        print("Winner list", self.winner_list)

        # for candidate in self.winner_list:
        #     print("Candidate", candidate, "has", self.outcome[candidate], " votes")
        print("Hated list", self.hate_list)
        for voter, voter_preferences in self.preferences.items():
            # If the preferred candidate of the voter would win without doing anything
            # if voter_preferences[0] is self.winner_list[0] or voter_preferences[0] is self.winner_list[1]:
                # Maybe it is interesting to vote for someone else that other voters
                # do not like so that the second round is easier
                # print()
                # print("Voter", voter, "is very HAPPY")
                # print(self.preferences[voter])
            self.change_voter_votes_plurality(voter)

    """
    In plurality voting only one candidate can be voted and it is therefore the only that should be changed
    """
    def change_voter_votes_plurality(self, voter):
        new_preferences = self.preferences.copy()
        possible_strategy = []
        true_preferred_cand = self.preferences[voter][0]
        opponent = self.vs.get_opponent(true_preferred_cand)
        for candidate in self.hate_list:
            voter_preferences = self.preferences[voter].copy()
            if candidate is voter_preferences[0]:
                # It does not make sense making win someone less hated than the person we would like that wins
                break
            # print()
            # Change the preferred voted
            c_index_v_pref = voter_preferences.index(candidate)
            help = voter_preferences[c_index_v_pref]
            voter_preferences[c_index_v_pref] = true_preferred_cand
            # print("The voter", voter, "was voting for", voter_preferences[0], "and is gonna try to vote for", help)
            voter_preferences[0] = help
            new_preferences[voter] = voter_preferences
            # Create a new voting scheme with the new preferences
            new_vs = VotingScheme(new_preferences, len(new_preferences[0]))
            # Vote a first time with the new preferences
            new_vs.execute_voting(self.voting_scheme)
            first_outcome = new_vs.get_outcome()
            new_opponent = new_vs.get_opponent(true_preferred_cand)
            # If the outcome of applying the voting manipulation is the same one then it is not a good manipulation
            if collections.Counter(first_outcome[:2]) == collections.Counter(self.winner_list[:2]):
                continue
            elif self.hate_list.index(new_opponent) >= self.hate_list.index(opponent):
                continue
            # print("The result of the first round is", help_outcome)  # Vote a first time
            new_vs.second_round(self.preferences)
            second_outcome = new_vs.get_outcome()
            # If after the second round the winner is the desired one then it is an acceptable way of strategic voting
            if new_vs.get_outcome()[0] is self.preferences[voter][0]:
                print("For the voter", voter, "that was voting for", self.preferences[voter][0],"a new possible strategies is voting for", help)
                print("The new outcome in first round would be", first_outcome, "and in the second", new_vs.get_outcome())
                possible_strategy.append(help)
            # If the two first candidates are not the same as previously
            # and the preferred candidate of the voter is still in top 2
        if len(possible_strategy) > 0:
            print("For the voter", voter, "the possible strategies are voting for", possible_strategy)

    def calculate_hate(self):
        hate = {}
        for voter, voter_preferences in self.preferences.items():
            # Since the preferences are order being the most preferred in the position zero and the less liked
            # in the position n, it can also be understood as a measure of not liking or dislike
            for dislike, candidate in enumerate(voter_preferences):
                try:
                    hate[candidate] += dislike
                except:
                    hate[candidate] = dislike
        return hate

    def calculate_hated_candidates(self):
        return sorted(self.hate, key=self.hate.get, reverse=True)
