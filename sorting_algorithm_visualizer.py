import pygame
import tkinter
import math
import random

# MenuWindow class for creating the GUI for sorting options
class MenuWindow:
    def __init__(self, root, title, geometry, message):
        # Initialize the root window with a title and geometry
        self.root = root
        self.root.title(title)
        self.root.geometry(geometry)
        tkinter.Label(self.root, text=message).pack()

        # List of sorting algorithms to choose from
        self.options = [
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
            "Merge Sort"
        ]

        # Add "Reset" button
        tkinter.Button(self.root, text="Reset", command=self.reset).pack()
        
        # Add dropdown menu for sorting algorithm options
        self.clicked = tkinter.StringVar()
        self.clicked.set(self.options[0])
        tkinter.OptionMenu(self.root, self.clicked, *self.options).pack()

        # Add radio buttons for ascending/descending sorting
        self.selected = tkinter.IntVar()
        self.selected.set(1)
        tkinter.Radiobutton(self.root, text="Ascending", variable=self.selected, value=1).pack()
        tkinter.Radiobutton(self.root, text="Descending", variable=self.selected, value=2).pack()

        # Add "Start Sort" button
        tkinter.Button(self.root, text="Start Sort", command=self.start_sort).pack()

        # Disable the ability to close the window through the X button
        self.root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Start the sorting algorithm
    def start_sort(self):
        global sorting_algorithm, sorting_algorithm_generator, is_ascending, is_sorting
        is_ascending = self.selected.get() == 1
        if self.clicked.get() == "Bubble Sort" and not is_sorting:
            is_sorting = True
            sorting_algorithm = bubble_sort
            sorting_algorithm_generator = sorting_algorithm(draw_info, is_ascending)
        if self.clicked.get() == "Selection Sort" and not is_sorting:
            is_sorting = True
            sorting_algorithm = selection_sort
            sorting_algorithm_generator = sorting_algorithm(draw_info, is_ascending)
        if self.clicked.get() == "Insertion Sort" and not is_sorting:
            is_sorting = True
            sorting_algorithm = insertion_sort
            sorting_algorithm_generator = sorting_algorithm(draw_info, is_ascending)
        if self.clicked.get() == "Merge Sort" and not is_sorting:
            is_sorting = True
            sorting_algorithm = merge_sort
            sorting_algorithm_generator = sorting_algorithm(draw_info, is_ascending)

    # Reset the sorting algorithm and generate new data
    def reset(self):
        global is_sorting, draw_info
        is_sorting = False
        self.values_list = generate_starting_list(num_vals, min_val, max_val)
        draw_info.set_list(self.values_list)

# DrawInformation class for storing and updating information for drawing the list
class DrawInformation:
    BACKGROUND_COLOR = 230, 230, 230
    def __init__(self, title, window_width, window_height, values_list):
        self.window_width = window_width
        self.window_height = window_height
        self.window = pygame.display.set_mode((window_width, window_height))
        self.set_list(values_list)
        pygame.display.set_caption(title)
    
    # Set the list of elements and size of elements
    def set_list(self, values_list):
        self.values_list = values_list
        self.min_val = min(values_list)
        self.max_val = max(values_list)
        self.block_width = round((self.window_width) / len(values_list))
        self.block_height = math.floor((self.window_height) / (self.max_val - self.min_val))

# Draw the list of elements
def draw(drawing_information):
    drawing_information.window.fill(drawing_information.BACKGROUND_COLOR)
    draw_list(drawing_information)
    pygame.display.update()

# Draw the elements of the list, with optional colors and background clearing
def draw_list(drawing_information, color_positions={}, clear_bg=False):
    values_list = drawing_information.values_list

    if clear_bg:
        clear_rect = (0, 0, drawing_information.window_width, drawing_information.window_height)
        drawing_information.window.fill(drawing_information.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(values_list):
        color = (199, 199, 199) if i not in color_positions else color_positions[i]
        x = i * drawing_information.block_width
        y = (drawing_information.max_val - val) * drawing_information.block_height
        rect = (x, y, drawing_information.block_width, val * drawing_information.block_height)
        pygame.draw.rect(drawing_information.window, color, rect)

        for j in range(3):
            pygame.draw.rect(drawing_information.window, (80, 80, 80),
                             (x - j, y - j, drawing_information.block_width, drawing_information.window_height), 1)

# Generate a starting list of values with a specified number of values, minimum value, and maximum value
def generate_starting_list(num_vals, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(num_vals)]

def bubble_sort(draw_info, ascending=True):
    values_list = draw_info.values_list

    for i in range(len(values_list) - 1):
        for j in range(len(values_list) - 1 - i):
            if (values_list[j] > values_list[j + 1] and ascending) or (values_list[j] < values_list[j + 1] and not ascending):
                values_list[j], values_list[j + 1] = values_list[j + 1], values_list[j]
                draw_list(draw_info, {j: (0, 255, 0), j + 1: (255, 0, 0)}, True)
            yield True

    return values_list

def selection_sort(draw_info, ascending=True):
    values_list = draw_info.values_list

    for i in range(0, len(values_list) - 1):
        cur_min_idx = i
        for j in range(i, len(values_list)):
            if (values_list[j] < values_list[cur_min_idx] and ascending) or (values_list[j] > values_list[cur_min_idx] and not ascending):
                cur_min_idx = j
            draw_list(draw_info, {i: (0, 255, 0), cur_min_idx: (255, 0, 0)}, True)
        values_list[i], values_list[cur_min_idx] = values_list[cur_min_idx], values_list[i]
        yield True
        
    return values_list

def insertion_sort(draw_info, ascending=True):
    values_list = draw_info.values_list

    for i in range(1, len(values_list)):
        j = i
        while (values_list[j - 1] > values_list[j] and j > 0 and ascending) or (values_list[j - 1] < values_list[j] and j > 0 and not ascending):
            values_list[j - 1], values_list[j] = values_list[j], values_list[j - 1]
            draw_list(draw_info, {j: (0, 255, 0), j - 1: (255, 0, 0)}, True)
            j -= 1
            yield True
    
    return values_list

def merge_sort(draw_info, ascending=True):
    values_list = draw_info.values_list

    if len(values_list) <= 1:
        return values_list
    
    current_size = 1
    while current_size < len(values_list):
        for left in range(0, len(values_list), 2*current_size):
            mid = left + current_size - 1
            right = min(left + 2*current_size - 1, len(values_list) - 1)
            left_half = values_list[left:mid+1]
            right_half = values_list[mid+1:right+1]
            i, j, k = 0, 0, left
            while i < len(left_half) and j < len(right_half):
                if (left_half[i] <= right_half[j] and ascending) or (left_half[i] >= right_half[j] and not ascending):
                    values_list[k] = left_half[i]
                    i += 1
                else:
                    values_list[k] = right_half[j]
                    j += 1

                k += 1
                draw_list(draw_info, {k: (255,0,0)}, True)
                yield True

            while i < len(left_half):
                values_list[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                values_list[k] = right_half[j]
                j += 1
                k += 1

        current_size *= 2
    
    return values_list

def main():
    global num_vals, min_val, max_val, is_sorting, is_ascending, draw_info, sorting_algorithm, sorting_algorithm_generator

    run = True
    clock = pygame.time.Clock()
    num_vals = 100
    min_val = 0
    max_val = 100
    is_sorting = False
    is_ascending = True

    sorting_algorithm = None
    sorting_algorithm_generator = None

    pygame.init()
    values_list = generate_starting_list(num_vals, min_val, max_val)
    draw_info = DrawInformation("Sorting Algorithm Visualizer", 1000, 600, values_list)

    root = tkinter.Tk()
    menu_window = MenuWindow(root, "Sorting Alogrithm Controller", '400x500', "Control Menu")

    while run:
        root.update()
        clock.tick(60)

        if is_sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                is_sorting = False
        else:
            draw(draw_info)

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()

