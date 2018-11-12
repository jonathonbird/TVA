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
#vote.plurality_voting()
#vote.voting_for_two()
#vote.anti_plurality_voting()
#print('OUTCOME: '+ str( vote.get_outcome()))
print("The overall happiness is", vote.calc_overall_happiness())

#print("test-happiness of voter " + str(0) + " are: " + str(vote.calc_happiness_by_preference(vote.preferences[0][0])))
vote.compromisingStrategy(0,[4,3,2,1,0])
