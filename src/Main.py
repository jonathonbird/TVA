# import numpy as np
from random import sample

nVoters = 5
nCandidates = 3

candidates = range(nCandidates)

preferences = {}

# ouput (giorgos says that maybe this should be in a function, probably he's right
for voter in range(nVoters):
    preferences[voter] = sample(candidates, len(candidates))
    print("For voter " +str(voter)+ " the preferences are: " +str(preferences[voter]))



### implementation of voting schemes

# PLURALITY VOTING
def plurality_voting() :


preferences = function()