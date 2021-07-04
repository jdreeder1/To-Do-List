#Using PostgreSQL
import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2

postgresql_uri = os.environ.get("POSTGRES_URI")

connection = psycopg2.connect(postgresql_uri)

   #A: Total user signups
   #B: Total signups in the last 24 hours
   #C: Total lists created
   #D: Lists created in the last 24 hours

#select * from users order by timeStamp desc; => gets timestamps in descending order
#select * from users where timeStamp BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW(); => find accounts created in last 24 hrs
def count_all_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM users;""")
            db_users = cursor.fetchone()
            user_count = int(''.join(map(str, db_users))) #convert tuple to int
            connection.commit()

            return user_count

def find_recent_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM users WHERE timeStamp BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW();""")
            db_users = cursor.fetchone()  #cursor.fetchall()
            #users = len(db_users) # []

           # for i in range(len(db_users)):
            #    person = db_users[i][0]
             #   users.append(person)

            connection.commit()

            return db_users

def count_all_lists():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM lists;""")
            list_count = cursor.fetchone()
            connection.commit()

            return list_count

def find_recent_lists():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT COUNT(*) FROM lists WHERE timestamp BETWEEN NOW() - INTERVAL '24 HOURS' AND NOW();""")
            recent_lists = cursor.fetchone()  #cursor.fetchall()
            #users = len(db_users) # []

           # for i in range(len(db_users)):
            #    person = db_users[i][0]
             #   users.append(person)

            connection.commit()

            return recent_lists

#SELECT email, fname, lname, timestamp FROM users;
def find_all_users(pg_num):
    per_pg = 50
    with connection:
        with connection.cursor() as cursor:
            #cursor.execute("""SELECT email, fname, lname, timestamp FROM users;""")
            cursor.execute("""SELECT email, fname, lname, timestamp FROM udf_GetRowsByPageNumberAndSize({pg_num},{per_pg}) """.format(pg_num = pg_num, per_pg = per_pg))
            db_users = cursor.fetchall()
            users = []

            for i in range(len(db_users)):
                person = db_users[i]
                users.append(person)

            connection.commit()

            return users

def delete_user(email):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM users WHERE email = '{email}';""".format(email = email))
            connection.commit()
            count = cursor.rowcount

            return count

#def delete_user_lists(email):
    #with connection:
        #with connection.cursor() as cursor:
            #cursor.execute("""DELETE FROM lists WHERE email = '{email}';""".format(email = email))
            #connection.commit()
            #count = cursor.rowcount

            #return count
