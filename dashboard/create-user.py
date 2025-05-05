import mysql.connector
import bcrypt

def create_user(username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db = mysql.connector.connect(host="localhost", user="root", password="", database="management_system")
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, hashed))
    db.commit()
    cursor.close()
    db.close()
    print(f"✅ User '{username}' created.")


create_user("Shabna, shabna123")
