# Functions to run the main menu, subject to change

from validation import *
from objects import *


def edit_ride(rides):  # Ride editing menu

    options = {
        1: "add_ride(rides)",
        2: "remove_ride(rides)",
        3: "1"
    }

    finished = False
    while not finished:
        print(" ")
        print("Rides - Select Option")
        print("1. Add ride")
        print("2. Remove ride")
        print("3. Go back")

        choice = int_validation("Input option: ")
        if choice == 3:
            finished = True
        else:
            eval(options[choice])


def add_ride(rides):  # Asks for ride info and creates object

    ride_name = name_validation("Enter ride name: ", rides)
    ride_time = int_validation("Enter ride time: ")
    ride_cap = int_validation("Enter ride capacity: ")
    ride_pop = int_validation("Enter ride popularity: ")
    ride_type = int_validation("Enter ride type (0-6 or else it breaks): ")

    ride = Ride(ride_name, ride_time, ride_cap, ride_pop, ride_type)
    rides.append(ride)
    for i in range(0, len(rides)):
        print(rides[i].ret_ride_info())


def remove_ride(rides):  # Removes target ride

    if len(rides) == 0:  # If list empty
        print("No rides to remove")
        return
    else:
        target_ride = str_validation("Enter ride name to remove: ")
        index = -1
        for current in range(0, len(rides)):
            if rides[current].ret_name().lower() == target_ride.lower():
                index = current
                break

        if index == -1:  # If item not found
            print("Couldn't find ride")
        else:
            rides.remove(rides[index])
            print("Ride removed")


def edit_settings(guests, turns):

    new_guests = int_validation(f'Current max guests = {guests}, enter new max: ')
    new_turns = int_validation(f'Current max turns = {turns}, enter new max: ')

    return new_guests, new_turns


def start_sim():

    pass


def main_menu(rides, guests, turns):  # Main menu function

    options = {
        1: "edit_ride(rides)",
        2: "edit_park(guests, turns)",
        3: "start_sim()"
    }

    finished = False
    while not finished:

        print(" ")
        print("Select Option")
        print("1. Edit rides")
        print("2. Edit park settings")
        print("3. Start sim")

        choice = int_validation("Input option: ")
        if choice == 2:
            guests, turns = edit_settings(guests, turns)
        elif choice == 3:
            finished = True
            eval(options[choice])
        else:
            eval(options[choice])

    return rides, guests, turns


if __name__ == '__main__':
    print("menu.py")
