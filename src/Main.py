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


  __  __           _____                    _                                  _     __ 
 |  \/  |   /\    / ____|     /\           (_)                                | |   /_ |
 | \  / |  /  \  | (___      /  \   ___ ___ _  __ _ _ __  _ __ ___   ___ _ __ | |_   | |
 | |\/| | / /\ \  \___ \    / /\ \ / __/ __| |/ _` | '_ \| '_ ` _ \ / _ \ '_ \| __|  | |
 | |  | |/ ____ \ ____) |  / ____ \\__ \__ \ | (_| | | | | | | | | |  __/ | | | |_   | |
 |_|  |_/_/    \_\_____/  /_/    \_\___/___/_|\__, |_| |_|_| |_| |_|\___|_| |_|\__|  |_|
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
output = model.calculate(False)

print(output)
