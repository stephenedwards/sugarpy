import sqlite3

print("Opening connection")
conn = sqlite3.connect('sugarpy.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("Create readings table if not present already")
cur.execute("CREATE TABLE IF NOT EXISTS readings(\
id INTEGER PRIMARY KEY, \
value INTEGER, \
time TEXT, \
trend INTEGER, \
trend_symbol TEXT, \
trend_words TEXT, \
delta INTEGER, \
units TEXT, \
mmol DECIMAL(10,2), \
reading TEXT, \
timestamp TEXT, \
full TEXT, \
user_normal_bottom INTEGER, \
user_normal_top INTEGER, \
user_urgent_low INTEGER) ;")

print("Closing connection")
conn.close()