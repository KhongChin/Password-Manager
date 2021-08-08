import tkinter
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- SEARCH SAVED DETAILS ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("./data.json", "r") as data:
            user_details = json.load(data)
            password = user_details[website]["password"]
            email = user_details[website]["email"]

    except (json.decoder.JSONDecodeError, FileNotFoundError):
        if len(website) <= 0:
            messagebox.showinfo(title="Error", message="Please insert website before searching.")

        else:
            messagebox.showinfo(title="Error", message="No Data File Found.")

    except KeyError:
        if len(website) <= 0:
            messagebox.showinfo(title="Error", message="Please insert website before searching.")

        elif website not in user_details:
            messagebox.showinfo(title="Error", message=f"No details for the {website} exists.")

    else:
        messagebox.showinfo(title=f"{website.title()}", message=f"Email/Username: {email}\n"
                                                                f"Password: {password}")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    username_email = username_entry.get()
    user_password = password_entry.get()
    new_data = {
        website: {
            "email": username_email,
            "password": user_password
        }
    }

    if len(website) <= 0 or len(user_password) <= 0 or len(username_email) <= 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")

    else:
        try:
            with open("./data.json", "r") as data:
                user_details = json.load(data)

        except FileNotFoundError:
            with open("./data.json", "w") as data:
                json.dump(new_data, data, indent=4)

        except json.decoder.JSONDecodeError:
            with open("./data.json", "w") as data:
                json.dump(new_data, data, indent=4)

        else:
            user_details.update(new_data)
            with open("./data.json", "w") as data:
                json.dump(user_details, data, indent=4)

        finally:
            website_entry.delete(0, "end")
            password_entry.delete(0, "end")


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.title("Password Manger")
window.config(padx=20, pady=20)

canvas = tkinter.Canvas(width=200, height=200)
logo = tkinter.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

website_label = tkinter.Label(text="Website:")
website_label.grid(row=1, column=0, sticky="EW")
username_label = tkinter.Label(text="Email/Username:")
username_label.grid(row=2, column=0, sticky="EW")
password_label = tkinter.Label(text="Password:")
password_label.grid(row=3, column=0, sticky="EW")

website_entry = tkinter.Entry()
website_entry.grid(row=1, column=1, columnspan=1, sticky="EW")
website_entry.focus()
username_entry = tkinter.Entry()
username_entry.insert(0, "khongchin96@hotmail.com")
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
password_entry = tkinter.Entry()
password_entry.grid(row=3, column=1, sticky="EW")

generate_button = tkinter.Button(text="Generate Password", command=generate_password)
generate_button.grid(row=3, column=2, sticky="EW")
add_button = tkinter.Button(text="Add", command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")
search_button = tkinter.Button(text="Search", command=find_password)
search_button.grid(row=1, column=2, sticky="EW")

window.mainloop()
