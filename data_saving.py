# Functions to save/load data into persistant storage

from objects import Ride, Amenity
from validation import str_validation
import re
import ast


def collect_type(array):  # Collect attributes out of the objects, storing them in array
    all_info = []

    for item in array:  # Iterate through each object, taking attributes
        curr_info = [item.save_attributes()]
        all_info.append(curr_info)

    return all_info


def write_to_file(data, file_name):  # Write saved data into the file

    file = open(file_name, 'a')

    for item in data:
        file.write(f'{str(item)},')

    file.write("\n")
    file.close()


def save_to_file(rides, amenities, settings, file_name, e_l):  # Combine all the saving functions into one
    settings = settings.ret_values()  # Take values from object
    print(file_name)

    file_name = file_name + ".txt"
    try:
        file = open(file_name, 'r')
        e_l.config(text="File name already exists, try another")
        print("File name already exists, try again.")
        file.close()
    except FileNotFoundError:
        file = open(file_name, 'w')
        file.close()

        write_to_file(collect_type(rides), file_name)
        write_to_file(collect_type(amenities), file_name)
        write_to_file(settings, file_name)

        e_l.config(text="Data saved to file", fg="green")
        print("Finished saving data")


def convert_from_str(data):  # Turn the string data into a workable array
    pattern = r'\[.*?\]'  # Pattern to compare string with
    matches = re.findall(pattern, data)  # Find all matches of the pattern in the string
    result_array = [ast.literal_eval(match) for match in matches]  # Convert each match into an array

    return result_array


def create_objects(info, array, o_t):  # Creates the objects with the data from the save file
    match o_t:
        case "R":  # If making a ride object
            for curr_obj in range(0, len(info)):
                obj = info[curr_obj][0]
                array.append(Ride(obj[0], obj[1], obj[2], obj[3], obj[4], obj[5]))
        case "A":  # If making an amenity object
            for curr_obj in range(0, len(info)):
                obj = info[curr_obj][0]
                array.append(Amenity(obj[0], obj[1]))


def import_settings(data):  # Turn the extracted settings string into individual variables
    # Put the string data into an array, making each value its required data type
    array = [float(x) if '.' in x else int(x) for x in data.split(',') if x.strip()]

    max_guests, max_turns, fp_ratio = array  # Create each variable for the settings

    return max_guests, max_turns, fp_ratio


def read_from_file(file_name, r_array, a_array, settings, e_l):  # Combines all loading functions
    try:
        file_name = file_name + ".txt"
        file = open(file_name, 'r')

        # Extracting all the data types
        extracted_r = file.readline()
        extracted_a = file.readline()
        extracted_s = file.readline()
        file.close()

        # Converts the information into a tuple, so it can be handled individually
        ride_info = convert_from_str(extracted_r)
        amenity_info = convert_from_str(extracted_a)

        # Create the objects
        create_objects(ride_info, r_array, "R")
        create_objects(amenity_info, a_array, "A")

        # Turn the extracted settings into required data types and variables
        settings.upd_values(import_settings(extracted_s))
        e_l.config(text="Data loaded", fg="green")
        print("Data loaded")

    except:  # If there is any problem whatsoever
        print("Unable to load information, setting values to default")
        e_l.config(text="Unable to load info, setting values to default", fg="red")
        settings.upd_values([0, 0, 0])


if __name__ == '__main__':
    print("data_saving.py")
