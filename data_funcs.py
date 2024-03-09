# Functions to display data at the end

def prin_basic_data(guest_list, rides, amenities, max_turns):  # Prints out basic sim data
    # Average total wait time
    total_t = 0
    for i in guest_list:
        total_t += i.ret_time()

    # Average rides ridden
    total_r = 0
    for i in guest_list:
        total_r += i.ret_rides_ridden()

    print(f"avg total wait time = {total_t / len(guest_list)}")
    print(f"avg wait per ride = {(total_t / len(guest_list)) / (total_r / len(guest_list))}")
    print(f"avg rides ridden = {total_r / len(guest_list)}")


def gen_stats(guest_list, rides, amenities):  # Calculates all the stats for final screen
    # Average rides ridden
    total_r = 0
    for i in guest_list:
        total_r += i.ret_rides_ridden()
    total_r = round(total_r / len(guest_list), 2)

    # Average amenities used
    total_a = 0
    for i in guest_list:
        total_a += i.ret_am_used()
    total_a = round(total_a / len(guest_list), 2)

    # Average total wait time
    total_t = 0
    for i in guest_list:
        total_t += i.ret_time()
    total_t = round(total_t / len(guest_list), 2)

    return f'{total_r} | {total_a} | {total_t}'
