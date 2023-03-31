import customtkinter
import validators
import requests
# import os
from requests.exceptions import Timeout


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("350x450")
app.resizable(width=False, height=False)
app.title("Site status")
app.iconify()

# current_path = os.getcwd()
# app.iconbitmap(f"@{current_path}/assets/icon.xbm")


text_addr = customtkinter.CTkEntry(master=app,
                                   placeholder_text="address",
                                   width=250,
                                   height=50,
                                   border_width=0,
                                   corner_radius=10,
                                   fg_color="#37383A",
                                   font=("Areal", 13))
text_addr.pack(pady=50, padx=10)

url = customtkinter.CTkLabel(master=app, text="", width=100,
                             height=50, bg_color="#212325", font=("Areal", 12))
url.place(relx=0.5, rely=0.60, anchor=customtkinter.CENTER)

text = customtkinter.CTkLabel(master=app, text="Status code: ",
                              width=100, height=50, bg_color="#212325", font=("Areal", 20))
text.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

label = customtkinter.CTkLabel(master=app, text="", width=100, height=50,
                               bg_color="#212325", font=("Areal", 20))
label.place(relx=0.5, rely=0.85, anchor=customtkinter.CENTER)


class InvalidURL(BaseException):
    def __init__(self):
        return None


#def req(event):
def req(event=None):
    try:
        addr = text_addr.get()

        if addr.strip() == "":
            label.configure(text="", bg_color="#212325")
        else:            
            if (addr.replace("https://", '').replace("http://", '') == "0.0.0.0"):
                raise Exception("sorry, but I cann't connect to 0.0.0.0 :(")

            if ('http://' not in addr) and ('https://' not in addr):
                addr = 'http://' + addr

            if not validators.url(addr):
                raise InvalidURL

            statcode = requests.get(addr.lower(), timeout=2).status_code

            if statcode == requests.codes.ok:
                label.configure(text=str(statcode),
                                bg_color="green", width=100)
            else:
                label.configure(text=str(statcode),
                                bg_color="orange", width=100)

    except InvalidURL:
        label.configure(text="InvalidURL", bg_color="red", width=200)
    except Timeout:
        label.configure(text="TimeoutError", bg_color="red", width=230)
    except Exception as err:
        window = customtkinter.CTkToplevel(fg_color="red")
        window.title("error")
        window.geometry("500x150")

        error = customtkinter.CTkTextbox(
            window, font=("Areal", 15), text_color="white")
        error.insert("0.0", f"error: {err}")
        error.configure(state="disabled")
        error.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    finally:
        outaddr = addr
        if len(addr) > 30:
            outaddr = ""
            for i in range(0, 27):
                outaddr += addr[i]
            outaddr += "...."

        url.configure(text=outaddr)

text_addr.bind("<Return>", req)

def textselect(event):
    def select_all(widget):
        widget.selection_range(0, customtkinter.END)
        widget.icursor(customtkinter.END)

    app.after(10, select_all, event.widget)

def textclear(event):
    def clear_all(widget):
        widget.delete(0, customtkinter.END)
        widget.insert(0, "")
    app.after(10, clear_all, event.widget)

button = customtkinter.CTkButton(master=app,
                                 width=180,
                                 height=50,
                                 border_width=0,
                                 corner_radius=50,
                                 text="check",
                                 command=req,
                                 font=("Areal", 17))
button.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

text_addr.bind('<Control-a>', textselect)
text_addr.bind('<Control-BackSpace>', textclear)

app.mainloop()
