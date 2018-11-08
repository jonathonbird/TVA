class VotingScheme:


    # TODO Put comments in every function
    def __init__(self, preferences, nCandidates):
        self.preferences = preferences
        self.voting = {}
        self.nCandidates = nCandidates
        self.reset_voting()

    def reset_voting(self):
        # Dictionary with the output of the vote
        for candidate in range(ord('A'), ord('A') + self.nCandidates):
            self.voting[chr(candidate)] = 0

    def voting_for_two(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            self.voting[voter_preference[0]] += 1
            self.voting[voter_preference[1]] += 1
        return self.voting

    def plurality_voting(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            self.voting[voter_preference[0]] += 1
        return self.voting

    def anti_plurality_voting(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            for i, p in enumerate(voter_preference):
                if i is len(voter_preference) - 1:
                    break
                self.voting[p] += 1
        return self.voting

    def borda_voting(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            for i, p in enumerate(voter_preference):
                self.voting[p] += len(voter_preference) - 1 - i
        return self.voting

    def get_voting(self):
        return self.voting