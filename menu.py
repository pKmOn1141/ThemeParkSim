# Functions to run the main menu, subject to change

from validation import *
from objects import *
from data_saving import *


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
    ride_relia = int_validation("Enter avrg breakdowns per day: ")

    ride = Ride(ride_name, ride_time, ride_cap, ride_pop, ride_type, ride_relia)
    rides.append(ride)
    for i in range(0, len(rides)):
        print(rides[i].ret_ride_info())


def remove_ride(rides):  # Removes target ride

    if len(rides) == 0:  # If list empty
        print("No rides to remove")
        return
    else:  # If not
        target_ride = str_validation("Enter ride name to remove: ")
        index = -1
        for current in range(0, len(rides)):  # Iterate through rides to find match
            if rides[current].ret_name().lower() == target_ride.lower():  # If names match
                index = current  # Save index of ride
                break  # End iteration

        if index == -1:  # If item not found
            print("Couldn't find ride")
        else:
            rides.remove(rides[index])  # Remove saved index from array
            print("Ride removed")


def edit_settings(guests, turns, fp_ratio):

    new_guests = int_validation(f'Current max guests = {guests}, enter new max: ')
    new_turns = int_validation(f'Current max turns = {turns}, enter new max: ')
    new_fp_ratio = flt_validation(f'Current fp ratio = {fp_ratio}, enter as decimal (0, .5, .75, .8): ')
    print(new_fp_ratio)

    return new_guests, new_turns, new_fp_ratio


def add_amenity(amenities):
    a_name = name_validation("Enter amenity name: ", amenities)
    a_time = int_validation("Enter time to spend at amenity: ")

    amenity = Amenity(a_name, a_time)
    amenities.append(amenity)

    return


def remove_amenity(amenities):
    if len(amenities) == 0:  # If list empty
        print("No amenities to remove")
        return
    else:
        target_amenity = str_validation("Enter amenity name to remove: ")
        index = -1
        for current in range(0, len(amenities)):
            if amenities[current].ret_name().lower() == target_amenity.lower():
                index = current
                break

        if index == -1:  # If item not found
            print("Couldn't find amenity")
        else:
            amenities.remove(amenities[index])
            print("Amenity removed")


def edit_amenities(amenities):
    finished = False
    while not finished:
        print("")
        print("Amenities - Select Option")
        print("1. Add Amenity")
        print("2. Remove Amenity")
        print("3. Go back")

        choice = int_validation("Input option: ")
        match choice:
            case 1:
                add_amenity(amenities)
            case 2:
                remove_amenity(amenities)
            case 3:
                return


def save_data(rides, amenities, guests, turns, fp_ratio):
    print(rides)
    print(amenities)
    save_to_file(rides, amenities, [guests, turns, fp_ratio])


def load_data(rides, amenities):
    # Try to see if the file selected exists
    valid_name = False
    while not valid_name:
        file_name = str_validation("Enter file name: ") + ".txt"
        try:
            f = open(file_name, 'r')
            valid_name = True
            f.close()
        except FileNotFoundError:
            print("File doesnt exist")
            return

    m_guests, m_turns, fp_r = read_from_file(file_name, rides, amenities)
    return m_guests, m_turns, fp_r


def data_imports(rides, amenities, guests, turns, fp_ratio):
    finished = False
    while not finished:
        print(" ")
        print("Save/Load Data")
        print("1. Save data")
        print("2. Load data")
        print("3. Go back")

        choice = int_validation("Input option: ")
        match choice:
            case 1:
                save_data(rides, amenities, guests, turns, fp_ratio)
            case 2:
                guests, turns, fp_ratio = load_data(rides, amenities)
            case 3:
                return guests, turns, fp_ratio


def main_menu(rides, guests, turns, fp_ratio, amenities):  # Main menu function

    finished = False
    while not finished:

        print(" ")
        print("Select Option")
        print("1. Edit rides")
        print("2. Edit park settings")
        print("3. Edit amenities")
        print("4. Save/Load settings")
        print("5. Start Sim")

        choice = int_validation("Input option: ")
        match choice:
            case 1:
                edit_ride(rides)
            case 2:
                guests, turns, fp_ratio = edit_settings(guests, turns, fp_ratio)
            case 3:
                edit_amenities(amenities)
            case 4:
                guests, turns, fp_ratio = data_imports(rides, amenities, guests, turns, fp_ratio)
            case 5:
                return rides, guests, turns, fp_ratio, amenities


if __name__ == '__main__':
    print("menu.py")
