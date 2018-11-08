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

    def calc_happiness(self):

        """
        In this assignment we use the following basic definition of happiness level of voter 𝑖: 𝐻𝑖 = 𝑚 − 𝑗, where 𝑗 – is a
        position of a winning candidate in a true preference list of voter 𝑖. For example, if the true preference list of voter
        𝑖 is {𝐵, 𝐶, 𝐴,𝐷}, and the voting outcome is {𝐴, 𝐶, 𝐵,𝐷}, the happiness level of this voter is 𝐻𝑖 = 1, because the
        winning candidate 𝐴 is at position 𝑗 = 3 in the true preference list.
        """

        happiness = {}

        winner = self.get_outcome()[0]

        for voter, voter_preferences in self.preferences.items():

            happiness[voter] = self.nCandidates - (voter_preferences.index(winner) + 1)
            # print('voter', voter, 'happiness is ', happiness[voter])
        return happiness

    def calc_overall_happiness(self):
        overall = 0
        for happiness in self.calc_happiness().values():
            overall += happiness
        return overall