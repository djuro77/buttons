from tkinter import filedialog
from tkinter import messagebox
from tkinter.colorchooser import askcolor

from tkinter import *
import pyperclip
import pickle
import time

app_version = "1.0"

categories = ["OneLiners", "Emails", "QuickNotes", "Temp"]
buttons = []
# each Button is:
# {"category":<one of the categories>, "label":"text for button label", "content":"this goes to clipboard"}

# if app does not start with at least 1 button there will be an error from
# menu_button_delete menu widget that requires at least one argument
buttons.append({"category":"Temp", "label":"Welcome", "content":"Hello", "color":None})

# variables to determine button location in gui grid
next_column = {"OneLiners":1, "Emails":1, "QuickNotes":1, "Temp":1}
category_row = {"OneLiners":1, "Emails":2, "QuickNotes":3, "Temp":4}

button_color = 'SystemButtonFace'
last_clicked_button = None
## Helper Functions START ##
def pickle_out():
    """Exports buttons list to .pkl file"""
    with open("export/dump_{}.pkl".format(time.strftime('%d-%m-%Y-%I-%M-%H-%M-%S')), "wb") as output:
        pickle.dump(buttons, output, pickle.HIGHEST_PROTOCOL)


def pickle_in(file_name):
    """imports and overwrittes button list with content from .pkl file"""
    with open(file_name, "rb") as in_put:
        global buttons
        buttons = pickle.load(in_put)


def clipboard_command(label, value_to_return):
    """returns a functions to be used for button action (command)"""
    def return_function():
        pyperclip.copy(value_to_return)
        global last_clicked_button
        last_clicked_button = label
        message_last_clicked.config(text="Current:\n{}".format(last_clicked_button))
    return return_function


def new_button(category=None, command=None, text=None, row=0, column=0, color=None):
    """Adds new button to the frame_buttons - displays button"""
    global next_column
    if next_column[category] > 30:
        print("Max number of Buttons")
        return
    button_new_button = Button(frame_buttons, text=text, command=command,\
      background=color, borderwidth=2, wraplength=60, width=8, relief=FLAT, overrelief=GROOVE) #, justify=LEFT ,width=10,
    button_new_button.grid(column=column, row=row, sticky=N+S+E+W)
    next_column[category] += 1


def build_buttons_frame(): ## it might be integrated with build_buttons ??
    global frame_buttons
    frame_buttons = Frame(root_window)
    frame_buttons.grid(row=2, rowspan = 4, columnspan=40, sticky=W)
    label_oneliners = Label(frame_buttons, text="OneLiners")
    label_oneliners.grid(column=0, row=1)
    label_emails = Label(frame_buttons, text="Emails")
    label_emails.grid(column=0, row=2)
    label_quicknotes = Label(frame_buttons, text="QuickNotes")
    label_quicknotes.grid(column=0, row=3)
    label_temp = Label(frame_buttons, text="Temp")
    label_temp.grid(column=0, row=4)


def build_buttons():
    """creates Button widget for each button in buttons list"""
    # destroy old and create new frame
    global frame_buttons
    try:
        frame_buttons.destroy()
    except:
        pass
    # create new frame and add buttons
    build_buttons_frame()
    global next_column
    next_column = {"OneLiners":1, "Emails":1, "QuickNotes":1, "Temp":1} # reset start position
    for b in buttons:
        new_button(category=b['category'], command=clipboard_command(b['label'], b['content']),\
         text=b['label'], row=category_row[b['category']], column=next_column[b['category']],\
         color=b['color'])


## following funcs are Button actions - to be passed as a value to Button command= kwarg  ##

def command_new_button():
    label = entry_new_label.get()
    if label == "":
        messagebox.showinfo("Failed to create a new Button", "You must provide a unique Label")
        return
    elif label in [button['label'] for button in buttons]:
        messagebox.showinfo("Failed to create a new Button", "Label '{}' already in use!".format(label))
        return

    category = var_categories.get()

    content = entry_new_content.get()
    command = clipboard_command(label, content)
    row = category_row[category]
    global button_color
    color = button_color
    new_button(category=category, command=command, text=label, row=row, column=next_column[category], color=color)
    buttons.append({"category":category, "label":label, "content":content, "color":color})

    # updating things
    entry_new_label.delete(0, END)
    entry_new_content.delete(0, END)
    button_button_color.config(background='SystemButtonFace', fg='SystemButtonFace')
    button_color = 'SystemButtonFace'


def command_import():
    import_filename = filedialog.askopenfilename(initialdir = "export/",title = "Select file",filetypes = (("pkl files","*.pkl"),("all files","*.*")))
    if import_filename == "":
        return
    pickle_in(import_filename)
    build_buttons()


def command_delete_button():
    # remove dict in buttons list
    global buttons
    buttons = [button for button in buttons if button['label'] != last_clicked_button]
    # remove button
    build_buttons()
    global message_last_clicked
    message_last_clicked.config(text="Current:\nNone")


def command_always_on_top():
    if var_always_on_top.get() == 1:
        root_window.wm_attributes("-topmost", 1)
    else:
        root_window.wm_attributes("-topmost", 0)


def command_get_button_color():
    global button_color
    button_color = askcolor(title="Button Color")[1]
    button_button_color.config(background=button_color, fg=button_color)


def command_move_left():
    global buttons
    for b in buttons:
        if b['label'] == last_clicked_button:
            button_index = buttons.index(b)
            try:
                previous_button = buttons[button_index-1]
            except Exception as e:
                break
            while True:
                if previous_button['category']==b['category']:
                    new_index = buttons.index(previous_button)
                    buttons.remove(b)
                    buttons.insert(new_index, b)
                    break
                else:
                    button_index -= 1
                    try:
                        previous_button = buttons[button_index-1]
                    except Exception as e: ## i.e. only one button in category
                        break
            build_buttons()
            break


def command_move_right():
    global buttons
    for b in buttons:
        if b['label'] == last_clicked_button:
            button_index = buttons.index(b)
            try:
                previous_button = buttons[button_index+1]
            except Exception as e:
                break
            while True:
                if previous_button['category']==b['category']:
                    new_index = buttons.index(previous_button)
                    buttons.remove(b)
                    buttons.insert(new_index, b)
                    break
                else:
                    button_index += 1
                    try:
                        previous_button = buttons[button_index+1]
                    except Exception as e: ## i.e. only one button in category
                        break
            build_buttons()
            break

## START GUI ##
root_window = Tk()
root_window.title("Buttons {}".format(app_version))

# Frames
frame_add_new = Frame(root_window, background='light grey', borderwidth=10)
frame_add_new.grid(column=0, row=0, columnspan=40) # , columnspan=20,  rowspan = 1

# Widgets
label_add_new_label = Label(frame_add_new, text="Label")
label_add_new_label.grid(column=0, row=0)
entry_new_label = Entry(frame_add_new)
entry_new_label.grid(column=1, columnspan=2, row=0, padx=2)

label_add_new_content = Label(frame_add_new, text="Content")
label_add_new_content.grid(column=3, row=0, padx=2)
entry_new_content = Entry(frame_add_new)
entry_new_content.grid(column=4, columnspan=2, row=0, padx=2)

var_categories = StringVar(frame_add_new)
var_categories.set(categories[0])
menu_categories = OptionMenu(frame_add_new, var_categories, *categories)
menu_categories.grid(column=6, row=0, padx=2)

button_button_color = Button(frame_add_new, text="Color", command=command_get_button_color, relief=GROOVE)
button_button_color.grid(column=7, row=0, padx=2)

button_add_new_button = Button(frame_add_new, text="ADD", command=command_new_button, relief=GROOVE)
button_add_new_button.grid(column=8, row=0, padx=2)

button_import = Button(frame_add_new, text="Import", command=command_import, relief=GROOVE)
button_import.grid(column=9, row=0, padx=2)
button_export = Button(frame_add_new, text="Export", command=pickle_out, relief=GROOVE)
button_export.grid(column=10, row=0, padx=2)

button_delete_button = Button(frame_add_new, text="<", command=command_move_left, relief=GROOVE)
button_delete_button.grid(column=11, row=0, padx=2)

message_last_clicked = Message(frame_add_new, text="Current:\n{}".format(last_clicked_button), justify=CENTER, width=60)
message_last_clicked.grid(column=12, row=0, padx=2)

button_delete_button = Button(frame_add_new, text=">", command=command_move_right, relief=GROOVE)
button_delete_button.grid(column=13, row=0, padx=2)

button_delete_button = Button(frame_add_new, text="Delete Current", command=command_delete_button, relief=GROOVE)
button_delete_button.grid(column=14, row=0, padx=2)

var_always_on_top = IntVar()
ckbox_always_on_top = Checkbutton(frame_add_new, text="Always on top", variable=var_always_on_top, command=command_always_on_top)
ckbox_always_on_top.grid(column=15, row=0, padx=2)


### END GUI ##

### END DECLARATION ###

### START APP ###
build_buttons()
root_window.mainloop()
