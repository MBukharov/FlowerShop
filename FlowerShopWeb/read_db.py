import sqlite3

conn = sqlite3.connect('db.sqlite3')
cur = conn.cursor()
# cur.execute('''SELECT name FROM sqlite_master WHERE type='table' ''')
cur.execute('''
    SELECT * FROM catalog_flower
''')
rows = cur.fetchall()
for row in rows:
    print(row)
conn.close()
