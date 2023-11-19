import sqlite3

connection=sqlite3.connect("habitica.db")

cursor=connection.cursor()
#cursor.execute("CREATE TABLE tasks (id integer primary key, task text not null, deadline text not null)")
#cursor.execute("delete from tasks where deadline='today'")
#x=list(cursor.execute("SELECT * FROM tasks WHERE deadline='month'"))
#print(x)
#cursor.execute("UPDATE tasks set task='de facut ceva' where id='1'")
deadline="today"
for x in cursor.execute("SELECT * FROM tasks WHERE deadline=?",(deadline,)):
	print(x)
# connection.commit()
connection.close()
