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
	"""
	Possibly empty set of strategic-voting options S = {Si},i∈n.
    a strategic-voting option for voter i,is a tuple
     Si = (v,O~,H~,z),
    where,
    v – is a tactically modified preference list of this voter, 
    O~ – a voting outcome resulting from applying v,
    H~ – an overall voter happiness level resulting from applying V,
    z – briefly states why i prefers O~ over O
    (i.e., what the advantage is for i)
    """

    def applySchemeByVotingVector(self, votingVector):
        if votingVector[0] > 1:#borda
            self.borda_voting()
        elif votingVector[1] == 0:# plurality
            self.plurality_voting()
        elif votingVector[2] > 0 : #anty-plural
            self.anti_plurality_voting()
        else:
            self.voting_for_two()

    def get_happiness_by_voter(self,voter):
        happinesses = self.calc_happiness()
        return happinesses[voter]
    def isHappy(self,happiness):
        if happiness == self.nCandidates-1:
            return True
        else:
            return False

    def compromisingStrategy(self,voter,votingVector):
        happinesses = self.calc_happiness()
        print("happinesses of voters are: "+str(happinesses) )
        print("happiness of voter "+str(voter)+" are: "+ str (happinesses[voter]))
        outcome = self.get_outcome()
        print("outcome is: " + str(outcome))
        if self.isHappy(happinesses[voter]) == False:
            v, Ov, Hv, z = self.compromise(voter,happinesses[voter],outcome,votingVector)
            print("best strategy: "+str(v))
            print("new outcome: "+str(Ov))
            print("new overal happiness: "+str(Hv))
            print("z: "+z)




    def compromise(self,voter,happiness,outcome,votingVector):
        favorite = self.preferences[voter][0]
        winner = outcome[0]
        newFavors = {}
        choices = {}
        choiceSchemes = {}

        happinessOfChoices = {}
        winnerPositionOfChoices = {}
        newFavorPositionOfChoices = {}
        choiceIndex = 0
        #find second higher candidate (not my favorite candidate to compromise)
        for i in range(1,len(outcome)):
            temp = outcome[i]
            if temp != favorite:
                newFavors[choiceIndex] = temp

                choices[choiceIndex] = self.preferences[voter].copy()
                v = choices[choiceIndex]
                print("before preference of voter "+str(voter)+" is: " + str(v))
                winnerIndex = v.index(winner)
                newFavorInex = v.index(newFavors[choiceIndex])
                v[winnerIndex], v[newFavorInex] = v[newFavorInex], v[winnerIndex]
                print("after preference of voter "+str(voter)+" is: "+str(v))
                choices[choiceIndex] = v

                # apply strategic voting v
                newPreferences = self.preferences.copy()
                newPreferences[voter] = v
                # print("new preferences are: "+str(newPreferences))
                newScheme = VotingScheme(newPreferences, self.nCandidates)

                # TODO change dynamic voting
                #newScheme.borda_voting()
                #newScheme.plurality_voting()
                #newScheme.voting_for_two()
                #newScheme.anti_plurality_voting()
                newScheme.applySchemeByVotingVector(votingVector)

                newOutcome = newScheme.get_outcome()
                print("new outcome is: " + str(newOutcome))
                happinessOfChoices[choiceIndex] = newScheme.get_happiness_by_voter(voter)#newScheme.calc_happiness_by_preference(favorite)
                winnerPositionOfChoices[choiceIndex] = newOutcome.index(winner)
                newFavorPositionOfChoices[choiceIndex] = newOutcome.index(newFavors[choiceIndex])

                choiceSchemes[choiceIndex] = newScheme
                print("happiness after strategy is: " + str(happinessOfChoices[choiceIndex]))
                choiceIndex+=1

        bestIndex = 0
        bestStrategy ={}
        '''
        #this is for target that my happiness is as much as possible (my prefer is as high as possible)
        maxHappiness = max(happinessOfChoices.values())
        for i,happiness in happinessOfChoices.items():
            if happiness == maxHappiness:
                if len(bestStrategy) == 0 or  winnerPositionOfChoices[i] > winnerPositionOfChoices[bestIndex]:
                    bestStrategy = choices[i]
                    bestIndex = i
        '''
        #this is for target that my alternative gets higher rank, but my prefer is the best in preference
        minFavorPosition = min(newFavorPositionOfChoices.values())
        for i,pos in newFavorPositionOfChoices.items():
            if pos == minFavorPosition:
                if len(bestStrategy) == 0 or happinessOfChoices[i] >happinessOfChoices[bestIndex]:
                    bestStrategy = choices[i]
                    bestIndex = i
        #print("maxHappiness is: " + str(maxHappiness))
        #print("choice list is: " + str(choices))
        #print("happiness list is: "+str(happinessOfChoices))
        #print("winnerPosition list is: "+str(winnerPositionOfChoices))
        #print("secondWinnerPosition list is: "+str(secondWinnerPositionOfChoices))
        #print("best strategy: "+str(bestStrategy))
        print(str(newFavors))

        z = "The voter compromised "+ str(winner) + " in favor of "+str(newFavors.get(bestIndex))+". "
        z += str(newFavors.get(bestIndex))+" took "+ str(newFavorPositionOfChoices[bestIndex]+1)+" place in the modified outcome."
        if happiness < happinessOfChoices[bestIndex]:
            comparison = "increased"
        elif happiness > happinessOfChoices[bestIndex]:
            comparison = "decreased"
        else:
            comparison = "unchanged"
        z += " Happiness of the voter is "+comparison+" from "+ str(happiness)+" to "+ str(happinessOfChoices[bestIndex])

        Ov = choiceSchemes[bestIndex].get_outcome()
        Hv = choiceSchemes[bestIndex].calc_overall_happiness()
        return bestStrategy,Ov,Hv,z

		
    """
    Execute a voting scheme.
    The possible voting_scheme are:
    0 - Plurality voting
    1 - Anti-plurality voting
    2 - Voting for two
    3 - Borda voting
    """

    def execute_voting(self, voting_scheme):
        if voting_scheme is 0:
            return self.plurality_voting()
        elif voting_scheme is 1:
            return self.anti_plurality_voting()
        elif voting_scheme is 2:
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
