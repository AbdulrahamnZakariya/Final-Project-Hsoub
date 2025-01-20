import sqlite3

# إنشاء قاعدة البيانات وفتح الاتصال
conn = sqlite3.connect('school_management.db')
cursor = conn.cursor()

# إنشاء جدول الطلاب
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER UNIQUE,
                    first_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    grade TEXT,
                    registration_date TEXT)''')

# إنشاء جدول الدروس
cursor.execute('''CREATE TABLE IF NOT EXISTS lessons (
                    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lesson_name TEXT)''')

# إنشاء جدول العلاقة بين الطلاب والدروس
cursor.execute('''CREATE TABLE IF NOT EXISTS student_lessons (
                    student_id INTEGER,
                    lesson_id INTEGER,
                    FOREIGN KEY(student_id) REFERENCES students(student_id),
                    FOREIGN KEY(lesson_id) REFERENCES lessons(lesson_id))''')

# إغلاق الاتصال
conn.commit()
conn.close()
