import psycopg2
conn=psycopg2.connect(database="postgres",user="postgres",password="123456", host="127.0.0.1", port="5432")
cursor=conn.cursor()
cursor.execute('''select * from pg_buffercache''')
rows = cursor.fetchall()
print(rows)
conn.commit()
conn.close()


