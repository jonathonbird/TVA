import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from random import sample
from Model import Model
import numpy as np

# The + 1 is because when using range the last value is not used
# Therefore, range (2,4) would give only 2 and 3 when we also want the 4
maximum_n_voters = 10 + 1
minimum_n_voters = 2

maximum_n_candidates = 10 + 1
minimum_n_candidates = 2

number_of_times_execute = 200

history = np.zeros((maximum_n_voters, maximum_n_candidates))


def get_random_preferences(n_voters, candidates):
    preferences = {}
    for voter in range(int(n_voters)):
        preferences[voter] = sample(candidates, len(candidates))
    return preferences


def calculate_risks(voting_scheme_option):
    for n_voters in range(minimum_n_voters, maximum_n_voters):
        for n_candidates in range(minimum_n_candidates, maximum_n_candidates):
            candidates = [chr(i) for i in range(ord('A'), ord('A') + n_candidates)]

            preferences = get_random_preferences(n_voters, candidates)
            # print(preferences)
            model = Model(preferences, voting_scheme_option)
            outcome, overall_happiness, strategic_voting_option, risk = model.calculate(False)
            # print("Number of voters is", n_voters, "and number of candidates is", n_candidates, "the risk is", risk)
            history[n_voters, n_candidates] = max(risk, history[n_voters, n_candidates])
            # max(risk, history[n_voters, n_candidates])
            # print(history)


def calculate_average_risk(voting_scheme_option):
    print()
    print("Apply voting scheme:", voting_scheme_option)
    for n in range(number_of_times_execute):
        calculate_risks(voting_scheme_option)
        print("Iteration", n, "finished")


def create_plot(voting_scheme_option):
    for n_voters in range(minimum_n_voters, maximum_n_voters):
        risk_to_represented = history[n_voters]
        plt.plot(range(len(risk_to_represented)), risk_to_represented, label=(str(n_voters) + " Voters"))

    plt.xlabel("Number of candidates")
    plt.ylabel("Maximum number of strategic options")
    # if voting_scheme_option == 0:
    #     plt.title("Applied plurality voting")
    # elif voting_scheme_option == 1:
    #     plt.title("Applied anti-plurality voting")
    # elif voting_scheme_option == 2:
    #     plt.title("Applied voting for 2")
    # else:
    #     plt.title("Applied Borda")
    plt.legend()
    plt.figure()

    for n_candidates in range(minimum_n_candidates, maximum_n_candidates):
        risk_to_represented = history[:, n_candidates]
        plt.plot(range(len(risk_to_represented)), risk_to_represented, label=(str(n_candidates) + " Candidates"))
    plt.xlabel("Number of voters")
    plt.ylabel("Maximum number of strategic options")
    # plt.title("Effect of increasing the number of voters in the risk")
    # if voting_scheme_option == 0:
    #     plt.title("Applied plurality voting")
    # elif voting_scheme_option == 1:
    #     plt.title("Applied anti-plurality voting")
    # elif voting_scheme_option == 2:
    #     plt.title("Applied voting for 2")
    # else:
    #     plt.title("Applied Borda")

    plt.legend()
    plt.figure()


for option in range(1):
    calculate_average_risk(option)
    create_plot(option)
    history = np.zeros((maximum_n_voters, maximum_n_candidates))

print("Shape of history", history.shape)
print("Number of voters", maximum_n_voters)
print("Number of candidates", maximum_n_candidates)

plt.legend()
plt.show()
