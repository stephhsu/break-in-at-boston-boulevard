from tkinter import *
from tkinter import ttk
import GameObject

DUMMY_OBJECT = 0
NUMBER_OF_OBJECTS = 1

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None
root = None

refresh_location = True
refresh_objects_visible = True
current_location = 11
turns_in_room_with_dog = 2

end_of_game = False
dog_fed = False
door_openend = False
vault_door_openend = False
window_openend = False
alarm_panel_box_openend = False
treat_found = False
key_found = False

screwdriver_object = GameObject.GameObject("screwdriver", 11, True, True, True, "The only tool you brought for your break-in. Maybe you can use it to get into the house...")
alarm_panel_box_object = GameObject.GameObject("alarm panel box", 12, False, True, False, "A grey rectangular box. It looks like it's being kept closed with a screw.")
window_object = GameObject.GameObject("window", 11, False, True, False, "The red light is no longer blinking." if alarm_panel_box_openend else "There is a blinking red light attached to the window.")
dog_object = GameObject.GameObject("dog", 3, False, True, False, "It looks like it won't move out of the way!")
jar_object = GameObject.GameObject("jar", 8, False, True, False, "It's a small blue jar.")
treat_object = GameObject.GameObject("treat", 8, True, False, False, "It's in a shape of a dog bone.")
desk_object = GameObject.GameObject("desk", 4, False, True, False, "A standard white and black office desk. There is a key inside of the drawer.")
key_object = GameObject.GameObject("key", 4, True, False, False, "It's a silver key.")
cabinet_object = GameObject.GameObject("cabinet", 2, False, True, False, "There's paper sticking out of the corner.")
paper_object = GameObject.GameObject("paper", 2, True, False, False, "A piece of paper with something scribbled on it.")
door_object = GameObject.GameObject("door", 10, False, True, False, "A white door with a key hole. It's locked.")
vault_door_object = GameObject.GameObject("vault door", 5, False, True, False, "A huge circular door made out of steel. There is a number pad on it where you can input a four digit code.")
valuables_object = GameObject.GameObject("valuables", 1, True, True, False, "A container marked with the word: valuables. You should grab it and go before the police come!")

game_objects = [screwdriver_object, alarm_panel_box_object, window_object, dog_object, jar_object, treat_object, desk_object, key_object, cabinet_object, paper_object, door_object, vault_door_object, valuables_object]

def perform_command(verb, noun):

    if (verb == "GO"):
        perform_go_command(noun)
    elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W")):
        perform_go_command(verb)
    elif ((verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST")):
        perform_go_command(verb)
    elif (verb == "GET"):
        perform_get_command(noun)
    elif (verb == "LOOK"):
        perform_look_command(noun)       
    elif (verb == "READ"):
        perform_read_command(noun)        
    elif (verb == "OPEN"):
        perform_open_command(noun)
    elif (verb == "INPUT" ):
        perform_input_command(noun)
    elif (verb == "UNSCREW"):
        perform_unscrew_command(noun)
    elif (verb == "FEED"):
        perform_feed_command(noun)
    elif (verb == "HELP"):
        perform_help_command()
    else:
        print_to_description("huh?")       
        
def perform_go_command(direction):

    global current_location
    global refresh_location
    
    if (direction == "N" or direction == "NORTH"):
        new_location = get_location_to_north()
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
    else:
        new_location = 0
        
    if (new_location == 0):
        print_to_description("You can't go that way!")
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    
    global refresh_objects_visible
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.location != current_location):
            print_to_description("You don't see one of those here!")
        elif (game_object.movable == False):
            print_to_description("You can't pick it up!")
        elif (game_object.carried == True):
            print_to_description("You are already carrying it")
        else:
            #handle special conditions
            if (False):
                print_to_description("special condition")
            else:
                #pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description("You don't see one of those here!")


def perform_look_command(object_name):

    global treat_found
    global key_found
    global refresh_location
    global refresh_objects_visible
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            print_to_description(game_object.description)
        else:
            #recognized but not visible
            print_to_description("You can't see one of those!")
 
        #special cases - when certain objects are looked at, others are revealed!
        if ((game_object == jar_object) and (treat_found == False)):
            treat_found = True
            treat_object.visible = True
            print_to_description("There are some treats!")
            refresh_objects_visible = True

        if ((game_object == desk_object) and (key_found == False)):
            key_found = True
            key_object.visible = True
            print_to_description("There is a key!")
            refresh_objects_visible = True

    else:
        if (object_name == ""):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
            print_to_description("You can't see one of those!")

def perform_read_command(object_name):
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if (game_object == paper_object):
            if (paper_object.carried):
                print_to_description("2546+789-121/11*19+23^2")
            elif ((paper_object.location == current_location) and (paper_object.visible)):
                print_to_description("You can't read it from a distance.  You may want to pick it up (hint - use the GET command)")
            else:
                print_to_description("You can't find it!)")
        else:
            if ((game_object.visible == False) and (game_object.carried == False)):
                print_to_description("You can't read what you can't see, silly!")
            elif (game_object.location != current_location):
                print_to_description("You can't read what you can't see, silly!")
            else:
                print_to_description("There is no text on it")
    else:
        print_to_description("I am not sure which " + object_name + "you are referring to")
# 
def perform_open_command(object_name):
    global window_openend
    global end_of_game
    global door_openend
    global end_of_game
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == door_object) and (game_object.location == current_location):
            if (key_object.carried):
                if (door_openend == True) and (game_object.location == current_location):
                    print_to_description("It is already opened!")
                else:
                    print_to_description("You unlock the door using your key. The door opens, revealing a set of stairs leading to the basement.")
                    door_openend = True
                    door_object.description = "An open door"
            else: 
                print_to_description("It is locked, and you don't have the key!")
        elif (game_object == window_object) and (game_object.location == current_location):
            if (alarm_panel_box_openend == True):
                print_to_description("The red light is no longer blinking. You open the window.")
                window_openend = True
            else:
                print_to_description("You trigger off an alarm!")
                print_to_description("You hear the sirens and you know that you've been caught. Your last thought is that maybe the blinking red light was important.")
                print_to_description("GAME OVER")
                end_of_game = True
        
        elif (game_object == valuables_object):
            if (current_location == 11):
                if(valuables_object.carried):
                    print_to_description("You open the box and you see a pair of golden dentures!")
                    print_to_description("Maybe next time you shouldn't steal from an old man...")
                    print_to_description("Well, at least you can sell them and make some money!")
                    print_to_description("GAME OVER")
                    end_of_game = True              
            else:
                print_to_description("Now's not the time to open it! You should get out of the house first!")
                        
        else:
            print_to_description("You can't open one of those.")
    else:
        print_to_description("You don't see one of those here.")

def perform_input_command(passcode):
    global vault_door_openend
    game_object = get_game_object(passcode)
     
    if (passcode == "2597") and (current_location == 5):
        print_to_description("You input a 4-digit number into the keypad. A green light blinks and a sound beeps. The vault slowly opens.")
        vault_door_openend = True
        vault_door_object.description = "An open vault"
    elif (passcode == game_object) or (current_location != 5):
        print_to_description("You can't input an object, silly!")
    else:
        print_to_description("You input a 4-digit number into the keypad. A red light blinks and the vault remains closed. ")         
        
def perform_unscrew_command(object_name):

    global window_openend
    global alarm_panel_box_openend
    game_object = get_game_object(object_name)
 
    if not (game_object is None) and (game_object.location == current_location):
        if (game_object == alarm_panel_box_object):
            if (screwdriver_object.carried):
                if (alarm_panel_box_openend == True):
                    print_to_description("It is already opened!")
                else:
                    print_to_description("You unscrew the screw on alarm panel box and open it. You see a switch and flip it off.")
                    alarm_panel_box_openend = True
                    alarm_panel_box_object.description = "An open alarm panel box"
            else: 
                print_to_description("It is closed tight with a screw!")                       
        else:
            print_to_description("You can't unscrew one of those.")
    else:
        print_to_description("You don't see one of those here.")  
        
def perform_feed_command(object_name):

    global dog_fed
    game_object = get_game_object(object_name)
 
    if not (game_object is None) and (game_object.location == current_location):
        if (game_object == dog_object):
            if (treat_object.carried):
                if (dog_fed == True):
                    print_to_description("You already gave the dog a treat!")
                else:
                    print_to_description("You feed the dog a treat and it wags it's tail. It moves away from the entrance.")
                    dog_fed = True
                    dog_object.description = "A cute fluffy poodle"
            else: 
                print_to_description("The dog looks hungry!")                       
        else:
            print_to_description("You can't feed one of those.")
    else:
        print_to_description("You don't see one of those here.")

def perform_help_command():
    print_to_description("north(n), east(e), south(s), west(w), get 'noun', look 'noun', read 'noun', open 'noun', input 'noun', unscrew 'noun', feed 'noun'")
                
def describe_current_location():
        
    if (current_location == 1):
        print_to_description("You are in the vault.")
    elif (current_location == 2):
        print_to_description("You are in the bathroom.")
    elif (current_location == 3):
        print_to_description("You are in the entry way of the house. There is small poodle sleeping in front of an entrance.")
    elif (current_location == 4):
        print_to_description("You are in the study.")
    elif (current_location == 5):
        print_to_description("You are in the basement.")
    elif (current_location == 6):
        print_to_description("You are in a hallway.")
    elif (current_location == 7):
        print_to_description("You are in the living room.")
    elif (current_location == 8):
        print_to_description("You are in the kitchen")
    elif (current_location == 9):
        print_to_description("You are going down some stairs.")
    elif (current_location == 10):
        print_to_description("You are in the family room.")
    elif (current_location == 11):
        if (valuables_object.carried):
            print_to_description("You have made it out of the house with the valuables! Now you can open it to see what's inside... ")
        else:
            print_to_description("You are standing in front of a window, ready to break into the house.")
    elif (current_location == 12):
        print_to_description("You are outside the house.")        
    else:
        print_to_description("unknown location:" + current_location)

def set_current_image():
    
    if (current_location == 1):
        image_label.img = PhotoImage(file = 'res/vault.gif')
    elif (current_location == 2):
        image_label.img = PhotoImage(file = 'res/bathroom.gif')
    elif (current_location == 3):
        image_label.img = PhotoImage(file = 'res/foyer.gif')
    elif (current_location == 4):
        image_label.img = PhotoImage(file = 'res/office.gif')
    elif (current_location == 5):
        image_label.img = PhotoImage(file = 'res/basement.gif')
    elif (current_location == 6):
        image_label.img = PhotoImage(file = 'res/hallway.gif')
    elif (current_location == 7):
        image_label.img = PhotoImage(file = 'res/living_room.gif')
    elif (current_location == 8):
        image_label.img = PhotoImage(file = 'res/kitchen.gif')
    elif (current_location == 9):
        image_label.img = PhotoImage(file = 'res/stairs.gif')
    elif (current_location == 10):
        image_label.img = PhotoImage(file = 'res/family_room.gif')
    elif (current_location == 11):
        image_label.img = PhotoImage(file = 'res/window.gif')
    elif (current_location == 12):
        image_label.img = PhotoImage(file = 'res/side_of_house.gif')                                   
    else:
        image_label.img = PhotoImage(file = 'res/hallway.gif')
        
    image_label.config(image = image_label.img)
        

def get_location_to_north():
    
    if (current_location == 11):
        return (7 if window_openend else 0)
    elif (current_location == 7):
        return 3
    elif (current_location == 6):
        return 2
    elif (current_location == 10):
        return 6
    elif (current_location == 9):
        return 5
    elif (current_location == 5):
        return (1 if vault_door_openend else 0)
    else:
        return 0

def get_location_to_south():
    
    if (current_location == 7):
        return 11
    elif (current_location == 3):
        return 7
    elif (current_location == 2):
        return 6
    elif (current_location == 6):
        return 10
    elif (current_location == 1):
        return 5
    elif (current_location == 5):
        return 9
    else:
        return 0

def get_location_to_east():
    
    if (current_location == 11):
        return 12
    elif (current_location == 7):
        return 8
    elif (current_location == 3):
        return (4 if dog_fed else 0)
    elif (current_location == 6):
        return 7
    elif (current_location == 9):
        return 10
    else:
        return 0

def get_location_to_west():
    
    if (current_location == 12):
        return 11
    elif (current_location == 8):
        return 7
    elif (current_location == 4):
        return 3
    elif (current_location == 7):
        return 6
    elif (current_location == 10):
        return (9 if door_openend else 0) 
    else:
        return 0

def handle_special_condition():
    global turns_in_room_with_dog
    global end_of_game
    
    if ((current_location == 3) and (dog_fed == False) and (end_of_game == False)):
        turns_in_room_with_dog -= 1
        if (turns_in_room_with_dog == 1):
            print_to_description("The dog wakes up! It looks like it will bark!")
        elif (turns_in_room_with_dog == 0):
            print_to_description("The dog barks and triggers an alert to the police.")
            print_to_description("You hear the sirens outside and you know that you've been caught. Your last thought is that maybe you should have befriended the dog.")
            print_to_description("GAME OVER")
            end_of_game = True
            set_directions_to_move() #TODO - this shouldn't be necessary


def print_to_description(output, user_input=False):
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')        
    description_widget.config(state = 'disabled')
    description_widget.see(END)
        
def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
            sought_object = current_object
            break
    return sought_object

def describe_current_visible_objects():
    
    object_count = 0
    object_list = ""
    
    for current_object in game_objects:
        if ((current_object.location  == current_location) and (current_object.visible == True) and (current_object.carried == False)):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
            
    print_to_description("You see: " + (object_list + "." if object_count > 0 else "nothing special.")) 

def describe_current_inventory():
    
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if (current_object.carried):
            object_list = object_list + ("," if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    
    inventory = "You are carrying: " + (object_list if object_count > 0 else "nothing")
    
    inventory_widget.config(state = "normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state = "disabled")
             
def build_interface():
    
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button    
    global root

    root = Tk()
    root.resizable(0,0)
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)    
    image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)

    description_widget = Text(root, width =50, height = 10, relief = GROOVE, wrap = 'word')
    description_widget.insert(1.0, "Welcome to Break In At Boston Boulevard! \r You hear from your friend that there are potential valuables in an old man's house and that he is on vacation. Desperate for money, can you break into his house and reach the vault before the police catch you? \r Good Luck! \r (You can type \"help\" for a list of commands.) \r")
    description_widget.config(state = "disabled")
    description_widget.grid(row=1, column=0, columnspan =3, sticky=W, padx = 2, pady = 2)

    command_widget = ttk.Entry(root, width = 25, style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=2, column=0, padx = 2, pady = 2)
    
    button_frame = ttk.Frame(root)
    button_frame.config(height = 150, width = 150, relief = GROOVE)
    button_frame.grid(row=3, column=0, columnspan =1, padx = 2, pady = 2)

    north_button = ttk.Button(button_frame, text = "N", width = 5)
    north_button.grid(row=0, column=1, padx = 2, pady = 2)
    north_button.config(command = north_button_click)
    
    south_button = ttk.Button(button_frame, text = "S", width = 5)
    south_button.grid(row=2, column=1, padx = 2, pady = 2)
    south_button.config(command = south_button_click)

    east_button = ttk.Button(button_frame, text = "E", width = 5)
    east_button.grid(row=1, column=2, padx = 2, pady = 2)
    east_button.config(command = east_button_click)

    west_button = ttk.Button(button_frame, text = "W", width = 5)
    west_button.grid(row=1, column=0, padx = 2, pady = 2)
    west_button.config(command = west_button_click)
    
    inventory_widget = Text(root, width = 30, height = 8, relief = GROOVE , state=DISABLED )
    inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)
    
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
        set_current_image()
    
    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    set_directions_to_move()                
    describe_current_inventory()
    handle_special_condition()
    
    refresh_location = False
    refresh_objects_visible = False
    
    command_widget.config(state = ("disabled" if end_of_game else "normal"))


def north_button_click():
    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()

def return_key_enter(event):
    if( event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():
    move_to_north = (get_location_to_north() > 0) and (end_of_game == False)
    move_to_south = (get_location_to_south() > 0) and (end_of_game == False)
    move_to_east = (get_location_to_east() > 0) and (end_of_game == False)
    move_to_west = (get_location_to_west() > 0) and (end_of_game == False)
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))    

def main():
    
    build_interface()
    set_current_state()
    root.mainloop()
        
main()