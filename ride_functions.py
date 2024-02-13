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


def check_ride(curr_ride, park, fp_r, curr_turn):  # Checks what to do with rides
    name, max_turn, ride_turn = curr_ride.ret_check_ride()  # Get ride information
    rq, ride, ride_cap, current_rides, fp_q = curr_ride.ret_ride_queues()  # Get ride queues and queue info
    next_bd, bd_status, bd_time = curr_ride.ret_bd_stats()  # Get breakdown stats

    if next_bd == -1:  # If there are no breakdowns
        bd_start, bd_duration = -1, 0  # Set to negative value so it skips checks
    else:
        bd_start, bd_duration = next_bd.ret_info()  # Get exact breakdown info

    if curr_turn == bd_start:  # If ride needs to breakdown
        print(f'{name} broke down')
        curr_ride.set_bd_status(True)
        curr_ride.set_bd_time(bd_duration)
        curr_ride.upd_bd_time()  # Include this turn in the breakdown duration
        curr_ride.rem_breakdown()  # Removes current breakdown from array
    elif bd_status:  # If ride broken down
        curr_ride.upd_bd_time()
        if bd_time == 0:  # If 'fixed'
            curr_ride.set_bd_status(False)
            print(f'{name} fixed')
    else:  # If ride isn't broken down, do normal stuff
        match True:
            case _ if curr_ride.queues_empty():  # If no one is there to be loaded
                return

            case _ if ride_turn == max_turn:  # If ride needs to stop
                ride_turn = 0
                print(f'{name} unloading')
                for space in range(0, current_rides):  # Takes guests off ride
                    curr_ride.off_ride(park)
                curr_ride.rst_curr_riders()
                curr_ride.fin_check_ride(ride_turn, rq, ride, fp_q)  # Updates all info
                return

            case _ if ride_turn == 0:  # If ride needs to be loaded
                load_ride(curr_ride, ride_cap, fp_r)
                print(f'{name} loaded')

        ride_turn += 1  # Increase ride turns, only when not broken down
        print(f'{name} turn increased')

    curr_ride.wait_time()  # Find the wait time at the end of the run
    curr_ride.fin_check_ride(ride_turn, rq, ride, fp_q)  # Updates all new info
    return
