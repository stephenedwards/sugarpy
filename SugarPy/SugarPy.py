import tkinter as tk
import threading
import urllib.request, json 
import sched, time
   

class App(threading.Thread):
    glyco_text = "waiting for value"
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def setGlycoText(self, valueText):
        print("Updating value to "+valueText)
        self.glyco_text = valueText
        self.label['text'] = valueText+" mg/dl"

    def run(self):
        self.root = tk.Tk()
        #root.attributes('-fullscreen', True)
        self.label = tk.Label(self.root, text=self.glyco_text, font=("Helvetica", 48)) # Create a text label
        self.label.pack(padx=20, pady=20, expand=1) # Pack it into the window
        self.root.mainloop()

app = App()

def getGlycoApi(s):
    with urllib.request.urlopen("http://sugarmate.io/api/v1/83y9kt/latest.json") as url:
        data = json.loads(url.read().decode())    
        app.setGlycoText(str(data["value"]))
        s.enter(5, 1, getGlycoApi, (s,))

s = sched.scheduler(time.time, time.sleep)
s.enter(5, 1, getGlycoApi, (s,))
s.run()
    

