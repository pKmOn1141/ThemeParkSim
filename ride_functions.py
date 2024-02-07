# Functions for dealing with the rides during main algorithm

import math


def order_by_type(ride_types, rides):  # Adds rides into array depending on type
    for curr_ride in rides:  # Puts each ride into its correct section
        r_t = curr_ride.ret_rt()  # Get ride type to add to right array
        ride_types[r_t].append(curr_ride)  # Add to appropriate array

    return ride_types


def order_by_pop(ride_types):  # Order each type of ride by their popularity
    for i in range(0, 6):  # Order each array, bubble sort
        amount = len(ride_types[i])  # For cheking how many rides in each sub array
        if amount == 0:  # No rides, skip to next array
            continue
        else:  # Anything else, do sort
            done_sort = False
            while not done_sort:
                swapped = False
                if len(ride_types[i]) <= 1:
                    done_sort = True
                    continue
                else:
                    for y in range(0, len(ride_types[i])-1):  # Loops through each ride in the sub array
                        # Check if popularities are greater or smaller
                        if ride_types[i][y].ret_popular() > ride_types[i][y+1].ret_popular():
                            ride_types[i][y], ride_types[i][y+1] = ride_types[i][y+1], ride_types[i][y]  # Swap the rides
                            swapped = True
                        elif not swapped:  # If nothing swapped
                            done_sort = True
                            break
                        else:
                            done_sort = True

    print(ride_types)
    return ride_types


def load_ride(curr_ride, ride_cap, fp_r):  # Loads the ride with guests from the queue
    fp_amount = math.floor(ride_cap * fp_r)
    fp_riders = True
    for space in range(0, ride_cap):
        match curr_ride.queues_empty():  # If queues arent empty
            case False:
                if fp_riders:  # If there are fast pass riders available
                    if curr_ride.ret_curr_riders() == fp_amount:  # If all fast pass riders are in
                        q_type = 0  # Load from normal queue
                    else:  # If fast pass riders aren't in
                        if curr_ride.ret_fp().qsize() > 0:  # If still fp riders to get on
                            q_type = 1
                        else:  # If no more fp riders to get on
                            q_type = 0
                            fp_riders = False

                else:  # If no more fp riders, despite being room
                    q_type = 0
                curr_ride.upd_curr_riders()  # Updates how many riders are on ride
                curr_ride.onto_ride(q_type)  # Load ride from queue until full, changes guests status

            case _:
                break  # Skip to ride start if no one else can fit

    return  # End function


def check_ride(curr_ride, park, fp_r):  # Checks what to do with rides
    name, max_turn, ride_turn = curr_ride.ret_check_ride()  # Get ride information
    rq, ride, ride_cap, current_rides, fp_q = curr_ride.ret_ride_queues()  # Get ride queues and queue info

    match True:
        case _ if curr_ride.queues_empty():  # If no one is there to be loaded
            return

        case _ if ride_turn == max_turn:  # If ride needs to stop
            ride_turn = 0
            for space in range(0, current_rides):  # Takes guests off ride
                curr_ride.off_ride(park)
            curr_ride.rst_curr_riders()
            curr_ride.fin_check_ride(ride_turn, rq, ride, fp_q)  # Updates all info
            return

        case _ if ride_turn == 0:  # If ride needs to be loaded
            load_ride(curr_ride, ride_cap, fp_r)

    ride_turn += 1  # Increase ride turns
    curr_ride.wait_time()  # Find the wait time at the end of the run
    curr_ride.fin_check_ride(ride_turn, rq, ride, fp_q)  # Updates all new info
    return
