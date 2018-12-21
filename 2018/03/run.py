#!/usr/bin/python

def get_claims_from(filename):
    result = []
    for claim in open(filename):
        claim_parts = claim.split(' ')
        
        id_value = claim_parts[0][1:]
        position = claim_parts[2][:-1].split(',')
        size = claim_parts[3][:-1].split('x')
        
        result.append({"id": id_value, "left": int(position[0]), "top": int(position[1]), "wide": int(size[0]), "tall": int(size[1])})
    return result 

def init_diagram_from(claims):
    max_rows_number = 0
    max_columns_number = 0
    for claim in claims:
        top_plus_tall = claim["top"] + claim["tall"]
        if top_plus_tall > max_rows_number:
            max_rows_number = top_plus_tall
        left_plus_wide = claim["left"] + claim["wide"]
        if left_plus_wide > max_columns_number:
            max_columns_number = left_plus_wide
   
    result = []
    for row in range(max_rows_number):
        column_list = []
        for column in range(max_columns_number):
            column_list.append({'count': 0, 'claim_ids': []})
        result.append(column_list)
    return result

def fill(diagram, claims):
    result = diagram
    for claim in claims:
        for row in range(claim["top"], claim["top"] + claim["tall"]):
            for column in range(claim["left"], claim["left"] + claim["wide"]):
                result[row][column]["count"] += 1
                result[row][column]["claim_ids"].append(claim["id"])
    return result

def get_inches_number_with_two_or_more_claims(diagram):
    result = 0
    for row in range(len(diagram)):
        two_or_more_list = filter(lambda cell: cell["count"] > 1, diagram[row])
        result += len(two_or_more_list)
    return result

def get_claim_not_overlapping(claims, diagram):
    candidates = [claim["id"] for claim in claims]

    for row in range(len(diagram)):
        for cell in diagram[row]:
            if cell["count"] > 1:
                for claim_id in cell["claim_ids"]:
                    if claim_id in candidates:
                        candidates.remove(claim_id)
    print candidates
    return candidates[0] 

if __name__ == "__main__":

    claims = get_claims_from("input.txt")
    diagram = init_diagram_from(claims)
    diagram = fill(diagram, claims)
    print "Part 1: " + str(get_inches_number_with_two_or_more_claims(diagram))
    print "Part 2: " + str(get_claim_not_overlapping(claims, diagram))

