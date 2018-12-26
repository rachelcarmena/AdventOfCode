#!/usr/bin/python

def get_polymer_from(filename):
    polymer_file = open(filename)
    return polymer_file.read()[:-1]

def react(unit, other_unit):
    if unit != other_unit:
        return (unit.upper() == other_unit) or (unit.lower() == other_unit)
    return False

def length_after_fully_react(polymer):
    index = 0
    while index < (len(polymer) - 1):
        if not react(polymer[index], polymer[index + 1]):
            index += 1
        else:
            polymer = polymer[:index] + polymer[index + 2:]
            index -= 1
            if index < 0:
                index = 0
    return len(polymer)

def length_after_removing_one_unit_and_fully_react(polymer, upper_unit):
    polymer = polymer.replace(upper_unit, "")
    polymer = polymer.replace(upper_unit.lower(), "")
    return length_after_fully_react(polymer)

def length_of_shortest_polymer(polymer):
    final_length_per_polymer = {}
    for unit in polymer:
        upper_unit = unit.upper()
        if not upper_unit in final_length_per_polymer.keys():
            final_length_per_polymer[upper_unit] = length_after_removing_one_unit_and_fully_react(polymer, upper_unit)
    min_pair = min(final_length_per_polymer.items(), key = lambda pair: pair[1])
    return min_pair[1]

if __name__ == "__main__":

    polymer = get_polymer_from("input.txt")
    print "Part #1: {0}".format(length_after_fully_react(polymer))
    print "Part #2: {0}".format(length_of_shortest_polymer(polymer))
