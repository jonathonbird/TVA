class VotingScheme:
    # TODO Put comments in every function
    def __init__(self, preferences):
        self.preferences = preferences
        # Dictionary with the output of the vote
        self.voting = {}

    def voting_for_two(self):
        for voter, preference in self.preferences.items():
            self.voting[preference[0]] += 1
            self.voting[preference[1]] += 1

    def plurality_voting(self):
        for voter, preference in self.preferences.items():
            self.voting[preference[0]] += 1

    def anti_plurality_voting(self):
        # print(preferences)
        for voter, preference in self.preferences.items():
            for i, p in enumerate(preference):
                if i is len(preference) - 1:
                    break
                self.voting[p] += 1

    def borda_voting(self):
        for voter, preference in self.preferences.items():
            for i, p in enumerate(preference):
                self.voting[p] += len(preference) - 1 - i

    def get_voting(self):
        return self.voting

