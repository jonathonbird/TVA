from random import sample
from Model import Model
from voting_scheme_option import VotingSchemeOption


def get_random_preferences():
    preferences = {}
    for voter in range(int(n_voters)):
        preferences[voter] = sample(candidates, len(candidates))
    return preferences


def ask_for_preferences():
    preferences = {}
    for voter in range(n_voters):
        correct_input = False
        while not correct_input:
            times_ocurred = [0 for i in range(n_candidates)]
            correct_input = True
            question = "Input preferences for voter %s in the form of ABCD: " % voter
            preferences_input_string = input(question).upper()
            preferences[voter] = list(preferences_input_string)

            if len(preferences[voter]) != n_candidates:
                print("Error in the input, the number of candidates is not correct. Expected %d, received %d"
                      % (n_candidates, len(preferences[voter])))
                correct_input = False
                continue

            for preference in preferences[voter]:
                if not candidates.__contains__(preference):
                    print("Error in the input, candidate %s is not in the candidate list." % preference)
                    correct_input = False
                    break
                if times_ocurred[ord(preference) - 65] == 0:
                    times_ocurred[ord(preference) - 65] = 1
                else:
                    print("Error in the input, the candidates %s is present more than once in the preference list."
                          % preference)
                    correct_input = False
                    break

    return preferences


art = """\


  _________      __                         _                                  _    
 |__   __\ \    / /\         /\            (_)                                | |  
    | |   \ \  / /  \       /  \    ___ ___ _  __ _ _ __  _ __ ___   ___ _ __ | |_ 
    | |    \ \/ / /\ \     / /\ \  / __/ __| |/ _` | '_ \| '_ ` _ \ / _ \ '_ \| __|
    | |     \  / ____ \   / ____ \ \__ \__ \ | (_| | | | | | | | | |  __/ | | | |_ 
    |_|      \/_/    \_\ /_/    \_\/___/___/_|\__, |_| |_|_| |_| |_|\___|_| |_|\__|
                                              __/ |    
                                             |___/    
"""
print(art)

error_in_input = True

while error_in_input:
    try:
        n_voters = int(input("Input number of voters: "))
        error_in_input = False
    except ValueError:
        print("The number of voters must be an integer")

error_in_input = True
while error_in_input:
    try:
        n_candidates = int(input("Input number of candidates: "))
        error_in_input = False
    except ValueError:
        print("The number of candidates must be an integer")

candidates = [chr(i) for i in range(ord('A'), ord('A') + n_candidates)]
print("Candidates are: ", candidates)

randomPreferences = input("Do you want to generate random preferences? (y/n): ")

if randomPreferences == "y":
    preferences = get_random_preferences()
else:
    preferences = ask_for_preferences()

[print("For voter %s the preferences are:" % voter, preferences[voter]) for voter in preferences]
print()
print("The possible voting schemes are: ")
print("0 - Plurality voting")
print("1 - Anti-plurality voting")
print("2 - Voting for two")
print("3 - Borda")
voting_scheme_option = int(input("Introduce the number of the voting scheme to apply: "))
model = Model(preferences, voting_scheme_option)

# In plurality voting bullet voting doesn't make sense because only the first preference gets a vote
if voting_scheme_option != 0:
    bullet_voting_allowed = input("Is bullet voting allowed? (y/n): ")
    outcome, overall_happiness, strategic_voting_option, risk = model.calculate(bullet_voting_allowed == "y")
else:
    outcome, overall_happiness, strategic_voting_option, risk = model.calculate(False)

from voting_scheme import VotingScheme as VS
print("The outcome list is:", VS(preferences, n_candidates).execute_voting(voting_scheme_option))

print()
print("---------------------------------------------------------------------------------------------------------------")
print()
print("Non strategic voting outcome:", outcome)
print()
print("Overall Happiness for non strategic voting outcome:", overall_happiness)
print()
print("Set of strategic voting options, for each voter a tuple (v, O, H, z, c) where: \n\t"
      "v = Modified preference list.\n\t"
      "O = the new outcome after applying v.\n\t"
      "H = New overall happiness level.\n\t"
      "z = Explanation of why the voter prefers this new outcome.\n\t"
      "c = Strategic voting schemes applied.")
print()
voter = 0
for new_voter_preferences, new_final_outcome, new_overall_happiness, changes in strategic_voting_option:
    if len(new_voter_preferences) == 0:
        print("Voter", voter, "has an empty set")
        voter += 1
        continue
    else:
        print("Voter", voter)
    print("\tv:", new_voter_preferences)
    print("\tO:", new_final_outcome)
    print("\tH:", new_overall_happiness)
    if len(new_final_outcome) > 0:

        index_of_previous_winner = preferences[voter].index(outcome[0])
        index_of_new_winner = preferences[voter].index(new_final_outcome[0])

        explanation = "Before applying tactical voting, the winner was in position %d " \
                      "of the voter preference list while the new winner is in position %d." \
                      % (index_of_previous_winner, index_of_new_winner)
    else:
        explanation = ""

    print("\tz:", explanation)

    changes_string = ""
    for candidate, change in changes.items():
        if change == Model.COMPROMISE:
            changes_string += "Compromised in favor of candidate %s. " % candidate
        elif change == Model.BURYING:
            changes_string += "Candidate %s was buried. " % candidate
        elif change == Model.BULLET_VOTING:
            changes_string += "Bullet voting in favor of candidate %s. " % candidate

    print("\tc:", changes_string)
    voter += 1


print()
print("Overall risk of strategic voting", risk)
