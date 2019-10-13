# This is a unique secret santa gift exchange script used to take some 
# arbitrary amount of people and assign them each with a gift from the gift 
# amount section. This allow everyone to buy each other a gift!

import random

# -------------------------------------------
# Constants to change for yourself!
# -------------------------------------------
TOTAL_PEOPLE = ["A", "B", "C", "D", "E", "F"]

# There must be one less gift amount than total participants (you dont buy 
# yourself a gift) 
GIFT_AMOUNTS = [50, 30, 20, 15, 10]

# -------------------------------------------
# End of constants! Do not change anything!
# -------------------------------------------

# Takes two lists of names and randomly selects a name from the difference 
# between two and the global set of names.
# Returns -1 on error or the choice of the name on success
def pick_name(some_list, round_list):
    valid_names_tmp = set(TOTAL_PEOPLE) - set(some_list)
    valid_names = valid_names_tmp - set(round_list)
    if (len(valid_names) == 0):
        return -1
    return random.choice(list(valid_names))

# Restarts the state of the game a blank one.
def restart():
    picked_name_state = {}
    for name in TOTAL_PEOPLE:
        picked_name_state[name] = [name]
    return picked_name_state

# Function that takes a state of the secret santa and
# either returns false if it fails, or returns the updated
# state of the list.
def do_round(state):
    # Create a copy of the list of names, for that round
    local_list = []
    for name in state:
        drawn_name = pick_name(state[name], local_list)
        if drawn_name == -1:
            return []
        
        local_list.append(drawn_name)
        state[name].append(drawn_name)

    return state

def main():
    state = restart()
    fail = False
    
    if len(GIFT_AMOUNTS) >= len(TOTAL_PEOPLE):
        print("TOO MANY GIFT AMOUNTS LISTED!")
        print("Ensure GIFT AMOUNT <= TOTAL_PEOPLE!")
        exit()

    # Uses the total amount specified in the gift amounts to determine who 
    # gives who what.
    for _ in range(len(GIFT_AMOUNTS)):
        tmp = do_round(state)
        if tmp == []:
            fail = True
            break
        state = tmp
    
    if fail:
        main()
    
    else:
        for key in state:
            index = 0
            # Pretty printing based on the gift amounts.
            # This is used to pipe into a file in bash and search people
            # using grep *insert name*'s. This allows the secret to be kept!
            for person in state[key][1:]:
                print(key + "'s " + str(GIFT_AMOUNTS[index]) + "$ person is: " 
                        + str(state[key][index + 1]))
                index += 1
main()
