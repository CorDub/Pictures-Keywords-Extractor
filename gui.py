import tkinter as tk
from tkinter import filedialog
from pke import extract_csv_kw

window = tk.Tk()
window.title("Image Keywords Extractor")

frame = tk.Frame()
frame.pack()

def open_folder_dialog(event):
    dirname = filedialog.askdirectory()
    try:
        not_parsed = extract_csv_kw(dirname)
        app_console["text"] = "Successfully extracted keywords in keywords.csv"
        if len(not_parsed) > 0 and len(not_parsed) <= 10:
            linebreak_notparsed = "\n".join(not_parsed)
            app_console["text"] = app_console["text"] + '\n' + '\n' + f"Could not parse the following {len(not_parsed)} image(s): \n{linebreak_notparsed}"
        if len(not_parsed)>10:
            app_console["text"] = app_console["text"] + '\n' + '\n' + f"More than 10 images could not be parsed." + '\n' + "You'll find the complete list in 'could_not_be_parsed.csv'"
    except:
        app_console["text"] = "There was an error"

folder_selector = tk.Button(master=frame, width=15, text="Choose the folder")
dirname = folder_selector.bind("<Button-1>", open_folder_dialog)
folder_selector.pack()

extra_info = tk.Label(master=frame, text="You have to be inside the folder\ncontaining the pictures", font=('TkDefaultFont', 8, "italic"))
extra_info.pack()

app_console = tk.Label(frame, text="", justify="center", borderwidth=10)
app_console.pack()

window.mainloop()
