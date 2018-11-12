from Voting_Scheme import VotingScheme
"""
    Voting a Candidate with the hope this candidate can get elected 
    The possible voting_scheme are:
    0 - Plurality voting
    1 - Anti-plurality voting
    2 - Voting for two
    3 - Borda voting
    
    Step1: exchange position of an alternative(not my first prefer) and hater
    Step2: save new favor information
    Step3: repeat Step1 until it has no alternative
    Step4: choose what strategy v which has an alternative ranked at the highest position (min position)
        Step 4.1: If there are more than one strategy, choose what strategy makes voter more happy than others
    Step5: return v,O,H,z
    """
class Compromise:

    def __init__(self, preferences, voting_scheme):

        self.preferences = preferences
        self.voting_scheme = voting_scheme
        self.vs = VotingScheme(preferences, len(preferences[0]))
        self.vs.execute_voting(voting_scheme)

        happinesses = self.vs.calc_happiness()
        outcome = self.vs.get_outcome()
        #it is for only 1 voter
        print("outcome: "+str(outcome))
        print("(sincerely rank)voter 0 has happiness is "+str(happinesses[0]))

        '''
        #it is for all voters
        for voter, voter_preferences in self.preferences.items():
            v, Ov, Hv, z = self.compromise(voter,happinesses[voter],outcome,voting_scheme)
            print("best strategy: " + str(v))
            print("new outcome: " + str(Ov))
            print("new overal happiness: " + str(Hv))
            print("z: " + z)
        '''
        v, Ov, Hv, z = self.compromise(0, happinesses[0], outcome, voting_scheme)
        print("best strategy: " + str(v))
        print("new outcome: " + str(Ov))
        print("new overal happiness: " + str(Hv))
        print("z: " + z)

    def compromise(self,voter,happiness,outcome,voting_scheme):
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

                choices[choiceIndex] = self.preferences[voter][:]
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
                newScheme = VotingScheme(newPreferences, len(self.preferences[0]))

                # TODO change dynamic voting
                newScheme.execute_voting(voting_scheme)

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
                if len(bestStrategy) == 0 or happinessOfChoices[i] > happinessOfChoices[bestIndex]:
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
