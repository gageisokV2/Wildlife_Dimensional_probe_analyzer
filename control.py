import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import plotter

file_loaded = False
file_path = None
plot_manager = plotter.plot_manager()


def load_file():
    global file_loaded
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        filename_label.config(text="File Loaded:\n" +
                              file_path, wraplength=650)
        view_button.configure(state="normal")
        file_loaded = True


def close_window():
    if file_loaded:
        results, status = parse_data()
        if (status == 0):
            messagebox.showerror(
                "FILE FORMAT ERROR", "Incorrect file format. Each line should have 4 parts:\n(index x: y: z:)" +
                "\nCheck for errors or other out of place elements\nExample valid format for each line:\n198 "+
                "x:125.000 y:63.687 z:27.298")
            load_window.destroy()
        else:
            load_window.destroy()
            plot_manager.assign_data(results)
            plot_manager.create_plots()
    else:
        if messagebox.askokcancel("Quit", "No data was loaded. Quit?"):
            load_window.destroy()


def parse_data():
    global plot_manager
    global file_path
    status = 0
    try:
        with open(file_path, 'r') as file:
            points = []
            for line in file:
                line = line.strip()
                if line.startswith("#"):
                    continue

                parts = line.split()
                if len(parts) != 4:
                    raise ValueError(
                        "Incorrect file format. Each line should have 4 parts (index, x, y, z).")

                index = int(parts[0])
                x = float(parts[1].split(":")[1])
                y = float(parts[2].split(":")[1])
                z = float(parts[3].split(":")[1])

                point = [x, y, z]
                points.append(point)

        points_array = np.array(points)
        status = 1
        return points_array, status

    except FileNotFoundError:
        print("File not found.")

    except ValueError as e:
        print("Error:", str(e))

    return status, status

def example_data():
    load_window.destroy()
    plot_manager.create_plots()

if __name__ == '__main__':

    # Generate random points for an example of the program
    n_points = 1000
    plot_manager.generate_random_points(n_points)

    plot_manager.delaunay_triangulation(100)

    # plot_manager.assign_data(results)

    # Create the GUI window
    load_window = tk.Tk()
    load_window.title("Data Viewer Loader")
    # Get the screen width and height
    screen_width = load_window.winfo_screenwidth()
    screen_height = load_window.winfo_screenheight()

    # Calculate the x and y coordinates for the window to be centered
    # Adjust 700 based on your window width
    x = int((screen_width / 2) - (700 / 2))
    # Adjust 400 based on your window height
    y = int((screen_height / 2) - (400 / 2))

    # Set the window's position
    load_window.geometry(f"700x400+{x}+{y}")

    # Configure window background color
    load_window.configure(bg="#36393F")

    # Create a label to display the filename
    filename_label = tk.Label(load_window, text="Please select a valid .txt file for loading.\nAny .txt file from the Wildlife Dimensional Probe should be valid",
                              bg="#36393F", fg="#FFFFFF", font=("Arial", 12, "bold"))
    filename_label.pack(pady=10)

    # Create a button to load the file
    load_button = tk.Button(load_window, text="Load File", command=load_file,
                            bg="#7289DA", fg="#FFFFFF", font=("Arial", 12, "bold"), width=10, height=1)
    load_button.pack(pady=10)

    # Create a close button (hidden initially)
    view_button = tk.Button(load_window, text="View Data", command=close_window,
                            bg="#8D7625", fg="#FFFFFF", font=("Arial", 12, "bold"), width=10, height=1)
    view_button.pack(padx=10, pady=10)
    view_button.configure(state="disabled")

    # create a button to show example data
    example_button = tk.Button(load_window, text="See Example 3x3 Inch Cube", command=example_data,
                            bg="#8D7625", fg="#FFFFFF", font=("Arial", 12, "bold"), width=25, height=1)
    example_button.pack(side=tk.LEFT, anchor=tk.SW, padx=10, pady=10)

    load_window.protocol("WM_DELETE_WINDOW", close_window)

    # Start the GUI event loop
    load_window.mainloop()
