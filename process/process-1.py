import schedule, sqlite3

def lalala():
	data = cursor.execute("select * from temp where value like '%4'")
	data = [i for i in data]
	with open('process-1.p', 'a') as file:
		file.write(str(data))

create_tmp_table = '''create table temp (
	name text unique,
	value text
)'''

conn = sqlite3.connect('./config/test.db')
cursor = conn.cursor()
insert_datos = [('RC_5', 'VAL1'),('RC_6', 'VAL2'),('RC_7', 'VAL3'),('RC_8', 'VAL4')]
try:
	cursor.execute(create_tmp_table)
except:
	print('Ya existe la tabla')

try:
	cursor.executemany('insert into temp values (?, ?)', insert_datos)
	conn.commit()
except:
	print('Ya hay datos')



schedule.every().minute.do(lalala)
while True:
	schedule.run_pending()