import sqlite3

connection = sqlite3.connect('flask_tutorial.db', check_same_thread = False)

cursor = connection.cursor()

cursor.execute(
    """INSERT INTO users(
        username, 
        password,
        color
        )
        VALUES(
            'Gordon',
            'Ramsay',
            'blue'    
        );"""   
)

cursor.execute(
    """INSERT INTO users(
        username, 
        password,
        color
        )
        VALUES(
            'Ironman',
            'Tony',
            'gold'    
        );"""   
)

connection.commit()
cursor.close()
connection.close()
