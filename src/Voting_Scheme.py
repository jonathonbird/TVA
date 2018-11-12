from enum import Enum


class VS(Enum):
    PLURALITY_VOTING = 0
    ANTI_PLURALITY_VOTING = 1
    VOTING_FOR_TWO = 2
    BORDA = 3


class VotingScheme:

    def __init__(self, preferences, n_candidates):
        self.preferences = preferences
        self.voting = {}
        self.nCandidates = n_candidates
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

    """
    Possibly empty set of strategic-voting options S = {Si},i∈n. a strategic-voting option for voter i,
    is a tuple Si = (v,O~,H~,z), where:
    v – is a tactically modified preference list of this voter,
    O~ – a voting outcome resulting from applying v,
    H~ – an overall voter happiness level resulting from applying V,
    z – briefly states why i prefers O~ over O
    (i.e., what the advantage is for i)
    """

    def get_happiness_by_voter(self, voter):
        return self.calc_happiness()[voter]

    def is_happy(self, happiness):
        if happiness == self.nCandidates-1:
            return True
        else:
            return False

    """
    Execute a voting scheme.
    The possible voting_scheme are:
    0 - Plurality voting
    1 - Anti-plurality voting
    2 - Voting for two
    3 - Borda voting
    """

    def execute_voting(self, voting_scheme):
        if voting_scheme is VS.PLURALITY_VOTING:
            return self.plurality_voting()
        elif voting_scheme is VS.ANTI_PLURALITY_VOTING:
            return self.anti_plurality_voting()
        elif voting_scheme is VS.VOTING_FOR_TWO:
            return self.voting_for_two()
        else:
            return self.borda_voting()

    """
    Generate the second round of the voting where only the two more voted candidates are options
    When a second round is executed after applying strategic voting in the first round, the voting for the second round
    will be made with the real preferences
    The only possible voting scheme here is plurality
    """
    def second_round(self, preferences):
        self.preferences = preferences
        first_round = self.get_outcome()
        possible_candidates = [first_round[0], first_round[1]]
        # self.nCandidates = len(possible_candidates)
        new_preference = {}
        for voter, voter_preferences in self.preferences.items():
            for candidate in voter_preferences:
                if candidate in possible_candidates:
                    try:
                        new_preference[voter].append(candidate)
                    except:
                        new_preference[voter] = [candidate]
        # for voter, prefences in new_preference.items():
        #     print("For voter", voter, "the preferences are:", prefences)
        self.preferences = new_preference
        self.plurality_voting()

    def get_opponent(self, pref_candidate):
        for candidate in self.get_outcome()[:2]:
            if candidate != pref_candidate:
                return candidate
