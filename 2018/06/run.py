#!/usr/bin/python

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, to_coordinate):
        return abs(self.x - to_coordinate.x) + abs(self.y - to_coordinate.y)

    def __eq__(self, another_coordinate):
        return (self.x == another_coordinate.x) and (self.y == another_coordinate.y)

    def __str__(self):
        return "({0}, {1})".format(self.x, self.y)

    def __hash__(self):
        return hash((self.x, self.y))

def get_coordinates_from(filename):
    coordinates = []
    for line in open(filename):
        parts = line.split(", ")
        coordinates.append(Coordinate(int(parts[0]), int(parts[1])))
    return coordinates

def get_coordinate_and_distance_list(from_coordinate, coordinates):
    result = []
    for coordinate in coordinates:
        distance = from_coordinate.distance_to(coordinate)
        result.append((coordinate, distance))
    return result

def calculate_closest_coordinate(new_coordinate, coordinates):
    coordinate_and_distance_list = get_coordinate_and_distance_list(new_coordinate, coordinates)
    min_distance = min(coordinate_and_distance_list, key = lambda pair: pair[1])
    distances = [pair[1] for pair in coordinate_and_distance_list]
    if distances.count(min_distance[1]) > 1:
        return None
    return min_distance[0]

def delete_coordinate(area_size_per_coordinate, coordinate):
    if coordinate in area_size_per_coordinate.keys():
        del(area_size_per_coordinate[coordinate])
    return area_size_per_coordinate

def sum_of_distances(coordinate_and_distance_list):
    distances_list = [coordinate_and_distance[1] for coordinate_and_distance in coordinate_and_distance_list]
    return sum(distances_list)
        
if __name__ == "__main__":
    
    coordinates = get_coordinates_from("input.txt")
    max_x = max([coordinate.x for coordinate in coordinates]) 
    max_y = max([coordinate.y for coordinate in coordinates]) 
    
    area_size_per_coordinate = {}
    for coordinate in coordinates:
        area_size_per_coordinate[coordinate] = 1
    
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            if not Coordinate(x, y) in coordinates:
                coordinate = calculate_closest_coordinate(Coordinate(x, y), coordinates)
                if coordinate:
                    area_size_per_coordinate[coordinate] += 1
            
    # Discarding infinites
    y = -1
    for x in range(max_x + 2):
        coordinate = calculate_closest_coordinate(Coordinate(x, y), coordinates)
        if coordinate:
            area_size_per_coordinate = delete_coordinate(area_size_per_coordinate, coordinate)
    
    y = max_y + 2
    for x in range(-1, max_x + 1):
        coordinate = calculate_closest_coordinate(Coordinate(x, y), coordinates)
        if coordinate:
            area_size_per_coordinate = delete_coordinate(area_size_per_coordinate, coordinate)

    x = max_x + 2
    for y in range(max_y + 2):
        coordinate = calculate_closest_coordinate(Coordinate(x, y), coordinates)
        if coordinate:
            area_size_per_coordinate = delete_coordinate(area_size_per_coordinate, coordinate)
    
    x = -1
    for y in range(-1, max_y + 1):
        coordinate = calculate_closest_coordinate(Coordinate(x, y), coordinates)
        if coordinate:
            area_size_per_coordinate = delete_coordinate(area_size_per_coordinate, coordinate)

    print "Part #1: {0}".format(max(area_size_per_coordinate.items(), key = lambda pair: pair[1])[1])

    region_size = 0    
    for x in range(max_x + 1):
        for y in range(max_y + 1):
            coordinate_and_distance_list = get_coordinate_and_distance_list(Coordinate(x, y), coordinates)
            if sum_of_distances(coordinate_and_distance_list) < 10000:
               region_size += 1

    print "Part #2: {0}".format(region_size)
