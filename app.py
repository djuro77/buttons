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


def clipboard_command(value_to_return):
    """returns a functions to be used for button action (command)"""
    return lambda: pyperclip.copy(value_to_return)


def new_button(category=None, command=None, text=None, row=0, column=0, color=None):
    """Adds new button to the frame_buttons - displays button"""
    global next_column
    if next_column[category] > 30:
        print("Max number of Buttons")
        return
    Button(frame_buttons, text=text, command=command, width=10, background=color).grid(column=column, row=row)
    next_column[category] += 1


def build_buttons_frame(): ## it might be integrated with build_buttons ??
    global frame_buttons
    frame_buttons = Frame(root_window, width=window_width)
    frame_buttons.grid(column=0, row=2, rowspan = 4)
    Label(frame_buttons, text="OneLiners").grid(column=0, row=1)
    Label(frame_buttons, text="Emails").grid(column=0, row=2)
    Label(frame_buttons, text="QuickNotes").grid(column=0, row=3)
    Label(frame_buttons, text="Temp").grid(column=0, row=4)


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
        new_button(category=b['category'], command=clipboard_command(b['content']),\
         text=b['label'], row=category_row[b['category']], column=next_column[b['category']],\
         color=b['color'])


def update_delete_menu():
    """Deletes and repopulates menu_button_delete OptionMenu wigdget with buttons that exists and can be deleted"""
    menu = menu_button_delete['menu']
    menu.delete(0, 'end')
    for label in [button['label'] for button in buttons]:
        menu.add_command(label=label, command=lambda v=label: var_button_delete.set(v))


## following func are Button actions - to be passed as a value to Button command= kwarg  ##

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
    command = clipboard_command(content)
    row = category_row[category]
    global button_color
    color = button_color
    new_button(category=category, command=command, text=label, row=row, column=next_column[category], color=color)
    buttons.append({"category":category, "label":label, "content":content, "color":color})

    # updating things
    update_delete_menu()
    entry_new_label.delete(0, END)
    entry_new_content.delete(0, END)
    button_button_color.config(background='SystemButtonFace')
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
    buttons = [button for button in buttons if button['label'] != var_button_delete.get()]
    # remove button
    frame_buttons.destroy()
    build_buttons_frame()
    build_buttons()

    # update delete menu
    update_delete_menu()


def command_always_on_top():
    if var_always_on_top.get() == 1:
        root_window.wm_attributes("-topmost", 1)
    else:
        root_window.wm_attributes("-topmost", 0)


def get_button_color():
    global button_color
    button_color = askcolor(title="Button Color")[1]
    button_button_color.config(background=button_color)


## START GUI ##

window_width = 1200

root_window = Tk()
root_window.title("Buttons {}".format(app_version))

# Root  window size
root_window.geometry(f"{window_width}x140")

# Frames
frame_add_new = Frame(root_window, width=window_width)
frame_add_new.grid(column=0, columnspan=20, row=0, rowspan = 1)

# Widgets
Label(frame_add_new, text="Label").grid(column=0, row=0)
entry_new_label = Entry(frame_add_new)
entry_new_label.grid(column=1, columnspan=2, row=0)

Label(frame_add_new, text="Content").grid(column=3, row=0)
entry_new_content = Entry(frame_add_new)
entry_new_content.grid(column=4, columnspan=2, row=0)

var_categories = StringVar(frame_add_new)
var_categories.set(categories[0])
menu_categories = OptionMenu(frame_add_new, var_categories, *categories)
menu_categories.grid(column=6, row=0)

button_button_color = Button(frame_add_new, text="Choose color", command=get_button_color)
button_button_color.grid(column=7, row=0)

Button(frame_add_new, text="ADD", command=command_new_button).grid(column=8, row=0)

Button(frame_add_new, text="Delete =>", command=command_delete_button).grid(column=9, row=0)

var_button_delete = StringVar(frame_add_new)
buttons_labels = [button['label'] for button in buttons]
menu_button_delete = OptionMenu(frame_add_new, var_button_delete, *buttons_labels)
var_button_delete.set(buttons_labels[0])
menu_button_delete.grid(column=10, row=0)

Button(frame_add_new, text="Import", command=command_import).grid(column=11, row=0)
Button(frame_add_new, text="Export", command=pickle_out).grid(column=12, row=0)

var_always_on_top = IntVar()
ckbox_always_on_top = Checkbutton(frame_add_new, text="Always on top", variable=var_always_on_top, command=command_always_on_top)
ckbox_always_on_top.grid(column=13, row=0)

build_buttons_frame()
build_buttons()
#Label(root_window, text="").grid(column=0, row=0)

### END GUI ##

### END DECLARATION ###

### START APP ###

root_window.mainloop()
