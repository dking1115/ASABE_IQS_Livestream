import mysql.connector

def cursor_connection():
    mydb = mysql.connector.connect(
    host="www.cppfallroundup.online",
    user="software",
    password="iqs2024",
    database="IQS_2024"
    )
    cursor=mydb.cursor()
    return mydb, cursor