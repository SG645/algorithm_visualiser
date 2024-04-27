import tkinter as tk
from PIL import Image, ImageTk
import time
from tkinter import PhotoImage
import itertools
import os
import math

# Define the window
root = tk.Tk()
root.title("Travelling Salesman Problem (Backtracking)")

# Define the canvas
canvas_width = 800
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Get the current working directory
current_dir = os.getcwd()

# Open the original image
original_image = Image.open("building.png")

# Resize the image to 30% of its original size
new_width = int(original_image.width * 0.06)
new_height = int(original_image.height * 0.06)
resized_image = original_image.resize((new_width, new_height))

# Save the resized image in a supported format (e.g., PNG)
resized_image.save(os.path.join(current_dir, "building_converted.png"), "PNG")

# Load the converted building image
building_image = PhotoImage(file=os.path.join(current_dir, "building_converted.png"))

# Create a grass background image
grass_image = Image.new("RGB", (canvas_width, canvas_height), color=(0, 128, 0))  # Green color
grass_image_tk = ImageTk.PhotoImage(grass_image)

# Set the grass background image on the canvas
canvas.create_image(0, 0, anchor=tk.NW, image=grass_image_tk)

# Define a function to get user input for the number of cities
def get_num_cities():
    def submit():
        global num_cities
        num_cities = int(num_cities_entry.get())
        input_window.destroy()
        get_distances()

    input_window = tk.Toplevel(root)
    input_window.title("Enter Number of Cities")
    label = tk.Label(input_window, text="Enter the number of cities:")
    label.pack(pady=10)
    num_cities_entry = tk.Entry(input_window)
    num_cities_entry.pack(pady=5)
    submit_button = tk.Button(input_window, text="Submit", command=submit)
    submit_button.pack(pady=10)

# Define a function to get user input for distances between cities
def get_distances():
    def submit():
        global distances
        distances = []
        for i in range(num_cities):
            row = []
            for j in range(num_cities):
                if i == j:
                    row.append(0)
                else:
                    row.append(int(entries[i][j].get()))
            distances.append(row)
        distances_window.destroy()
        run_tsp()

    distances_window = tk.Toplevel(root)
    distances_window.title("Enter Distances Between Cities")
    label = tk.Label(distances_window, text="Enter the distances between cities:")
    label.pack(pady=10)

    entries = []
    for i in range(num_cities):
        row_entries = []
        row_label = tk.Label(distances_window, text=f"Distances from city {i+1} to all other cities:")
        row_label.pack()
        for j in range(num_cities):
            if i == j:
                entry = tk.Label(distances_window, text="0", width=3, borderwidth=1, relief="sunken")
            else:
                entry = tk.Entry(distances_window, width=3)
            entry.pack(side=tk.LEFT)
            row_entries.append(entry)
        entries.append(row_entries)

    submit_button = tk.Button(distances_window, text="Submit", command=submit)
    submit_button.pack(pady=10)

# Define the Travelling Salesman Algorithm (Backtracking)
def travelling_salesman_backtracking():
    # Generate all possible permutations of city indices
    permutations = list(itertools.permutations(range(num_cities)))
    min_distance = float('inf')
    best_path = None

    # Iterate over all permutations
    for permutation in permutations:
        # Calculate the total distance for the current permutation
        total_distance = sum(distances[permutation[i]][permutation[i - 1]] for i in range(len(permutation)))
        total_distance += distances[permutation[-1]][permutation[0]]  # Add the distance from the last city to the first city

        # Draw the current path and display its distance on the canvas
        for i in range(len(permutation)):
            start_city = permutation[i]
            end_city = permutation[(i + 1) % num_cities]
            start_x, start_y = city_coords[start_city]
            end_x, end_y = city_coords[end_city]
            canvas.create_line(start_x, start_y, end_x, end_y, fill="gray", width=2)
            canvas.create_text((start_x + end_x) // 2, (start_y + end_y) // 2, text=str(distances[start_city][end_city]), fill="black", font=("Arial", 10))
        canvas.update()
        time.sleep(0.5)  # Adjust the delay to control the animation speed

        # Update the minimum distance and best path if a shorter path is found
        if total_distance < min_distance:
            min_distance = total_distance
            best_path = permutation

    # Draw the best path
    for i in range(len(best_path)):
        start_city = best_path[i]
        end_city = best_path[(i + 1) % num_cities]
        start_x, start_y = city_coords[start_city]
        end_x, end_y = city_coords[end_city]
        canvas.create_line(start_x, start_y, end_x, end_y, fill="red", dash=(4, 4), width=4)  # Bolder red line for the best path
        canvas.update()
        time.sleep(0.5)  # Increase the delay for slower animation

    # Print the minimum distance on the canvas
    canvas.create_text(canvas_width // 2, 20, text=f"Minimum Distance: {min_distance}", fill="black", font=("Arial", 16))

# Define a function to run the TSP
def run_tsp():
    # Clear the canvas
    canvas.delete("all")

    # Draw the cities on the canvas
    radius = min(canvas_width, canvas_height) // 3  # Adjust the radius as needed
    center_x, center_y = canvas_width // 2, canvas_height // 2

    global city_coords
    city_coords = []
    for i in range(num_cities):
        angle = 2 * math.pi * i / num_cities
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        city_coords.append((x, y))

    for i, (x, y) in enumerate(city_coords):
        canvas.create_image(x, y, image=building_image)
        canvas.create_text(x, y + 20, text=f"City{i+1}", fill="blue")  # Display city names

    # Run the Travelling Salesman Algorithm (Backtracking)
    travelling_salesman_backtracking()

# Get user input for the number of cities
get_num_cities()

# Run the Tkinter event loop
root.mainloop()