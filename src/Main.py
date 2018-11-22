from random import sample
from Model import Model
from voting_scheme_option import VotingSchemeOption


def get_random_preferences():
    preferences = {}
    for voter in range(int(nVoters)):
        preferences[voter] = sample(candidates, len(candidates))
    return preferences


def ask_for_preferences():
    preferences = {}
    for voter in range(nVoters):
        question = "Input preferences for voter %s in the form of ABCD: " % voter
        preferences_input_string = input(question).upper()
        preferences[voter] = list(preferences_input_string)
    return preferences


art = """\


  _________      __                        _                                  _     __ 
 |__   __\ \    / /\         /\           (_)                                | |   /_ |
    | |   \ \  / /  \       /  \   ___ ___ _  __ _ _ __  _ __ ___   ___ _ __ | |_   | |
    | |    \ \/ / /\ \     / /\ \ / __/ __| |/ _` | '_ \| '_ ` _ \ / _ \ '_ \| __|  | |
    | |     \  / ____ \   / ____ \\__ \__ \ | (_| | | | | | | | | |  __/ | | | |_   | |
    |_|      \/_/    \_\ /_/    \_\___/___/_|\__, |_| |_|_| |_| |_|\___|_| |_|\__|  |_|
                                              __/ |                                    
                                             |___/                                     
"""
print(art)

nVoters = int(input("Input number of voters: "))
nCandidates = int(input("Input number of candidates: "))

candidates = [chr(i) for i in range(ord('A'), ord('A') + nCandidates)]
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

output2 = model.calculate(True)

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
      "c = Strategic voting schemes applied")
print()
voter = 0
for new_voter_preferences, new_final_outcome, new_overall_happiness, changes in strategic_voting_option:
    print("Voter", voter)
    print("\tv:", new_voter_preferences)
    print("\tO:", new_final_outcome)
    print("\tH:", new_overall_happiness)
    if len(new_final_outcome) > 0:

        index_of_previous_winner = preferences[voter].index(outcome[0])
        index_of_new_winner = preferences[voter].index(new_final_outcome[0])

        explanation = "Before applying tactical voting, the winner was in position %d " \
                      "of the voter preference while the new winner is in position %d." \
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
