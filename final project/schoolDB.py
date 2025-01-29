import sqlite3

def setup_database():
    connection = sqlite3.connect('school.sqlite')
    cursor = connection.cursor()

    # إنشاء جدول الطلاب
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL,
        registration_date TEXT NOT NULL
    )
    """)

    # إنشاء جدول الدروس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id INTEGER PRIMARY KEY,
        lesson_name TEXT NOT NULL
    )
    """)

    # إنشاء جدول العلاقة بين الطلاب والدروس
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS student_lessons (
        student_id INTEGER NOT NULL,
        lesson_id INTEGER NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (lesson_id) REFERENCES lessons (id)
    )
    """)

    connection.commit()
    connection.close()
    print("Database setup completed successfully.")

if __name__ == "__main__":
    setup_database()
