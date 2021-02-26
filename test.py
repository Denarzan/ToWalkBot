import sqlite3


# conn = sqlite3.connect('users.db')  # create connection
# c = conn.cursor()  # create cursor
# # c.execute('update users set description=? where user_id=?', ("description2", 123))
# # c.execute('INSERT INTO users (user_id, description, photo, location) VALUES (?,?,?,?)', ('123', 'desc1', 'photo1', 'loc1'))
# c.execute("select * from users")
# result = c.fetchone()
# while result:
#     print(result)
#     result = c.fetchone()
#
# # Save (commit) the changes
# conn.commit()
# conn.close()
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="010701",
    database='mydatabase'
)
mycursor = mydb.cursor()

sql = "INSERT INTO users (user_id, description, photo, location) VALUES (%s, %s, %s, %s)"
val = ("3", "desc3", "photo3", "loc3")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
# mycursor = mydb.cursor()
#
# mycursor.execute("SELECT * FROM users")
#
# myresult = mycursor.fetchall()
#
# for x in myresult:
#   print(x)