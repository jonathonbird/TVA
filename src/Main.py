# import numpy as np
from random import sample

nVoters = 5
nCandidates = 3

# this is not good, we need candidates to be in the form: {A, B, C, ...}
# candidates = range(nCandidates)
candidates = [chr(i) for i in range(ord('A'), ord('A') + nCandidates)]

preferences = {}

# ouput (giorgos says that maybe this should be in a function, probably he's right
for voter in range(nVoters):
    preferences[voter] = sample(candidates, len(candidates))
    print("For voter " +str(voter)+ " the preferences are: " +str(preferences[voter]))



### implementation of voting schemes

# PLURALITY VOTING
def plurality_voting(preferencesMatrix) :

    for voter in range(nVoters):
        # if preferences[0, voter] work in progress don't mess up plz

preferences = function()