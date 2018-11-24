from voting_scheme import VotingScheme
from voting_scheme_option import VotingSchemeOption
import itertools


class Model:
    COMPROMISE = "Compromised in favor of this candidate"
    BURYING = "This candidate was buried"
    BULLET_VOTING = "There was bulet voting in favor of this candidate"

    """
        Voting a Candidate that is easy to beat insincerely high in the first round so that the second round is easy to win
        """

    def __init__(self, preferences, voting_scheme_option):

        self.preferences = preferences
        self.voting_scheme_option = voting_scheme_option

        self.voting_scheme = VotingScheme(preferences, len(preferences[0]))
        self.points_outcome = self.voting_scheme.execute_voting(voting_scheme_option)
        self.outcome = self.voting_scheme.get_outcome()
        self.happiness = self.voting_scheme.calc_happiness(self.outcome)
        self.overall_happiness = self.voting_scheme.calc_overall_happiness(self.outcome)

    """
    Calculates for every voter the possible strategic-voting result
    
    output possibly empty strategic-voting option 
    """

    def calculate(self, bullet_voting_allowed):

        strategic_voting_option = []
        self.n_strategic_options = 0
        for voter in range(len(self.preferences)):
            voter_max_hap = self.voting_scheme.calc_happiness(self.outcome)[voter]
            voter_original_hap = voter_max_hap
            voter_strategic_votes = {}

            candidates = self.preferences[voter]

            if self.voting_scheme_option != VotingSchemeOption.PLURALITY_VOTING and bullet_voting_allowed:
                self.calculate_bullet_voting(candidates, voter, voter_max_hap, voter_strategic_votes,
                                             voter_original_hap)
            elif self.voting_scheme_option == VotingSchemeOption.PLURALITY_VOTING:
                self.calculate_compromising_and_burying_plurality(voter, voter_max_hap, voter_strategic_votes,
                                                                  voter_original_hap)
            else:
                self.calculate_compromising_and_burying(voter, voter_max_hap, voter_strategic_votes, voter_original_hap)

            strategic_voting_option.append(self.evaluate_outcome(voter, voter_strategic_votes))

        risk = self.n_strategic_options / len(self.preferences)

        return self.outcome, self.overall_happiness, strategic_voting_option, risk

    def calculate_compromising_and_burying_plurality(self, voter, voter_max_hap, voter_strategic_votes,
                                                     voter_original_hap):

        for index, candidate in enumerate(self.preferences[voter]):
            new_voter = voter
            new_voter_preferences = self.preferences[voter].copy()

            # Change the preferred voted
            new_voter_preferences[index] = new_voter_preferences[0]
            new_voter_preferences[0] = candidate
            # print("The voter", voter, "was voting for", voter_preferences[0], "and is gonna try to vote for", help)

            new_outcome, new_voting_scheme = self.calculate_new_outcome(new_voter_preferences, voter)

            if new_outcome[0] is self.outcome[0]:
                continue

            new_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome)

            if new_happiness > voter_original_hap:
                self.n_strategic_options += 1

            if new_happiness <= voter_max_hap:
                continue

            voter_max_hap = new_happiness
            voter_strategic_votes[new_voting_scheme] = new_outcome

    def calculate_compromising_and_burying(self, voter, voter_max_hap, voter_strategic_votes, voter_original_hap):
        for new_voter_preference in itertools.permutations(self.preferences[voter]):

            new_voter_preference = list(new_voter_preference)

            new_outcome, new_voting_scheme = self.calculate_new_outcome(new_voter_preference, voter)

            if new_outcome[0] is self.outcome[0]:
                continue

            new_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome)

            if new_happiness > voter_original_hap:
                self.n_strategic_options += 1

            if new_happiness <= voter_max_hap:
                continue

            voter_max_hap = new_happiness
            voter_strategic_votes[new_voting_scheme] = new_outcome

    def calculate_bullet_voting(self, candidates, voter, voter_max_hap, voter_strategic_votes, voter_original_hap):
        # to perform bullet voting as strategic voting we have to generate the preference with only the first one
        for candidate in candidates:

            new_voter_preference = ["" for i in candidates]
            new_voter_preference[0] = candidate

            new_outcome, new_voting_scheme = self.calculate_new_outcome(new_voter_preference, voter)

            if new_outcome[0] is self.outcome[0]:
                continue

            new_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome)

            if new_happiness > voter_original_hap:
                self.n_strategic_options += 1

            if new_happiness <= voter_max_hap:
                continue

            voter_strategic_votes[new_voting_scheme] = new_outcome

    """
    Evaluate the input strategic vote for the input voter and return the kind of strategic vote applied and to which candidate.
    input @voter 
    input @voter_strategic_votes 
    
    output (dict/list/array?) changes
    
    """

    def evaluate_outcome(self, voter, voter_strategic_votes):

        best_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, self.outcome)
        changes = {}

        # for bullet prove change the preference in the array with ""
        # before checking if the position is greater/smaller than the original check if the position is ""
        new_preferences = []
        new_final_outcome = []
        new_overall_happiness = 0

        for new_voting_scheme, new_outcome in voter_strategic_votes.items():

            if self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome) <= best_happiness:
                continue

            best_happiness = self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome)

            changes = {}

            if new_voting_scheme.preferences[voter][1] is "":
                candidate = new_voting_scheme.preferences[voter][0]
                changes[candidate] = self.BULLET_VOTING
                new_preferences = new_voting_scheme.preferences[voter]
                new_final_outcome = new_outcome
                new_overall_happiness = self.voting_scheme.calc_overall_happiness(new_outcome)
                continue

            # Position is the index in the array and candidate the value
            for old_position, candidate in enumerate(self.outcome):

                if new_outcome.index(candidate) < old_position:
                    # Compromising
                    changes[candidate] = self.COMPROMISE
                elif new_outcome.index(candidate) > old_position:
                    # Burying
                    changes[candidate] = self.BURYING

            new_preferences = new_voting_scheme.preferences[voter]
            new_final_outcome = new_outcome
            new_overall_happiness = self.voting_scheme.calc_overall_happiness(new_outcome)

        return new_preferences, new_final_outcome, new_overall_happiness, changes

    def calculate_new_outcome(self, new_voter_preference, voter):

        new_preference = self.preferences.copy()
        new_preference[voter] = new_voter_preference

        new_voting_scheme = VotingScheme(new_preference, len(new_preference[0]))
        new_voting_scheme.execute_voting(self.voting_scheme_option)

        new_outcome = new_voting_scheme.get_outcome()

        return new_outcome, new_voting_scheme
