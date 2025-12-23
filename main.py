import tkinter as tk
from tkinter import ttk

# Create the main window
window = tk.Tk()
window.title("Kalman Filter Tracking")
window.geometry("1200x800")
window.configure(bg="white")

# Create a square border around the window
border = ttk.Frame(window, width=1200, height=800, style="Square.TFrame")
border.place(x=0, y=0)


# Create a title on the window
title_label = tk.Label(window, text="Kalman Filter Tracking", font=("Arial", 20))
title_label.pack(pady=10)


# Create a button to quit the program
quit_button = ttk.Button(window, text="Quit", command=window.destroy)
quit_button.pack(pady=10)



# Create a Canvas widget where the square will be drawn
# The canvas dimensions are set here
canvas = tk.Canvas(border, width=1200, height=800, bg='white')
canvas.pack(pady=20)

# Define the coordinates for the squares
# (x1, y1) are the top-left corner coordinates 
# (x2, y2) are the bottom-right corner coordinates 
# The difference between x2 and x1 must equal the difference between y2 and y1 for a perfect square
side_length = 100
gap = 20  # Gap between front and back rectangles

# Car position (center point of the car unit)
car_x, car_y = 300, 300

# Shared velocity for the car unit
dx, dy = 4, 3  # Horizontal and vertical velocity

# Track which rectangle is in front (True = red is front, False = blue is front)
red_is_front = True

# Initial positions (will be calculated based on direction)
x1_red = 0
y1_red = 0
x2_red = 0
y2_red = 0

x1_blue = 0
y1_blue = 0
x2_blue = 0
y2_blue = 0

# Draw the red rectangle
red_rectangle = canvas.create_rectangle(
    0, 0, side_length, side_length,
    fill="red",      # Fill color of the square
    outline="black", # Outline color
    width=2          # Outline width
)

# Draw the blue rectangle
blue_rectangle = canvas.create_rectangle(
    0, 0, side_length, side_length,
    fill="blue",      # Fill color of the square
    outline="black", # Outline color
    width=2          # Outline width
)

# Canvas dimensions
canvas_width = 1200
canvas_height = 800

# Function to calculate rectangle positions based on direction and which is front
def calculate_positions():
    global car_x, car_y, dx, dy, red_is_front
    global x1_red, y1_red, x2_red, y2_red
    global x1_blue, y1_blue, x2_blue, y2_blue
    
    # Determine front and back offsets based on direction of travel
    # Front should be in the direction of movement
    if abs(dx) > abs(dy):  # Moving more horizontally
        if dx > 0:  # Moving right
            front_offset_x = side_length + gap
            front_offset_y = 0
            back_offset_x = -(side_length + gap)
            back_offset_y = 0
        else:  # Moving left
            front_offset_x = -(side_length + gap)
            front_offset_y = 0
            back_offset_x = side_length + gap
            back_offset_y = 0
    else:  # Moving more vertically
        if dy > 0:  # Moving down
            front_offset_x = 0
            front_offset_y = side_length + gap
            back_offset_x = 0
            back_offset_y = -(side_length + gap)
        else:  # Moving up
            front_offset_x = 0
            front_offset_y = -(side_length + gap)
            back_offset_x = 0
            back_offset_y = side_length + gap
    
    # Position rectangles based on which is front
    if red_is_front:
        # Red is front, blue is back
        x1_red = car_x + front_offset_x
        y1_red = car_y + front_offset_y
        x2_red = x1_red + side_length
        y2_red = y1_red + side_length
        
        x1_blue = car_x + back_offset_x
        y1_blue = car_y + back_offset_y
        x2_blue = x1_blue + side_length
        y2_blue = y1_blue + side_length
    else:
        # Blue is front, red is back
        x1_blue = car_x + front_offset_x
        y1_blue = car_y + front_offset_y
        x2_blue = x1_blue + side_length
        y2_blue = y1_blue + side_length
        
        x1_red = car_x + back_offset_x
        y1_red = car_y + back_offset_y
        x2_red = x1_red + side_length
        y2_red = y1_red + side_length

# Function to animate the car (both rectangles moving together)
def animate():
    global car_x, car_y, dx, dy, red_is_front
    
    # Update car center position
    car_x += dx
    car_y += dy
    
    # Calculate positions based on current direction
    calculate_positions()
    
    # Check boundaries and bounce for the car unit
    # Determine which rectangle is currently in front
    front_x1 = x1_red if red_is_front else x1_blue
    front_x2 = x2_red if red_is_front else x2_blue
    front_y1 = y1_red if red_is_front else y1_blue
    front_y2 = y2_red if red_is_front else y2_blue
    
    # Check horizontal boundaries
    if front_x1 <= 0 or front_x2 >= canvas_width:
        dx = -dx  # Reverse horizontal direction
        red_is_front = not red_is_front  # Flip orientation
        # Adjust car position to stay within bounds
        if front_x1 <= 0:
            car_x = side_length + gap
        else:
            car_x = canvas_width - side_length - gap
        # Recalculate positions with new orientation
        calculate_positions()
    
    # Check vertical boundaries
    if front_y1 <= 0 or front_y2 >= canvas_height:
        dy = -dy  # Reverse vertical direction
        red_is_front = not red_is_front  # Flip orientation
        # Adjust car position to stay within bounds
        if front_y1 <= 0:
            car_y = side_length
        else:
            car_y = canvas_height - side_length
        # Recalculate positions with new orientation
        calculate_positions()
    
    # Move both rectangles to their new positions
    canvas.coords(red_rectangle, x1_red, y1_red, x2_red, y2_red)
    canvas.coords(blue_rectangle, x1_blue, y1_blue, x2_blue, y2_blue)
    
    # Schedule the next animation frame (approximately 30 FPS)
    window.after(33, animate)

# Initialize positions before starting animation
calculate_positions()
canvas.coords(red_rectangle, x1_red, y1_red, x2_red, y2_red)
canvas.coords(blue_rectangle, x1_blue, y1_blue, x2_blue, y2_blue)

# Start the animation
animate()

# Start the main loop to keep the window open
window.mainloop()