from tkinter import *
import random
import numpy as np
import matplotlib.pyplot as plt 

pressed_button = None
starting_point = None
obstacle_list = None
destination_point = None
first_number_start = None
second_number_start = None
second_number_dest = None
first_number_dest = None
reward_point = 0

def gui():
    root = Tk()
    root.title('QLearning Algorithm')
    root.geometry('800x900')
    root.resizable(width = FALSE, height = FALSE)
    count = 0                                           # for identifying each button/vertex and passing unique parameters
    
    root_size = 25                            

    # Rewards Matrix for algorithm
    rewards = [[0 for i in range(root_size)] for j in range(root_size)]

    # Matrix For Buttons painting
    button_matrix = [[0 for i in range(root_size)] for j in range(root_size)]

    frame_up = Label(root)
    frame_down = Label(root)

    frame_up.pack()
    frame_down.pack()

    global pressed_button                               # for differentiating b/w starting, ending & obstacles point
    pressed_button = 0
    global starting_point                               # starting_point is starting point
    starting_point = 0
    global destination_point                            # final destination variable

    f = open("Obstacle_list.txt", "w")

    def button_mode(mode):                              # input field by user starting/obstacles/destination point
        global pressed_button
        pressed_button = mode

    def button_click(but_no):                                   # clicked buttons in path
        global pressed_button
        global second_number_start
        global first_number_start
        global second_number_dest
        global first_number_dest

        if pressed_button == 1:                            # for starting point when pressed_button = 1
            second_number_start = int(but_no % root_size)
            first_number_start = int(but_no / root_size)
            button_matrix[first_number_start][second_number_start].config(bg = 'Aqua')
            start_button['state'] = DISABLED                    # Disable button after press
            pressed_button = 0

        if pressed_button == 2:                                # for destination when pressed_button = 2
            second_number_dest = int(but_no % root_size)
            first_number_dest = int(but_no / root_size)
            button_matrix[first_number_dest][second_number_dest].config(bg = '#7dcf21')
            destination_button['state'] = DISABLED              # Disable button after press
            pressed_button = 0

    start_button = Button(frame_up, text = 'Select Start Point', command = lambda: button_mode(1))
    destination_button = Button(frame_up, text = 'Select Destination', command = lambda: button_mode(2))

    start_button.grid(row = 0, column = 0, padx = 10)
    destination_button.grid(row = 0, column = 1)

    for i in range(root_size):
        for j in range(root_size):
            random_number = random.randint(1, 9)
            button_matrix[i][j] = Button(frame_down, text = f'{random_number}', padx = 5, pady = 5, command = lambda x=count: button_click(x))
            button_matrix[i][j].grid(row = i, column = j, sticky = "ew")
            rewards[i][j] = random_number
            count += 1

   # Restarting Gui
    def restart():           
        root.destroy()
        gui()
        
    restart_button = Button(frame_up, text='Restart', command = restart)
    restart_button.grid(row = 0, column = 3, padx = 10, pady = 5)
    
    # Creating obstacles that random place
    def setting_obstacles(): 
        b = int((root_size**2)*(0.3))  # 30 percent of the matrix is obstacle 
        
        for a in range(b): 
            random_numbers_x = random.randint(0, root_size - 1)
            random_numbers_y = random.randint(0, root_size - 1)
            
            while rewards[random_numbers_x][random_numbers_y] == -100: # If there is random number in obstacle list generate new random number
                random_numbers_x = random.randint(0, root_size - 1)
                random_numbers_y = random.randint(0, root_size - 1)

            rewards[random_numbers_x][random_numbers_y] = -100
        
            button_matrix[random_numbers_x][random_numbers_y].config(bg = 'Red')

        for i in range (root_size):
            for j in range (root_size):
                if(rewards[i][j] == -100):
                    f.write(str(i) + ", " + str(j) + ", " + "K" + "\n") # K Obstacle
                else:
                    f.write(str(i) + ", " + str(j) + ", " + "B" + "\n") # B Not Obstacle

    obstacle_button = Button(frame_up, text = 'Set Obstacles', command = setting_obstacles)
    obstacle_button.grid(row = 0, column = 4, padx = 10, pady = 5)

        # algorithm script is called
    def Run():           
        environment_rows = root_size
        environment_columns = root_size

        q_values = np.zeros((environment_rows, environment_columns, 4)) 

        actions = ['up', 'right', 'down', 'left']
  
        for i in range(root_size):
            for j in range(root_size):
                if rewards[i][j] != -100:
                    rewards[i][j] = -1
         
        rewards[first_number_dest][second_number_dest] = 100

        rewards2 = np.array(rewards)

        # Is there any obstacle on path
        def is_terminal_state(current_row_index, current_column_index):
            if rewards2[current_row_index, current_column_index] == -1:
                return False
            else:
                return True

        # Choose a path that without obstacle
        def get_starting_location():
            current_row_index = np.random.randint(environment_rows)
            current_column_index = np.random.randint(environment_columns)
            
            while is_terminal_state(current_row_index, current_column_index):
                current_row_index = np.random.randint(environment_rows)
                current_column_index = np.random.randint(environment_columns)
            return current_row_index, current_column_index

        def get_next_action(current_row_index, current_column_index, epsilon):
            if np.random.random() < epsilon:
                return np.argmax(q_values[current_row_index, current_column_index])
            else:
                return np.random.randint(4)
        
        def get_next_location(current_row_index, current_column_index, action_index):
            new_row_index = current_row_index
            new_column_index = current_column_index

            if actions[action_index] == 'up' and current_row_index > 0:
                new_row_index -= 1
            elif actions[action_index] == 'right' and current_column_index < environment_columns - 1:
                new_column_index += 1
            elif actions[action_index] == 'down' and current_row_index < environment_rows - 1:
                new_row_index += 1
            elif actions[action_index] == 'left' and current_column_index > 0:
                new_column_index -= 1
            return new_row_index, new_column_index

        def get_shortest_path(start_row_index, start_column_index):
            global reward_point
            if is_terminal_state(start_row_index, start_column_index):
                return []
            else: 
                current_row_index, current_column_index = start_row_index, start_column_index
                shortest_path = []
                shortest_path.append([current_row_index, current_column_index])
            
                while not is_terminal_state(current_row_index, current_column_index):
                    action_index = get_next_action(current_row_index, current_column_index, 1.)
                    current_row_index, current_column_index = get_next_location(current_row_index, current_column_index, action_index)
                    shortest_path.append([current_row_index, current_column_index])
                    button_matrix[current_row_index][current_column_index].config(bg = 'Orange')
                    button_matrix[first_number_dest][second_number_dest].config(bg = '#7dcf21')
                    reward_point += 5
                return shortest_path

        epsilon = 0.9 #the percentage of time when we should take the best action (instead of a random action)
        discount_factor = 0.9 #discount factor for future rewards
        learning_rate = 0.9 #the rate at which the AI agent should learn
        
        for episode in range((root_size**2)*10):
            row_index, column_index = get_starting_location()
            while not is_terminal_state(row_index, column_index):
                action_index = get_next_action(row_index, column_index, epsilon)

                old_row_index, old_column_index = row_index, column_index #store the old row and column indexes1
                row_index, column_index = get_next_location(row_index, column_index, action_index)
                
                reward = rewards2[row_index, column_index]

                old_q_value = q_values[old_row_index, old_column_index, action_index]
                
                temporal_difference = reward + (discount_factor * np.max(q_values[row_index, column_index])) - old_q_value

                new_q_value = old_q_value + (learning_rate * temporal_difference)
                q_values[old_row_index, old_column_index, action_index] = new_q_value
                          
        path = get_shortest_path(first_number_start, second_number_start)

        plt.xlabel("Episode")
        plt.ylabel("Steps")
        plt.title("Episode via Steps")

        plt.hist(rewards, histtype = 'bar', rwidth = 0.8)
        
        plt.show()

    run_button = Button(frame_up, text = 'Run', command = Run)
    run_button.grid(row = 0, column = 2, padx = 10, pady = 5)

    mainloop()
gui()


