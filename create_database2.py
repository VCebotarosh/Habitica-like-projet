import sqlite3

connection=sqlite3.connect("habitica.db")
cursor=connection.cursor()
#cursor.execute("CREATE TABLE login_info (id integer primary key, username text not null, password text not null)")
#cursor.execute("INSERT INTO login_info (username, password) VALUES ('vlad','zxc')")
#connection.commit()
# for row in cursor.execute("SELECT * FROM login_info"):
# 	print(row)
user='john'
query='SELECT * FROM login_info'
pass1=cursor.execute(query)
user_password={}
for pair in pass1:
	print(pair)
	user_password[pair[1]]=pair[2]
print(user_password)
for key, value in user_password.items():
	print(f"{key} ii revine {value}")
