from os import path
import generator
import files
import conn

lists = generator.generuj(N=100)
saved = {}
for key, list in lists.items():
    saved[key] = files.dump(key, list.values())

for key, filepath in saved.items():
    conn.execute_bulk(key, filepath)