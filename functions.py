import sqlite3
def set_database_connection():

	connection=None
	try:
		connection=sqlite3.connect("habitica.db")
	except Error as e:
		print(e)
	return connection


def add_task(conn,tasks, deadline: str="today"):
	cursor=conn.cursor()
	for task in tasks:
		cursor.execute("INSERT INTO tasks (task, deadline) VALUES (?, ?)",(task, deadline))
	conn.commit()

def switch_task(conn,tasks:list, deadline:str="today"):
	cursor=conn.cursor()
	if len(tasks)!=2:
		exit;
	cursor.execute("UPDATE tasks SET task=(?) where task=(?) and deadline=(?)",(tasks[1],tasks[0], deadline))
	conn.commit()

def remove_task(conn,numbers_of_the_task:list, deadline:str="today"):
	cursor=conn.cursor()
	tasks1=list(cursor.execute("SELECT * FROM tasks where deadline=(?)",(deadline,)))
	tasks2=[]
	print(numbers_of_the_task)
	for number in numbers_of_the_task:
		tasks2.append(tasks1[number])
	cursor.execute("DELETE FROM tasks where deadline=(?)",(deadline,))
	set_dif=set(tasks1).symmetric_difference(set(tasks2))
	tasks3=list(task[1] for task in list(set_dif))
	add_task(conn,tasks3, deadline)

