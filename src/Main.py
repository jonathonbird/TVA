# import numpy as np
from random import sample

nVoters = 5
nCandidates = 3

candidates = range(nCandidates)

preferences = {}

for voter in range(nVoters):
    preferences[voter] = sample(candidates, len(candidates))
    print("For voter " +str(voter)+ " the preferences are: " +str(preferences[voter]))

