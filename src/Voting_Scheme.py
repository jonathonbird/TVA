class VotingScheme:

    def __init__(self, preferences, nCandidates):
        self.preferences = preferences
        self.voting = {}
        self.nCandidates = nCandidates
        self.reset_voting()

    """
    Reset the voting object
    """
    def reset_voting(self):
        # Dictionary with the output of the vote
        for candidate in range(ord('A'), ord('A') + self.nCandidates):
            self.voting[chr(candidate)] = 0

    """    
    Only the first candidate in the preference list gets a vote
    """
    def plurality_voting(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            self.voting[voter_preference[0]] += 1
        return self.voting

    """    
    Only two first candidates in the preference list get a vote
    """
    def voting_for_two(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            self.voting[voter_preference[0]] += 1
            self.voting[voter_preference[1]] += 1
        return self.voting

    """
    All the candidates in the preference list get a vote except the last one    
    """
    def anti_plurality_voting(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            for i, p in enumerate(voter_preference):
                if i is len(voter_preference) - 1:
                    break
                self.voting[p] += 1
        return self.voting

    """    
    If there are N candidates, the first in the preference list gets N points, the second N - 1, etc
    """
    def borda_voting(self):
        self.reset_voting()
        for voter, voter_preference in self.preferences.items():
            for i, p in enumerate(voter_preference):
                self.voting[p] += len(voter_preference) - 1 - i
        return self.voting

    """
    Get the result of the voting
    """
    def get_outcome(self):
        return sorted(self.voting, key=self.voting.get, reverse=True)
