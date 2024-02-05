# Functions to validate inputs

def int_validation(output):  # Validates if an input is an integer
    correct = False
    inp = 0
    while not correct:
        inp = input(output)
        try:
            inp = int(inp)
            correct = True
        except ValueError:
            print("Invalid input, try again")

    return inp


def str_validation(output):  # Validates that an input is a string
    correct = False
    inp = ""
    while inp == "" or not correct:
        inp = input(output).strip()
        try:
            inp = str(inp)
            correct = True
        except ValueError:
            print("Invalid input, try again")

    return inp


def name_validation(output, rides):  # Validates names specifically for making rides

    if len(rides) == 0:  # If list is empty
        return str_validation(output)

    ride_names = []
    for i in range(0, len(rides)):  # Add ride names to check
        ride_names.append(rides[i].ret_name().lower())

    while True:  # If not, iterate until valid input
        inp = str_validation(output)
        if inp not in ride_names:
            break
        else:
            print("Name already used")

    return inp


if __name__ == '__main__':
    string = str_validation("Test for string: ")
    integer = int_validation("Test for int: ")
