#!/usr/bin/python
from sys import exit

def get_IDs_from(filename):
    result = []
    for line in open(filename):
        result.append(line[:-1])
    return result

def get_letters_and_count_for(ID):
    result = {}    
    for letter in ID:
        if letter in result.keys():
            result[letter] += 1
        else:
            result[letter] = 1
    return result

def calculate_checksum_from(IDs):
    twice_number = 0
    three_times_number = 0
    for ID in IDs:
        letters_and_count = get_letters_and_count_for(ID)
        if 2 in letters_and_count.values():
            twice_number += 1
        if 3 in letters_and_count.values():
            three_times_number += 1
    return twice_number * three_times_number

def print_answer_from(ID, otherID, position):
    print "--- PART TWO ---"
    print "From:           " + ID
    print "                " + otherID
    print "Common letters: " + ID[:position] + " " + ID[position + 1:]
    print "Answer:         " + ID[:position] + ID[position + 1:]

def print_common_letters_between_two_correct_IDs(IDs):
    position = 0
    for index, ID in enumerate(IDs):
        for otherID in IDs[index + 1:]:
            differentLetters = 0
            for index in range(len(ID)):
                if ID[index] != otherID[index]:
                    position = index
                    differentLetters += 1
                    if differentLetters > 1:
                        break
            if differentLetters == 1:
                print_answer_from(ID, otherID, position)
                exit(0)


if __name__ == "__main__":

    IDs = get_IDs_from("input.txt")
    print "The rudimentary checksum: " + str(calculate_checksum_from(IDs))
    print_common_letters_between_two_correct_IDs(IDs)
