import sqlite3

DATABASE = 'school.sqlite'

# إضافة طالب
def add_student(student_data, lessons):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        # إضافة بيانات الطالب
        cursor.execute("""
        INSERT INTO students (id, first_name, last_name, age, grade, registration_date)
        VALUES (?, ?, ?, ?, ?, ?)
        """, student_data)

        # إضافة الدروس وربطها بالطالب
        for lesson in lessons:
            cursor.execute("SELECT id FROM lessons WHERE lesson_name = ?", (lesson,))
            result = cursor.fetchone()

            if result is None:
                cursor.execute("INSERT INTO lessons (lesson_name) VALUES (?)", (lesson,))
                lesson_id = cursor.lastrowid
            else:
                lesson_id = result[0]

            cursor.execute("""
            INSERT INTO student_lessons (student_id, lesson_id)
            VALUES (?, ?)
            """, (student_data[0], lesson_id))

        connection.commit()
        print("Student added successfully.")
    except sqlite3.IntegrityError:
        print("Error: Student ID already exists.")
    finally:
        connection.close()

# حذف طالب
def delete_student(student_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        cursor.execute("DELETE FROM student_lessons WHERE student_id = ?", (student_id,))
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        connection.commit()
        print("Student deleted successfully.")
    finally:
        connection.close()

# تعديل بيانات طالب
def update_student(student_id, new_data):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        cursor.execute("""
        UPDATE students
        SET first_name = ?, last_name = ?, age = ?, grade = ?, registration_date = ?
        WHERE id = ?
        """, (*new_data, student_id))
        connection.commit()
        print("Student updated successfully.")
    finally:
        connection.close()

# عرض بيانات طالب
def show_student(student_id):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    try:
        cursor.execute("""
        SELECT students.*, group_concat(lessons.lesson_name, ', ')
        FROM students
        LEFT JOIN student_lessons ON students.id = student_lessons.student_id
        LEFT JOIN lessons ON student_lessons.lesson_id = lessons.id
        WHERE students.id = ?
        GROUP BY students.id
        """, (student_id,))
        result = cursor.fetchone()

        if result:
            print(f"ID: {result[0]}")
            print(f"First Name: {result[1]}")
            print(f"Last Name: {result[2]}")
            print(f"Age: {result[3]}")
            print(f"Grade: {result[4]}")
            print(f"Registration Date: {result[5]}")
            print(f"Lessons: {result[6]}")
        else:
            print("Student not found.")
    finally:
        connection.close()

if __name__ == "__main__":
    while True:
        print("\nPlease select an operation:")
        print("* To add a student, press 'a'")
        print("* To delete a student, press 'd'")
        print("* To update a student, press 'u'")
        print("* To show student information, press 's'")
        print("* To exit, press 'e'")

        choice = input("Enter your choice: ").lower()

        if choice == 'a':
            student_id = int(input("Enter student ID: "))
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            age = int(input("Enter age: "))
            grade = input("Enter grade: ")
            registration_date = input("Enter registration date (YYYY-MM-DD): ")
            lessons = input("Enter lessons (comma-separated): ").split(',')

            add_student((student_id, first_name, last_name, age, grade, registration_date), lessons)

        elif choice == 'd':
            student_id = int(input("Enter student ID to delete: "))
            delete_student(student_id)

        elif choice == 'u':
            student_id = int(input("Enter student ID to update: "))
            first_name = input("Enter new first name: ")
            last_name = input("Enter new last name: ")
            age = int(input("Enter new age: "))
            grade = input("Enter new grade: ")
            registration_date = input("Enter new registration date (YYYY-MM-DD): ")

            update_student(student_id, (first_name, last_name, age, grade, registration_date))

        elif choice == 's':
            student_id = int(input("Enter student ID to show: "))
            show_student(student_id)

        elif choice == 'e':
            break

        else:
            print("Invalid choice, please try again.")
