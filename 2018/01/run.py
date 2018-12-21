#!/usr/bin/python
from sys import exit


def apply_change_and_get_new_frequency(change, frequency):
    if change['symbol'] == '+':
        return frequency + change['value']
    return frequency - change['value']

def get_changes_from(filename):
    changes = []
    for line in open(filename):
        changes.append({'symbol': line[0], 'value': int(line[1:-1])})
    return changes

def next_index_from(index, length):
    new_index = index + 1
    if new_index == length:
        return 0
    return new_index

if __name__ == "__main__":

    frequency = 0
    changes = get_changes_from("input.txt")
    for change in changes:
        frequency = apply_change_and_get_new_frequency(change, frequency)
    print "The resulting frequency after all of the changes in frequency: " + str(frequency)
    
    frequency = 0
    frequencies = [frequency]
    index = 0
    while True:
        frequency = apply_change_and_get_new_frequency(changes[index], frequency)
        if not frequency in frequencies:
            frequencies.append(frequency)
            index = next_index_from(index, len(changes))
        else:
            print "The first frequency my device reaches twice: " + str(frequency)
            exit(0)
