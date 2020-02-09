import tkinter as tk
import urllib.request, json 

with urllib.request.urlopen("http://sugarmate.io/api/v1/83y9kt/latest.json") as url:
    data = json.loads(url.read().decode())
    print(data)

root = tk.Tk()
root.attributes('-fullscreen', True)
glyco_text = str(data["value"])+"mg/dl"

label = tk.Label(root, text=glyco_text, font=("Helvetica", 48)) # Create a text label

label.pack(padx=20, pady=20, expand=1) # Pack it into the window


root.mainloop()
