import tkinter as tk
import threading
import urllib.request, json 
import sched, time
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import db



class App(threading.Thread):
    glyco_text = "waiting for value"
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def setData(self,data):
        self.data = data
        self.lblGlyco['text'] = str(self.data['value']) +" mg/dl " + self.data['trend_symbol']
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.lblTime['text'] = current_time
        print("Current Time =", current_time)

    def setGlycoText(self, valueText):
        print("Updating value to "+valueText)
        self.glyco_text = valueText
        

    def run(self):
        self.root = tk.Tk()
        self.root.configure(background='black')
        #self.root.attributes('-fullscreen', True)
        self.lblGlyco = tk.Label(self.root, text=self.glyco_text, font=("Helvetica", 72), bg="black", fg="white")
        self.lblTime = tk.Label(self.root, text="time", font=("Helvetica", 30), bg="black", fg="white")
        self.lblGlyco.pack(padx=20, pady=20, expand=1) # Pack it into the window
        self.lblTime.pack(padx=20, pady=20, expand=1) # Pack it into the window
        self.root.mainloop()
        

app = App()

def getGlycoApi(s):
    with urllib.request.urlopen("http://sugarmate.io/api/v1/83y9kt/latest.json") as url:
        data = json.loads(url.read().decode())        
        
        print("Opening connection")
        conn = sqlite3.connect('sugarpy.db')
        conn.set_trace_callback(print)
        cur = conn.cursor()

        print("Inserting value into DB")
        
        sql = "INSERT OR IGNORE INTO readings VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
        cur.execute(sql, (data['x'], data['value'], data['time'], data['trend'], data['trend_symbol'], data['trend_words'], data['delta'], data['units'], data['mmol'], data['reading'], data['timestamp'], data['full'], data['user_settings']['normal_bottom_mgdl'], data['user_settings']['normal_top_mgdl'], data['user_settings']['urgent_low_mgdl'],))        
        cur.close()
        conn.commit()

        print("Closing connection")
        conn.close()

        app.setData(data)
        s.enter(60, 1, getGlycoApi, (s,))

s = sched.scheduler(time.time, time.sleep)
getGlycoApi(s)
s.run()
    

