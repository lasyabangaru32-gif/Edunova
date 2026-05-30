import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lasya@2008",  # 👈 CHANGE THIS
        database="edunova"
    )

    print("🔥 SUCCESS: Connected to edunova database")

except Exception as e:
    print("❌ ERROR:", e)