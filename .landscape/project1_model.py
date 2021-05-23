#Using PostgreSQL
import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2

postgresql_uri = os.environ.get("POSTGRES_URI")

connection = psycopg2.connect(postgresql_uri)

#Route that denies signup if user already created
def signup(fname, lname, email, pw):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT password FROM users WHERE email = '{email}';""".format(email = email))
            exists = cursor.fetchone()

        if exists is None:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO users VALUES(%s, %s, %s, %s);", (email, fname, lname, pw))
                    connection.commit()
                    cursor.close()
                    return True
            
        else:
            return False

def check_users():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT email FROM users ORDER BY email DESC;""")
            db_users = cursor.fetchall()
            users = []

            for i in range(len(db_users)):
                person = db_users[i][0]
                users.append(person)

            connection.commit()
            #cursor.close()
            #connection.close()

            return users

def check_pw(email):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT password FROM users WHERE email = '{email}';""".format(email = email))
            password = cursor.fetchone()
            if password:
                return password[0]
            else:
                return None

#Creates new list
def seed_list(username, lst_name, tasks):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO lists (email, list_name, tasks) VALUES(%s, %s, %s);", (username, lst_name, [tasks]))

#Gets all lists
def read_lists(email):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM lists WHERE email = '{email}';""".format(email = email))
            db_lists = cursor.fetchall()

            lists = []

            for i in range(len(db_lists)):
                lists.append(db_lists[i])

            connection.commit()
            #cursor.close()
            #connection.close()

            return lists

#Find chosen list
def find_list(l_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT list_name, tasks FROM lists WHERE list_name = '{l_name}';""".format(l_name = l_name))
            selected_list = cursor.fetchone()

            connection.commit()
            #cursor.close()

            return selected_list

#Update list
def update_list(email, l_name, task):
    with connection:
        with connection.cursor() as cursor:
           cursor.execute("""UPDATE lists SET tasks = '{task}' WHERE email = '{email}' AND list_name = '{l_name}';""".format(email = email, l_name = l_name, task = task))
           connection.commit()
           count = cursor.rowcount

           return count

#Delete list
def delete_list(email, l_name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""DELETE FROM lists WHERE email = '{email}' AND list_name = '{l_name}';""".format(email = email, l_name = l_name))
            connection.commit()
            count = cursor.rowcount

            return count