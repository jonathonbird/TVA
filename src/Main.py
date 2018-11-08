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

vote = VotingScheme(preferences, nCandidates)
# print(vote.plurality_voting())
# print(vote.voting_for_two())
# print(vote.anti_plurality_voting())
vote.borda_voting()
# print('OUTCOME: \n', vote.get_outcome())
print("The overall happiness is", vote.calc_overall_happiness())

