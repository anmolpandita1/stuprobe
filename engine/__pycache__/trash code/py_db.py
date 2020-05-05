
import sqlite3
from sqlite3 import Error

database = "C:/project/be/db.sqlite3"



def create_connection(db_file):
    
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
 
    return conn
 
 
conn = create_connection(database)

print(conn)
cur = conn.cursor()

ms = cur.execute("INSERT INTO stuprobe_attendance (date,status,course_id,student_id) VALUES ('2020-03-10', 1, 'Course_CS_1' , 'be_comp_a_06' )")
print(ms)

conn.commit()