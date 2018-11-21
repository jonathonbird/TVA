from voting_scheme import VotingScheme
from voting_scheme import VS


def same_outcomes(old_outcome, new_outcome):
    for i in range(len(old_outcome)):
        if old_outcome[i] != new_outcome[i]:
            return False
    return True


class Burying:

    def __init__(self, voting_scheme, candidates, preferences, voters):
        self.voting_scheme = voting_scheme
        self.candidates = candidates
        self.preferences = preferences
        self.voters = voters

    def get_strategic_voting_ability_for_all_voters(self):
        # Strategic voting ability for each voter
        strategic_voting_ability = []

        # Apply voting scheme
        self.voting_scheme.voting_for_two()

        # Retrieve outcome out of the voting
        outcome = self.voting_scheme.get_outcome()

        # Identify the alternative (second candidate)
        alternative_candidate = outcome[1]

        print("Burying candidate is: %s" % alternative_candidate)

        # Investigate for each voter the options to achieve burying
        for voter in range(self.voters):
            # Get the index of the alternative candidate
            # from the preferences list of this voter
            alternative_candidate_index = self.preferences[voter].index(alternative_candidate)

            # Change the preferences of voter and put the alternative
            # candidate to the bottom of his preferences - Swap
            self.preferences[voter][alternative_candidate_index], self.preferences[voter][self.candidates - 1] = \
                self.preferences[voter][self.candidates - 1], self.preferences[voter][alternative_candidate_index]

            # Perform a new voting procedure with the new preferences
            new_voting_scheme = VotingScheme(self.preferences, self.candidates)
            new_voting_scheme.execute_voting(VS.VOTING_FOR_TWO)
            new_outcome = new_voting_scheme.get_outcome()

            # Did voter changed the outcome with his strategic voting?
            strategic_voting_ability.append(same_outcomes(outcome, new_outcome))

            # Verbosity
            if strategic_voting_ability[-1]:
                print("Voter %d can NOT change the outcome" % voter)
            else:
                print("Voter %d can change the outcome" % voter)

        # Return the list of strategic voting abilities for each voter
        return strategic_voting_ability
