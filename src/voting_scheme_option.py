from enum import Enum


class VotingSchemeOption(int):
    PLURALITY_VOTING = 0
    ANTI_PLURALITY_VOTING = 1
    VOTING_FOR_TWO = 2
    BORDA = 3