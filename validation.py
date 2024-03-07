# Functions to validate inputs

def int_validation(output):  # Validates if an input is an integer
    correct = False
    inp = 0
    while not correct:  # Whilst invalid input
        inp = input(output)  # Take in input
        try:  # Try converting to integer
            inp = int(inp)
            correct = True  # If it can, end iteration
        except ValueError:  # If it cannot, repeat
            print("Invalid input, try again")

    return inp  # Return inputted value


def flt_validation(output):  # Validates input is a float
    correct = False
    inp = 0.0
    while not correct:
        inp = input(output)
        try:
            inp = float(inp)
            correct = True
        except ValueError:
            print("Invalid input, needs to be float, try again")

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


def name_validation(output, array):  # Validates names specifically for making rides/amenities

    if len(array) == 0:  # If list is empty
        return str_validation(output)

    type_names = []
    for i in range(0, len(array)):  # Add ride names to check
        type_names.append(array[i].ret_name().lower())

    while True:  # If not, iterate until valid input
        inp = str_validation(output)
        if inp not in type_names:
            break
        else:
            print("Name already used")

    return inp


if __name__ == '__main__':
    string = str_validation("Test for string: ")
    integer = int_validation("Test for int: ")
