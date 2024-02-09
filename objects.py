# Object file, containing all the class declarations and methods

import queue as q
import random


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
        self._wait_time = 0
        self._rides_ridden = 0
        self._rides = []  # Array of the rides ridden
        self._queue_status = 0
        # 0=not in anything, 1=in park, 2=in queue, 3=on ride, 4=just off ride, 5=in amenity, -1=leaving park, -2=gone from park
        self._personality = -1
        # -1=unassigned, 0=average, 1=enthusiast, 2=tame, 3=thrillseeker, 4=child
        self._time_left = 0  # Time left to spend at amenity

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
        # q_type: 0 = normal, 1 = fast pass
        match q_type:
            case 0:  # If coming from normal queue
                print("loading from normal")
                guest = self._queue.get_nowait()
                guest.change_status(3)
                self._ride.put_nowait(guest)

            case 1:  # If coming from fast pass queue
                print("loading from fp")
                guest = self._fast_queue.get_nowait()
                guest.change_status(3)
                self._ride.put_nowait(guest)

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


class Ride(object):
    def __init__(self, name, rl, rc, rp, rt):
        self._name = name
        self._ride_time = rl  # How long ride lasts
        self._ride_cap = rc  # How many people fit on ride
        self._ride_pop = rp  # Ride popularity
        self._ride_type = rt
        # 0=kids, 1=small coaster, 2=small flat, 3=dark, 4=big flat, 5=big coasts, 6=insane
        self._queues = RQueues()
        self._ride_turn = 0
        self._current_riders = 0
        self._current_wait = 0

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
        return self._name, self._ride_time, self._ride_cap, self._ride_pop, self._ride_type

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

    def into_fast(self, item):  # Put into fast pass queue
        self._queues.into_fast(item)

    def onto_ride(self, q_type):
        self._queues.onto_ride(q_type)

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

    def time_to_spend(self):  # Returns how long guest should spend at amenity
        time = self._time
        if time == 1:
            times = [time, time + 1]  # Means guest cant spend 0 time
        else:
            times = [time-1, time, time+1]  # How long guest can spend at amenity, varying for each
        return random.choice(times)

    def ret_name(self):
        return self._name


if __name__ == '__main__':
    print("objects.py")
