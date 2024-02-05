# Theme park simulation - James Curzon

from imports import *


if __name__ == '__main__':

    rides = []
    max_guests = 0
    max_turns = 0

    rides, max_guests, max_turns = main_menu(rides, max_guests, max_turns)  # Main menu
    print("")
    # Prints key variables for testing
    print(rides, max_guests, max_turns)

    guest_list = initialise_guests(max_guests)  # Sets up the guests

    # Ordering rides for guest checking
    ride_types = [[], [], [], [], [], [], []]  # Initialise the empty array
    ride_types = order_by_type(ride_types, rides)  # Storing what rides of each type are in 2d array
    ride_types = order_by_pop(ride_types)  # Order the arrays by ride popularity

    # Creates the park
    park = Park(max_guests)

    # Start of simulation
    if len(rides) == 0:  # Check if there are any rides
        print("no rides, cancelling simulation")
    else:
        current_turn = 1
        print("started simulation")
        while current_turn <= max_turns:

            for current_ride in rides:  # Check all the rides
                check_ride(current_ride, park)

            for current_guest in guest_list:  # Check all guests
                check_guest(current_guest, park, ride_types)

            current_turn += 1
        # End of simulation

        # Present data
        prin_basic_data(guest_list, rides)