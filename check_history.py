from db import get_connect

con = get_connect()
c = con.cursor()

c.execute("SELECT id, username FROM users")

for row in c.fetchall():
    print(dict(row))

con.close()