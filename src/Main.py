# import numpy as np
from random import sample
from Voting_Scheme import VotingScheme

nVoters = 5
nCandidates = 5

# this is not good, we need candidates to be in the form: {A, B, C, ...}
# candidates = range(nCandidates)
candidates = [chr(i) for i in range(ord('A'), ord('A') + nCandidates)]
preferences = {}

# Dictionary with the output of the vote
voting = {}

# ouput (giorgos says that maybe this should be in a function, probably he's right
for voter in range(nVoters):
    preferences[voter] = sample(candidates, len(candidates))
    print("For voter " + str(voter) + " the preferences are: " + str(preferences[voter]))


# WiP
def calc_happiness(outcome):

    """
    In this assignment we use the following basic definition of happiness level of voter 𝑖: 𝐻𝑖 = 𝑚 − 𝑗, where 𝑗 – is a
    position of a winning candidate in a true preference list of voter 𝑖. For example, if the true preference list of voter
    𝑖 is {𝐵, 𝐶, 𝐴,𝐷}, and the voting outcome is {𝐴, 𝐶, 𝐵,𝐷}, the happiness level of this voter is 𝐻𝑖 = 1, because the
    winning candidate 𝐴 is at position 𝑗 = 3 in the true preference list.
    """

    happiness = {}

    winner = outcome[0]

    for voter, voter_preferences in preferences.items():

        happiness[voter] = nCandidates - (voter_preferences.index(winner) + 1)
        print('voter', voter, 'happiness is ', happiness[voter])


vote = VotingScheme(preferences, nCandidates)
# print(vote.plurality_voting())
# print(vote.voting_for_two())
# print(vote.anti_plurality_voting())
print(vote.borda_voting())
print('OUTCOME: \n', vote.get_outcome())
print(calc_happiness(vote.get_outcome()))

