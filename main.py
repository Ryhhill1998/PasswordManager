from tkinter import *
from tkinter import messagebox
from random import shuffle, choice, randint
import string
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    password_letters = []

    letters = list(string.ascii_lowercase)
    numbers = [num for num in range(0, 10)]
    symbols = ["?", "%", "$", "&", "£", "!", "#", "*"]
    upper_lower = ["U", "L"]

    for num in range(randint(8, 12)):
        letter = choice(letters)
        case = choice(upper_lower)
        if case == "U":
            letter = letter.upper()
        password_letters.append(letter)

    for num in range(randint(4, 6)):
        password_letters.append(choice(numbers))

    for num in range(randint(2, 4)):
        password_letters.append(choice(symbols))

    shuffle(password_letters)

    password = "".join(map(str, password_letters))

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def search_credentials():

    website = website_entry.get()

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
            credentials = data[website]

    except KeyError:
        messagebox.showinfo(message=f"Sorry, you do not have any credentials saved for {website}.\n\n"
                                    f"Remember, entries are case sensitive.")

    except FileNotFoundError:
        messagebox.showinfo(message="Sorry, you do not have any credentials saved yet")

    else:
        username = credentials["Username"]
        password = credentials["Password"]
        messagebox.showinfo(message=f"Your credentials for {website} are:\n\nUsername: \n{username}\n"
                                    f"Password: \n{password}")


def reset_entries():
    website_entry.delete(0, END)
    website_entry.focus()

    username_entry.delete(0, END)
    username_entry.insert(0, "ryhhill1998@outlook.com")

    password_entry.delete(0, END)


def save_password():

    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "Username": username,
            "Password": password
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(message="Please fill all available fields")

    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", mode="w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            reset_entries()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Create labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Create buttons
generate_password_button = Button(text="Generate Password", command=generate_password, width=12)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", command=save_password, width=35)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", command=search_credentials, width=12)
search_button.grid(column=2, row=1)

# Create entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = Entry(width=37)
username_entry.insert(0, "ryhhill1998@outlook.com")
username_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

window.mainloop()
