from voting_scheme import VotingScheme
from voting_scheme_option import VotingSchemeOption
import itertools

COMPROMISE = "Compromised in favor of this candidate"
BURYING = "This candidate was buried"
BULLET_VOTING = "There was bulet voting in favor of this candidate"


class Model:
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
        # self.hate = self.calculate_hate()
        # self.hate_list = self.calculate_hated_candidates()
        # print("The winning list is", self.outcome)

        # print(self.calculate())
        # self.change_voter_votes_borda(1)

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
                self.calculate_bullet_voting(candidates, voter, voter_max_hap, voter_strategic_votes, voter_original_hap)
            else:
                self.calculate_compromising_and_burying(voter, voter_max_hap, voter_strategic_votes, voter_original_hap)

            strategic_voting_option.append(self.evaluate_outcome(voter, voter_strategic_votes))

        risk = self.n_strategic_options / len(self.preferences)

        return self.outcome, self.overall_happiness, strategic_voting_option, risk

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

            # print("For the voter", voter, "The new outcome is", new_outcome, " and the new preference is",
            #       new_voter_preference)

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
                changes[candidate] = BULLET_VOTING
                # print(changes, "voter original happiness was", self.voting_scheme.get_happiness_by_voter(voter),
                #       "and now is", self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome))
                continue

            # Position is the index in the array and candidate the value
            for old_position, candidate in enumerate(self.outcome):

                if new_outcome.index(candidate) < old_position:
                    # Compromising
                    changes[candidate] = COMPROMISE
                elif new_outcome.index(candidate) > old_position:
                    # Burying
                    changes[candidate] = BURYING

            new_preferences = new_voting_scheme.preferences[voter]
            new_final_outcome = new_outcome
            new_overall_happiness = self.voting_scheme.calc_overall_happiness(new_outcome)

            # if len(changes) > 0:
            #     changes = "Voter " + str(voter) + " " + changes + "."
            #     print(changes + "voter original happiness was", self.voting_scheme.get_happiness_by_voter(voter), "and now is", self.voting_scheme.get_new_happiness_by_voter(voter, new_outcome))
            #     a = 1
            # print("The changes with the new preferences", preferences, changes)
            # for candidate, situation in changes_list.items():
            #     print("The candidate", candidate, "was", situation)

        return new_preferences, new_final_outcome, new_overall_happiness, changes

    def calculate_new_outcome(self, new_voter_preference, voter):

        new_preference = self.preferences.copy()
        new_preference[voter] = new_voter_preference

        new_voting_scheme = VotingScheme(new_preference, len(new_preference[0]))
        new_voting_scheme.execute_voting(self.voting_scheme_option)

        new_outcome = new_voting_scheme.get_outcome()

        return new_outcome, new_voting_scheme
