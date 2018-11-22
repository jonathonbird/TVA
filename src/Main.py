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

outcome, overall_happiness, strategic_voting_option, risk = model.calculate(False)

output2 = model.calculate(True)

print()
print("---------------------------------------------------------------------------------------------------------------")
print()
print("Non strategic voting outcome:", outcome)
print()
print("Overall Happiness for non strategic voting outcome:", overall_happiness)
print()
print("Set of strategic voting options, for each voter a tuple (v, O, H, z) where: \n\t"
      "v is the modified preference list.\n\t"
      "O the new outcome after applying v.\n\t"
      "H the new overall happiness level.\n\t"
      "z explanation of why the voter prefers this new outcome.")
print()
voter = 0
for new_preferences, new_final_outcome, new_overall_happiness, changes in strategic_voting_option:
    print("Voter", voter, "\n\tv: ", new_preferences, "\n\tO: ", new_final_outcome,
          "\n\tH: ", new_overall_happiness, "\n\tThe changes are: ", changes)
    voter += 1
print()
print("Overall risk of strategic voting", risk)