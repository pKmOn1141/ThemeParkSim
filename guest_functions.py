# Functions for running each guest

from objects import Guest
import math
import random


def initialise_guests(max_guests):  # Creates guests and sets up their personalities

    guest_list = []
    guest_ps = find_pers_prop(max_guests)  # Proportions of guest personalities
    assigned_ps = [0, 0, 0, 0, 0]  # Assigned personalities
    # Average(40), Enthusiast(5), Scared(20), Thrill-seeker(20), Child(15) - will be customisable

    for i in range(0, max_guests):  # Create each guest
        guest_list.append(Guest(i + 1))

    # Distributing personalities
    tar_index = 0
    for guest in guest_list:  # Assign personalities
        c_ps = guest.ret_personality()  # For checking personality

        match c_ps:  # To validate in case guest already has personality
            case -1:  # If guest doesn't have personality
                if tar_index == 6:  # If all personality types done
                    print("all personalities done")

                elif assigned_ps[tar_index] < guest_ps[tar_index]:  # If max for personality isn't reached
                    guest.assign_p(tar_index)  # Assign personality
                    assigned_ps[tar_index] += 1

                elif assigned_ps[tar_index] >= guest_ps[tar_index]:  # If max is reached
                    tar_index += 1  # Move onto next personality
                    guest.assign_p(tar_index)  # Assign personality
                    assigned_ps[tar_index] += 1

            case _:
                print("guest already has personality")

    return guest_list


def find_pers_prop(max_guests):  # Find how to distribute guests personalities
    array = [0.4, 0.05, 0.2, 0.2, 0.15]  # Percentages for each
    for p_type in range(0, 5):
        val = array[p_type]
        val *= max_guests
        val = math.floor(val)
        array[p_type] = val

    if sum(array) != max_guests:  # If not everyone would get a personality
        difference = max_guests - sum(array)
        smallest = 0
        for i in range(0, 5):  # Find the smallest in the array
            if array[i] < array[smallest]:
                smallest = i

        array[smallest] += difference

    return array


def choose_type(a, b, ride_types):  # Choose the ride type based on the limits
    types = []
    for i in range(a, b+1):  # Create a list of all the valid ride types
        if len(ride_types[i]) > 0:  # If type has any rides
            types.append(i)  # Add its index to the array

    if len(types) == 0:  # If no valid ride types
        r_type = -1
    else:
        r_type = random.choice(types)  # Picks random type

    return r_type


def add_to_queue(name, guest, ride, fp):  # Add guest into ride queue
    match fp:
        case 1:  # Use fastpass queue
            print("added to fastpass")
            guest.add_ride(name)
            ride.into_fast(guest)  # Put into queue
        case 0:  # Use normal queue
            print("added to normal queue")
            guest.add_ride(name)
            ride.into_queue(guest)


def choose_queue(fp_c):  # Choose whether to use fast pass queue or normal
    rand_num = random.random()  # Pick a random number between 0-1
    if rand_num < fp_c:  # Use a fastpass
        return 1  # Guest uses fastpass queue
    else:
        return 0  # Guest uses normal queue


def make_ride_choice(max_waits, a, b, ride_types, guest, multi_ride, fp_c):  # Choose ride, customisable for each personality
    # max_waits=array of times, a/b=for type choice, ride_types=array of rides, guest=guest object
    type_choice = choose_type(a, b, ride_types)  # Choose type, except for kids

    if type_choice == -1:  # If no choice found
        guest.change_status(-1)  # Tell guest to leave the park
        return  # End function

    rides_checked = 1
    for ride in ride_types[type_choice]:  # Iterate through rides to find best
        name = ride.ret_name()
        ridden = guest.ret_rides()  # List of rides guest has already ridden
        if not multi_ride:  # If guest won't ride same ride twice
            if name in ridden:  # If ride already ridden skip
                continue

        popularity, wait_time = ride.choose_ride_info()
        if popularity > 4:  # If popularity is greater than 5
            popularity = 4  # Use same conditions as if it were 5
        if wait_time < max_waits[popularity]:  # If wait is 'tolerable'
            fp = choose_queue(fp_c)
            add_to_queue(name, guest, ride, fp)  # Put into queue
            return  # End function
        elif wait_time > max_waits[popularity]:  # Skip to next ride
            if rides_checked == len(ride_types[type_choice]):  # If looking at last ride
                fp = choose_queue(fp_c)
                add_to_queue(name, guest, ride, fp)  # Put into queue
                return  # End function
            else:  # Go to next ride
                rides_checked += 1
                continue


def choose_ride(guest, ride_types):  # Incomplete
    is_empty = all(not row for row in ride_types)  # Check if the array is empty
    if is_empty:  # Check if there are any rides
        print("no rides to go on")
        return

    personality = guest.ret_personality()
    match personality:
        case 0:  # Average
            max_waits = [140, 110, 80, 60, 40]  # How long they can wait for each ride popularity
            fp_chance = 0.2  # Chance guest has a fast pass
            multi_ride = False  # Cant ride the same rides more than once
            make_ride_choice(max_waits, 1, 6, ride_types, guest, multi_ride, fp_chance)  # Finds ride and puts guest on it

        case 1:  # Enthusiast
            max_waits = [170, 130, 90, 65, 45]
            fp_chance = 0.15
            multi_ride = True
            make_ride_choice(max_waits, 1, 6, ride_types, guest, multi_ride, fp_chance)

        case 2:  # Tame rider
            max_waits = [125, 95, 70, 50, 30]
            fp_chance = 0.1
            multi_ride = True
            make_ride_choice(max_waits, 1, 3, ride_types, guest, multi_ride, fp_chance)

        case 3:  # thrillseeker
            max_waits = [170, 135, 100, 70, 40]
            fp_chance = 0.25
            multi_ride = True
            make_ride_choice(max_waits, 3, 6, ride_types, guest, multi_ride, fp_chance)

        case 4:  # Child
            max_waits = [110, 80, 60, 40, 25]
            fp_chance = 0.15
            multi_ride = True
            make_ride_choice(max_waits, 0, 3, ride_types, guest, multi_ride, fp_chance)


def choose_amenity(amenities):  # Choose an amenity to use, and return how long the guest will be using that amenity
    choice = random.choice(amenities)
    time = choice.time_to_spend()  # Find time to spend for chosen amenity

    return time


def check_guest(guest, park, ride_types, any_amenities, amenities):  # Checks what to do for each guest
    wait_time, queue_status, time_left = guest.ret_info()

    match queue_status:
        case -2:  # Ignore guest
            pass

        case -1:  # Make guest leave the park
            park.remove_from(guest)
            guest.change_status(-2)

        case 0:  # If guest isn't in anything, put into park
            park.add_to(guest)
            guest.change_status(1)

        case 1:  # If guest is in park
            if not any_amenities:  # If there are no amenities, skip straight to choosing ride
                guest.change_status(2)
                guest.update_rides_ridden()
                choose_ride(guest, ride_types)

            else:  # If there are amenities, pick whether to go on ride or use amenity
                amenity_chance = 0.2  # Chance that guest wants to use an amenity
                choice = random.random()  # Pick random number between 0-1
                if choice < amenity_chance:  # If chose to use amenity
                    guest.change_status(5)
                    time = choose_amenity(amenities)
                    guest.set_time_left(time)

                else:  # Pick a queue to go into and enter it
                    guest.change_status(2)
                    guest.update_rides_ridden()
                    choose_ride(guest, ride_types)

        case 2:  # If guest in a queue
            guest.update_time()

        case 3:  # If guest on ride
            pass

        case 4:  # If just got off ride
            guest.change_status(1)
        
        case 5:  # If using an amenity
            if time_left == 0:  # If need to leave amenity
                guest.change_status(1)

            else:  # If still have time left
                guest.upd_time_left()  # Reduce time left by 1


if __name__ == '__main__':
    print("guest_functions.py")
