# Code for gui

import tkinter as tk
from objects import Ride, Amenity
from data_saving import save_to_file, read_from_file
from simulation import simulation
from data_funcs import gen_stats

BG_COLOR = "#b3b3b3"


def main_menu(rides, amenities, settings, min_break, max_break):  # Main meunu window
    # Creating the main window
    root = tk.Tk()
    root.title("Theme Park Sim - Main Menu")
    root.geometry("600x400")
    root.configure(bg=BG_COLOR)

    # Create center frame for buttons
    center_frame = tk.Frame(root)
    center_frame.pack(expand=True, fill=tk.BOTH)

    buttons = [
        ("Edit rides", lambda: edit_object("R", rides)),
        ("Edit amenities", lambda: edit_object("A", amenities)),
        ("Edit settings", lambda: edit_settings(settings)),
        ("Save/Load settings", lambda: save_load_window(rides, amenities, settings)),
        ("Start sim", lambda: start_sim(root, rides, amenities, settings, min_break, max_break))
    ]

    # Calculate size of buttons
    max_text_length = max(len(text) for text, _ in buttons)
    button_height = 2
    button_width = max_text_length + 2

    # Create buttons
    for i, (text, command) in enumerate(buttons):
        btn = tk.Button(center_frame, text=text, command=command, height=button_height, width=button_width, padx=10, pady=100)
        btn['font'] = ('Ariel', 15)
        btn.grid(row=i, column=0, sticky="ew")
        center_frame.grid_rowconfigure(i, weight=1, uniform="buttons")
        center_frame.grid_columnconfigure(0, weight=1, uniform="buttons")

    root.mainloop()


def edit_object(e_t, t_array):  # Screen to edit either rides or amenities
    # Set variables to tell if something isn't working
    title_name = "error"
    o_type = "error"
    c_names = "error"
    # Check which type to use
    match e_t:
        case "R":
            title_name = "Rides"
            o_type = "Ride"
            c_names = "Name, Time, Cap, Popularity, Type, Avg breakdowns"
        case "A":
            title_name = "Amenities"
            o_type = "Amenity"
            c_names = "Name, Avg time spent"

    # Creating window
    root = tk.Tk()
    root.geometry("600x400")
    root.title(f'Editing {title_name}')
    root.configure(bg=BG_COLOR)

    # Frame to hold buttons with padding
    button_frame = tk.Frame(root, padx=12, pady=20, bg=BG_COLOR)
    button_frame.pack(side=tk.LEFT, fill=tk.Y)

    # Left hand buttons
    button1 = tk.Button(button_frame, text=f'Add {o_type}', width=15, height=3)
    button1.pack(side=tk.TOP, pady=10)
    match e_t:  # Edit the functionality of button1 depending on what type
        case "R":
            button1.config(command=lambda: add_ride_window(t_array, text_box, c_names))
        case "A":
            button1.config(command=lambda: add_amenity_window(t_array, text_box, c_names))

    button2 = tk.Button(button_frame, text=f'Remove {o_type}', width=15, height=3, command=lambda: remove_obj_window(t_array, e_t, text_box, c_names))
    button2.pack(side=tk.TOP, pady=10)
    button3 = tk.Button(button_frame, text="Go back", width=15, height=3, command=lambda: go_back(root))
    button3.pack(side=tk.BOTTOM, pady=10)

    # Frame for the box with black outline
    box_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
    box_frame.place(relx=0.6, rely=0.5, anchor=tk.CENTER, relwidth=0.75, relheight=0.9)
    # Text widget in box
    text_box = tk.Text(box_frame, wrap="word", bg="white")
    text_box.pack(fill=tk.BOTH, expand=True)

    update_text_box(c_names, t_array, text_box)

    root.mainloop()


def update_text_box(column_names, t_array, text_box):  # Updates data in the text box
    text_box.delete('1.0', tk.END)  # Cleares text box first
    text_box.insert(tk.END, f'{column_names}\n')
    for curr in t_array:
        text_box.insert(tk.END, f'{curr.save_attributes()}\n')


def save_added_object(o_array, entry_boxes, o_type, c_n, txt_b, root, er_l):
    names = []
    for i in o_array:  # Make a list of all the used ride names
        names.append(i.ret_name())

    data = []
    name = entry_boxes[0].get()
    if name not in names:  # If name not already used
        try:
            for count, entry in enumerate(entry_boxes):  # Get data
                if count == 0:
                    data.append(entry.get())
                else:  # Convert the numbers into integers
                    data.append(int(entry.get()))

            match o_type:
                case "R":
                    o_array.append(Ride(data[0], data[1], data[2], data[3], data[4], data[5]))  # Create ride object
                    update_text_box(c_n, o_array, txt_b)
                    print("Ride added")
                case "A":
                    o_array.append(Amenity(data[0], data[1]))
                    update_text_box(c_n, o_array, txt_b)
                    print("Amenity added")

            root.destroy()
        except:  # If any issue with inputs happen
            er_l.config(text="Invalid inputs", fg="red")  # Activate error message
            print("Invalid inputs")

    else:  # If name already used
        er_l.config(text="Name already used", fg="red")  # Activate error message


def add_ride_window(rides, text_box, c_n):  # Menu for adding a new ride

    root = tk.Tk()
    root.title("Add Ride")
    root.config(bg=BG_COLOR)

    # Create a frame to hold the input boxes and button
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(padx=10, pady=10)

    # Custom labels' text
    entry_labels = ["Ride name:", "Ride time:", "Ride cap:", "Ride popularity:", "Ride type:", "Avg breakdowns:"]

    # Create 6 input boxes
    entry_boxes = []
    for i, text in enumerate(entry_labels):
        label = tk.Label(frame, text=text, bg=BG_COLOR)
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry_boxes.append(entry)

    # Create button to confirm input
    confirm_button = tk.Button(root, text="Confirm", command=lambda: save_added_object(rides, entry_boxes, "R", c_n, text_box, root, error_label))
    confirm_button.pack(pady=10)

    error_label = tk.Label(root, fg="red", bg=BG_COLOR)
    error_label.pack()

    root.mainloop()


def add_amenity_window(amenities, txt_box, c_n):

    root = tk.Tk()
    root.title("Add Amenity")
    root.config(bg=BG_COLOR)

    # Create a frame to hold the input boxes and button
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(padx=10, pady=10)

    # Custom labels' text
    entry_labels = ["Amenity name:", "Time spent at amenity:"]

    # Create boxes
    entry_boxes = []
    for i, text in enumerate(entry_labels):
        label = tk.Label(frame, text=text, bg=BG_COLOR)
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry_boxes.append(entry)

    # Create button to confirm input
    confirm_button = tk.Button(root, text="Confirm", command=lambda: save_added_object(amenities, entry_boxes, "A", c_n, txt_box, root, error_label))
    confirm_button.pack(pady=10)

    error_label = tk.Label(root, fg="red", bg=BG_COLOR)
    error_label.pack()

    root.mainloop()


def remove_obj_window(t_array, o_type, textbox, c_n):  # Window to remove ride/amenity
    title = "error"
    match o_type:
        case "R":
            title = "Ride"
        case "A":
            title = "Amenity"

    def remove_object(t_array, title):
        names = []
        for curr in t_array:
            names.append(curr.ret_name())

        name = entry.get()
        if name not in names:  # If name not found
            error_label.config(text=f'{title} not found')
        else:
            for current in range(0, len(t_array)):
                if t_array[current].ret_name().lower() == name.lower():
                    t_array.remove(t_array[current])
                    update_text_box(c_n, t_array, textbox)
                    root.destroy()
                    print("removed ride")
                    break

    root = tk.Tk()
    root.title(f'Remove {title}')
    root.config(bg=BG_COLOR)

    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text=f'{title} name:', bg=BG_COLOR)
    label.grid(row=0, column=0, padx=5, pady=5)
    entry = tk.Entry(frame)
    entry.grid(row=0, column=1, padx=5, pady=5)

    confirm_button = tk.Button(root, text="Confirm", command=lambda: remove_object(t_array, title))
    confirm_button.pack(pady=10)

    error_label = tk.Label(root, fg="red", bg=BG_COLOR)
    error_label.pack()

    root.mainloop()


def go_back(root):  # Function for go back buttons
    root.destroy()


def edit_settings(settings):

    root = tk.Tk()
    root.title("Edit Settings")
    root.config(bg=BG_COLOR)

    # Create a frame to hold the input boxes and button
    frame = tk.Frame(root, bg=BG_COLOR)
    frame.pack(padx=10, pady=10)

    # Custom labels' text
    entry_labels = ["Max guests:", "Max Turns:", "FastPass Ratio:"]
    defaults = settings.ret_values()

    # Create boxes
    entry_boxes = []
    for i, text in enumerate(entry_labels):
        label = tk.Label(frame, text=text, bg=BG_COLOR)
        label.grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(frame)
        entry.insert(0, defaults[i])
        entry.grid(row=i, column=1, padx=5, pady=5)
        entry_boxes.append(entry)

    # Create button to confirm input
    confirm_button = tk.Button(root, text="Confirm", command=lambda: save_settings(settings, error_label, entry_boxes, root))
    confirm_button.pack(pady=10)

    error_label = tk.Label(root, fg="red", bg=BG_COLOR)
    error_label.pack()

    root.mainloop()


def save_settings(settings, e_label, e_boxes, root):  # Saves the inputted settings into the object
    valid = False
    data = []
    try:
        for i, entry in enumerate(e_boxes):
            value = entry.get()
            if i == 2:  # Checking last value is a float
                if float(value) < 1:  # If a valid number
                    valid = True
                    data.append(float(value))
                else:
                    valid = False
            else:
                data.append(int(value))
                valid = True

        if valid:
            settings.upd_values(data)
            root.destroy()
            print("Settings saved")
        else:
            e_label.config(text="FastPass Ratio needs to be <1")

    except:
        e_label.config(text="Invalid input")


def get_file_name(txt_box):  # Get the input out of the text box
    file_name = txt_box.get("1.0", "end-1c")
    return file_name


def save_load_window(rides, amenities, settings):
    root = tk.Tk()
    root.title("Save/Load Settings")
    root.config(bg=BG_COLOR)
    root.geometry("400x150")

    # Create a frame for padding
    padding_frame = tk.Frame(root, bg=BG_COLOR)
    padding_frame.pack(padx=10, pady=10)

    # Create label and entry for file name input
    file_label = tk.Label(padding_frame, text="File name:", bg=BG_COLOR)
    file_label.grid(row=0, column=0, sticky="e")

    text_entry = tk.Text(padding_frame, height=2, width=50)
    text_entry.grid(row=0, column=1, padx=10)

    # Create buttons for save, load, and go back
    save_button = tk.Button(root, text="Save Data", command=lambda: save_to_file(rides, amenities, settings, get_file_name(text_entry), error_label))
    save_button.place(relx=0.35, rely=0.5, anchor="center")

    load_button = tk.Button(root, text="Load Data", command=lambda: read_from_file(get_file_name(text_entry), rides, amenities, settings, error_label))
    load_button.place(relx=0.65, rely=0.5, anchor="center")

    go_back_button = tk.Button(root, text="Go Back", command=lambda: go_back(root))
    go_back_button.pack(side="left", padx=20, pady=10, anchor="s")

    error_label = tk.Label(root, fg="red", bg=BG_COLOR)
    error_label.place(relx=0.5, rely=0.8, anchor="center")

    root.mainloop()


def start_sim(menu_window, rides, amenities, settings, min_b, max_b):
    menu_window.destroy()  # Clear menu window

    root = tk.Tk()
    root.title("Simulation In Progress")
    root.config(bg=BG_COLOR)

    simulation_label = tk.Label(root, text="Running Simulation", font=("Arial", 24), bg=BG_COLOR)
    simulation_label.pack(pady=20)

    turn_label = tk.Label(root, text="", font=("Arial", 18), bg=BG_COLOR)
    turn_label.pack()

    root.update()

    fin, guest_list = simulation(rides, amenities, settings, min_b, max_b, turn_label, root)
    if fin:  # If simulation finished
        root.destroy()  # Destory current screen
        data_screen(rides, amenities, settings, guest_list)  # Open menu screen

    root.mainloop()


def update_data_box(column_names, text_box, data, max_turns):  # Updates the data screens text box
    text_box.configure(state='normal')
    text_box.delete('1.0', tk.END)  # Cleares text box first
    text_box.insert(tk.END, f'{column_names}\n')
    for curr in data:
        text_box.insert(tk.END, f'{curr.ret_data(max_turns)}\n')  # Print the objects information
    text_box.configure(state='disabled')


def update_stats_box(column, text_box, guest_list, rides, amenities):  # Updates data screen for stats
    text_box.configure(state='normal')
    text_box.delete('1.0', tk.END)  # Cleares text box first
    text_box.insert(tk.END, f'{column}\n')
    text_box.insert(tk.END, gen_stats(guest_list, rides, amenities))
    text_box.configure(state='disabled')


def show_stats(text_box, guest_list, rides, amenities):  # Deals with the stats screen
    columns = "Avg Rides Ridden | Avg Amenities Used | Avg Total Time Waited"
    update_stats_box(columns, text_box, guest_list, rides, amenities)


def show_data(d_type, text_box, data, max_turns):  # Function to show data based on what button is pressed
    match d_type:
        case "R":
            columns = "Name | Total Riders | Normal/Fastpass ratio | Avg Wait Time | Total Bds | Avg Bd time"
            update_data_box(columns, text_box, data, max_turns)
        case "A":
            columns = "Name | Total Guests Used | Average Guests per Turn"
            update_data_box(columns, text_box, data, max_turns)


def data_screen(rides, amenities, settings, guest_list):
    max_turns = settings.ret_max_turns()

    # Create new window
    root = tk.Tk()
    root.geometry("800x500")
    root.title("Simulation results")
    root.configure(bg=BG_COLOR)

    # Text box
    text_frame = tk.Frame(root, bd=2, relief=tk.SOLID)
    text_frame.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.6)

    text_scrollbar = tk.Scrollbar(text_frame)
    text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_box = tk.Text(text_frame, wrap="word", bg="white", yscrollcommand=text_scrollbar.set)
    text_box.pack(fill=tk.BOTH, expand=True)
    text_box.configure(state='disabled')

    text_scrollbar.config(command=text_box.yview)

    # Buttons
    button_frame = tk.Frame(root, padx=12, pady=20, bg=BG_COLOR)
    button_frame.place(relx=0.25, rely=0.95, anchor=tk.SW)

    button1 = tk.Button(button_frame, text="Rides", width=18, height=4, command=lambda: show_data("R", text_box, rides, max_turns))
    button1.pack(side=tk.LEFT, padx=10, pady=5)

    button2 = tk.Button(button_frame, text="Amenities", width=18, height=4, command=lambda: show_data("A", text_box, amenities, max_turns))
    button2.pack(side=tk.LEFT, padx=10, pady=5)

    button3 = tk.Button(button_frame, text="Stats", width=18, height=4, command=lambda: show_stats(text_box, guest_list, rides, amenities))
    button3.pack(side=tk.LEFT, padx=10, pady=5)

    exit_button = tk.Button(root, text="Exit", width=10, height=2, command=lambda: go_back(root))
    exit_button.place(relx=0.05, rely=0.95, anchor=tk.SW)

    root.mainloop()


if __name__ == '__main__':
    print("gui.py")
