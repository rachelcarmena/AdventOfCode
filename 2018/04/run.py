#!/usr/bin/python
from enum import Enum

class Status(Enum):
    ASLEEP = 0
    AWAKE = 1

def get_records_from(filename):
    result = []
    for record in open(filename):
        month = int(record[6:8])
        day = int(record[9:11])
        hour = int(record[12:14])
        minute = int(record[15:17])
        if record.rfind('#') > 0:
            ID_guard = int(record.split(' ')[3][1:])
            result.append({"month": month, "day": day, "hour": hour, "minute": minute, "ID_guard": ID_guard})
            continue
        if record.rfind('falls asleep') > 0:
            result.append({"month": month, "day": day, "hour": hour, "minute": minute, "status":Status.ASLEEP})
            continue
        result.append({"month": month, "day": day, "hour": hour, "minute": minute, "status":Status.AWAKE})
    return result

def order(records):
    return sorted(records, key = lambda record: (record["month"], record["day"], record["hour"], record["minute"]))

def get_minutes_list_per_guard_from(records):
    minutes_list_per_guard = {}
    for record in records:
        if "ID_guard" in record.keys():
            ID_guard = record["ID_guard"]
            continue
        if record["status"] == Status.ASLEEP:
            asleep_minute = record["minute"]
            continue
        if not ID_guard in minutes_list_per_guard.keys():
            minutes_list_per_guard[ID_guard] = []
        for minute in range(asleep_minute, record["minute"]):
            minutes_list_per_guard[ID_guard].append(minute)
    return minutes_list_per_guard

def get_ID_guard_with_max_number_of_minutes_from(list_per_guard):
    number_of_minutes_per_guard = [{"ID_guard": ID_guard, "minutes_number": len(list_per_guard[ID_guard])} for ID_guard in list_per_guard.keys()]
    record_with_max_number_of_minutes = max(number_of_minutes_per_guard, key = lambda record: record["minutes_number"])
    return record_with_max_number_of_minutes["ID_guard"]

def get_most_repeteated_minute_and_count_from(minutes_list):
    minute_and_count_list = map(lambda minute: {"minute": minute, "count": minutes_list.count(minute)}, minutes_list)
    return max(minute_and_count_list, key = lambda minute_and_count: minute_and_count["count"])

def get_max_stats_per_guard_from(minutes_list_per_guard):
    stats_per_guard = []
    for ID_guard in minutes_list_per_guard.keys():
        info_per_guard = get_most_repeteated_minute_and_count_from(minutes_list_per_guard[ID_guard])
        info_per_guard["ID_guard"] = ID_guard

        stats_per_guard.append(info_per_guard)
    return max(stats_per_guard, key = lambda info_per_guard: info_per_guard["count"])

def print_solution(part_number, ID_guard, selected_minute):
    print '-'*20
    print "Part #" + str(part_number)
    print '-'*20
    print "ID guard: " + str(ID_guard)
    print "Minute when guard spends asleep the most: " + str(selected_minute)
    print "Solution: {0} * {1} = {2}".format(ID_guard, selected_minute, ID_guard * selected_minute)

if __name__ == "__main__":

    records = get_records_from("input.txt")  
    records = order(records)
    minutes_list_per_guard = get_minutes_list_per_guard_from(records)

    ID_guard = get_ID_guard_with_max_number_of_minutes_from(minutes_list_per_guard)
    max_minute_and_count = get_most_repeteated_minute_and_count_from(minutes_list_per_guard[ID_guard])
    print_solution(1, ID_guard, max_minute_and_count["minute"])

    max_stats_per_guard = get_max_stats_per_guard_from(minutes_list_per_guard)
    print_solution(2, max_stats_per_guard["ID_guard"], max_stats_per_guard["minute"])
