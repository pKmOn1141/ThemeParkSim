# Functions to display data at the end

def prin_basic_data(guest_list, rides):  # Prints out basic sim data
    # Average wait time
    total_t = 0
    for i in guest_list:
        total_t += i.ret_time()
    total_r = 0
    for i in guest_list:
        total_r += i.ret_rides_ridden()

    for i in rides:
        print(i.ret_wait_time())

    print(f"avg total wait time = {total_t / len(guest_list)}")
    print(f"avg wait per ride = {(total_t / len(guest_list)) / (total_r / len(guest_list))}")
    print(f"avg rides ridden = {total_r / len(guest_list)}")
