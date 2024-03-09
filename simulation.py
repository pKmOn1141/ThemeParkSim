# Code for initialisation and simulation

from imports import *


def simulation(rides, amenities, settings, min_break, max_break, turn_label, window):
    max_guests, max_turns, fp_ratio = settings.ret_values()  # Takes settings out of object
    print("")
    # Prints key variables for testing
    print(rides)
    print(amenities)
    print(max_guests, max_turns, fp_ratio)

    # Check if there are any amenities
    if len(amenities) < 1:
        any_amenities = False
    else:  # If there are amenities
        any_amenities = True

    # Pre-simulation checks
    if len(rides) == 0 or max_guests == 0 or max_turns == 0:
        ready_to_start = False
    else:
        ready_to_start = True

    # Simulation
    if not ready_to_start:
        print("Key variables invalid, cancelling simulation")
    else:
        guest_list = initialise_guests(max_guests)  # Sets up the guests

        # Sets up breakdown settings for rides
        for curr_ride in rides:
            curr_ride.breakdowns(max_turns, min_break, max_break)

        # Calculate avg breakdown times
        for curr_ride in rides:
            curr_ride.find_avg_bd()

        # Ordering rides for guest checking
        ride_types = [[], [], [], [], [], [], []]  # Initialise the empty array
        ride_types = order_by_type(ride_types, rides)  # Storing what rides of each type are in 2d array
        ride_types = order_by_pop(ride_types)  # Order the arrays by ride popularity

        # Creates the park
        park = Park(max_guests)

        current_turn = 1
        print("started simulation")
        while current_turn <= max_turns:
            # Update the label with the current turn and update the window to show it
            turn_label.config(text=f"Turn {current_turn}/{max_turns}")
            window.update()

            for current_ride in rides:  # Check all the rides
                check_ride(current_ride, park, fp_ratio, current_turn)

            for current_guest in guest_list:  # Check all guests
                check_guest(current_guest, park, ride_types, any_amenities, amenities)

            current_turn += 1
        # End of simulation

        # Present data
        prin_basic_data(guest_list, rides, amenities, max_turns)

    return True, guest_list
