# Object file, containing all the class declarations and methods

import queue as q
import random
from numpy import random as p  # Labelled different to destinct from random


class Park(object):
    def __init__(self, ms):
        self._max_size = ms
        self._arr = []

    def update_arr(self, array):  # Update the array
        self._arr = array

    def add_to(self, item):  # Adds item to array
        self._arr.append(item)

    def remove_from(self, item):  # Removes item from array
        self._arr.remove(item)

    def ret_ms(self):
        return self._max_size

    def ret_arr(self):
        return self._arr


class Guest(object):
    def __init__(self, name):
        self._name = f"Guest {name}"
        self._wait_time = 0  # Total time spent in queues
        self._rides_ridden = 0
        self._amenities_used = 0
        self._rides = []  # Array of the rides ridden
        self._queue_status = 0
        # 0=not in anything, 1=in park, 2=in queue, 3=on ride, 4=just off ride, 5=in amenity, -1=leaving park, -2=gone from park
        self._personality = -1
        # -1=unassigned, 0=average, 1=enthusiast, 2=tame, 3=thrillseeker, 4=child
        self._time_left = 0  # Time left to spend at amenity
        self._current_wait = 0  # Time spent in current queue

    def upd_amenities_used(self):
        self._amenities_used += 1

    def ret_am_used(self):
        return self._amenities_used

    def upd_curr_wait(self, val):  # Change the current wait attribute
        match val:
            case 0:  # Reset the value
                self._current_wait = 0
            case 1:  # Update the value
                self._current_wait += 1

    def ret_curr_wait(self):  # Return the current time waited
        return self._current_wait

    def assign_p(self, personality):  # Assign guest personality
        self._personality = personality

    def ret_personality(self):
        return self._personality

    def ret_info(self):
        return self._wait_time, self._queue_status, self._time_left

    def ret_name(self):
        return self._name

    def ret_time(self):
        return self._wait_time

    def update_time(self):
        self._wait_time += 1

    def update_rides_ridden(self):
        self._rides_ridden += 1

    def ret_rides_ridden(self):
        return self._rides_ridden

    def ret_rides(self):
        return self._rides

    def add_ride(self, name):  # Add ridden rides names
        self._rides.append(name)

    def change_status(self, value):  # Change the queue_status attribute
        # Look above for what each value means
        self._queue_status = value

    def set_time_left(self, item):  # Set the time left to spend at amenity
        self._time_left = item

    def upd_time_left(self):  # Updates how long left to spend at amenity
        self._time_left -= 1


class RQueues(object):
    def __init__(self):
        self._queue = q.Queue()
        self._fast_queue = q.Queue()
        self._ride = q.Queue()

    def into_queue(self, item):  # Puts guest from park into queue
        item.change_status(2)
        self._queue.put_nowait(item)

    def into_fast(self, item):  # Puts guest from park into fast past queue
        item.change_status(2)
        self._fast_queue.put_nowait(item)

    def onto_ride(self, q_type):  # Puts the guest from queue onto ride
        wait_time = 0
        # q_type: 0 = normal, 1 = fast pass
        match q_type:
            case 0:  # If coming from normal queue
                guest = self._queue.get_nowait()
                guest.change_status(3)
                wait_time = guest.ret_curr_wait()  # Get wait time from guest
                self._ride.put_nowait(guest)

            case 1:  # If coming from fast pass queue
                guest = self._fast_queue.get_nowait()
                guest.change_status(3)
                wait_time = guest.ret_curr_wait()
                self._ride.put_nowait(guest)

        return wait_time

    def off_ride(self, park):  # Moves the guest off the ride and into the park
        guest = self._ride.get_nowait()
        guest.change_status(4)  # Just got off ride
        park.add_to(guest)

    def update_queues(self, queue, fast, ride):
        self._queue = queue
        self._fast_queue = fast
        self._ride = ride

    def queue_time(self):  # Return the size of the queue to work out the time
        return self._queue.qsize()

    def ret_queue(self):
        return self._queue

    def ret_fast(self):  # Return fast pass queue
        return self._fast_queue

    def ret_ride(self):
        return self._ride


class Breakdowns(object):  # Stores the conditions of a ride breaking down
    def __init__(self, start_turn, duration):
        self._start_turn = start_turn  # Turn where breakdown starts
        self._duration = duration

    def ret_start(self):
        return self._start_turn

    def ret_duration(self):
        return self._duration

    def ret_info(self):
        return self._start_turn, self._duration


class Ride(object):
    def __init__(self, name, rl, rc, rp, rt, rr):
        self._name = name
        self._ride_time = rl  # How long ride lasts
        self._ride_cap = rc  # How many people fit on ride
        self._ride_pop = rp  # Ride popularity
        self._ride_type = rt
        # 0=kids, 1=small coaster, 2=small flat, 3=dark, 4=big flat, 5=big coasts, 6=insane
        self._ride_reliability = rr  # Average daily breakdowns
        self._breakdowns = 0  # How many times the ride will break down
        self._bd_schedu = []  # At what turns the ride is going to breakdown
        self._bd_status = False  # Status of whether ride is broken down or not
        self._bd_time = 0  # How long left till 'fixed'
        self._queues = RQueues()
        self._ride_turn = 0
        self._current_riders = 0
        self._current_wait = 0
        self._total_riders = 0  # Stores how many people have ridden the ride in total
        self._norm_riders = 0  # Tracks normal queue riders
        self._fp_riders = 0  # Tracks fp queue riders
        self._time_waited = 0  # Stores the average time waited
        self._avg_breakd_time = 0  # Stores the average time brokendown

    def ret_data(self, max_turns):  # Returns data for final screen
        try:
            average_wait = self._time_waited // self._total_riders
        except ZeroDivisionError:
            average_wait = 0

        queue_ratio = f'{self._norm_riders}/{self._fp_riders}'  # Create the ratio between queues
        return f'{self._name}  |  {self._total_riders}  |  {queue_ratio}  |  {average_wait}  |  {self._breakdowns}  |  {self._avg_breakd_time}'

    def upd_total_riders(self):  # Update total riders counter
        self._total_riders += 1

    def save_attributes(self):  # Return attributes needed for saving information
        return self._name, self._ride_time, self._ride_cap, self._ride_pop, self._ride_type, self._ride_reliability

    def find_avg_bd(self):  # Calculates the average time brokendown
        total = 0
        for curr_bd in self._bd_schedu:  # Iterate breakdowns
            total += curr_bd.ret_duration()

        try:  # Find average
            self._avg_breakd_time = total // len(self._bd_schedu)
        except ZeroDivisionError:  # If cant, default to 0
            self._avg_breakd_time = 0

    def breakdowns(self, turns, min_b, max_b):  # Works out how many times it will break down in the 'day'
        amount = p.poisson(lam=self._ride_reliability, size=1)  # Amount of times it's going to break down
        amount = amount[0]
        self._breakdowns = amount
        if amount == 0:
            return
        else:
            start_times = [-1]
            for i in range(0, amount):
                duration = random.randrange(min_b, max_b)  # How long ride will be broken down for
                start_turn = -1
                while start_turn in start_times:
                    start_turn = random.randrange(3, turns-duration)  # Pick when to breakdown in the range

                start_times.append(start_turn)
                self._bd_schedu.append(Breakdowns(start_turn, duration))

        # Sort list by start time, so it doesn't need to check everytime
        arr = self._bd_schedu
        n = len(arr)
        swapped = True
        if n > 1:
            while swapped:  # Iterate until no swaps done, bubble sort
                for i in range(n-1):
                    for j in range(0, n-i-1):
                        if arr[j].ret_start() > arr[j+1].ret_start():
                            swapped = True
                            arr[j], arr[j + 1] = arr[j + 1], arr[j]
                        else:
                            swapped = False

    def ret_bd_stats(self):  # Return information related to breakdowns
        array = self._bd_schedu
        if len(array) > 0:  # If breakdowns, act as normal
            return self._bd_schedu[0], self._bd_status, self._bd_time
        elif len(array) == 0:  # If no breakdowns
            return -1, self._bd_status, self._bd_time

    def set_bd_time(self, value):
        self._bd_time = value

    def set_bd_status(self, value):
        self._bd_status = value

    def rem_breakdown(self):  # Remove the first breakdown in the array
        self._bd_schedu.pop(0)

    def upd_bd_time(self):  # Updates the breakdown time left on a ride
        self._bd_time -= 1

    def wait_time(self):  # Works out the wait time after every turn
        q_size = self._queues.queue_time()
        wait_time = (q_size // self._ride_cap) * self._ride_time  # Calculates the wait time
        self._current_wait = wait_time

    def ret_wait_time(self):
        return self._current_wait

    def ret_ride_queues(self):  # Return ride queues and infomation
        return self._queues.ret_queue(), self._queues.ret_ride(), self._ride_cap, self._current_riders, self._queues.ret_fast()

    def ret_check_ride(self):
        return self._name, self._ride_time, self._ride_turn

    def queues_empty(self):  # Returns True if rides queue is empty
        queue = self._queues.ret_queue().empty()
        fp = self._queues.ret_fast().empty()
        return queue and fp

    def ret_ride_info(self):
        return self._name, self._ride_time, self._ride_cap, self._ride_pop, self._ride_type, self._ride_reliability

    def ret_name(self):
        return self._name

    def ret_popular(self):
        return self._ride_pop

    def ret_rt(self):  # Return the rides type
        return self._ride_type

    def ret_fp(self):  # Return queue
        return self._queues.ret_fast()

    def into_queue(self, item):
        self._queues.into_queue(item)
        self._norm_riders += 1  # Increase counter

    def into_fast(self, item):  # Put into fast pass queue
        self._queues.into_fast(item)
        self._fp_riders += 1  # Increase counter

    def onto_ride(self, q_type):
        wait_t = self._queues.onto_ride(q_type)
        self._time_waited += wait_t

    def off_ride(self, park):
        self._queues.off_ride(park)

    def fin_check_ride(self, ride_turn, rq, ride, fp):  # Update attributes after ride_check function
        self._ride_turn = ride_turn
        self._queues.update_queues(rq, fp, ride)

    def upd_curr_riders(self):
        self._current_riders += 1

    def rst_curr_riders(self):
        self._current_riders = 0

    def ret_curr_riders(self):
        return self._current_riders

    def choose_ride_info(self):  # Return info needed for the choose_ride function
        return self._ride_pop, self._current_wait


class Amenity(object):  # Shops/Other services
    def __init__(self, name, time):
        self._name = name
        self._time = time  # Time spent at service
        self._guest_count = 0  # Amount of guests that have used the amenity

    def time_to_spend(self):  # Returns how long guest should spend at amenity
        time = self._time
        if time == 1:
            times = [time, time + 1]  # Means guest cant spend 0 time
        else:
            times = [time-1, time, time+1]  # How long guest can spend at amenity, varying for each
        return random.choice(times)

    def increase_g_count(self):  # Increase guest counter
        self._guest_count += 1

    def ret_g_count(self):
        return self._guest_count

    def ret_name(self):
        return self._name

    def save_attributes(self):
        return self._name, self._time

    def ret_data(self, max_turns):  # Function to return collected data
        average = int(self._guest_count / max_turns)
        return f'{self._name} | {self._guest_count} | {average}'


class Settings(object):  # Object to hold simulation settings
    def __init__(self, guests, turns, fp_ratio):
        self._max_guests = guests
        self._max_turns = turns
        self._fp_ratio = fp_ratio

    def ret_values(self):  # Return all the settings
        return self._max_guests, self._max_turns, self._fp_ratio

    def upd_values(self, data):  # Update all the settings
        self._max_guests, self._max_turns, self._fp_ratio = data

    def ret_max_turns(self):
        return self._max_turns


if __name__ == '__main__':
    print("objects.py")
