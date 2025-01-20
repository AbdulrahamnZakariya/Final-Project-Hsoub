import sqlite3


def connect_db():
    return sqlite3.connect('school_management.db')


def add_student():
    conn = connect_db()
    cursor = conn.cursor()

    # أخذ معلومات الطالب
    student_id = int(input("أدخل رقم الطالب: "))
    first_name = input("أدخل الاسم الأول: ")
    last_name = input("أدخل الكنية: ")
    age = int(input("أدخل العمر: "))
    grade = input("أدخل الصف: ")
    registration_date = input("أدخل تاريخ التسجيل: ")

    # إضافة الطالب إلى جدول الطلاب
    cursor.execute('''INSERT INTO students (student_id, first_name, last_name, age, grade, registration_date) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (student_id, first_name, last_name, age, grade, registration_date))

    # إضافة الدروس
    print("أدخل الدروس المشترك فيها الطالب (أدخل 'done' لإنهاء):")
    while True:
        lesson_name = input("أدخل اسم الدرس: ")
        if lesson_name.lower() == 'done':
            break
        cursor.execute('''INSERT INTO lessons (lesson_name) VALUES (?)''', (lesson_name,))
        lesson_id = cursor.lastrowid
        cursor.execute('''INSERT INTO student_lessons (student_id, lesson_id) 
                          VALUES (?, ?)''', (student_id, lesson_id))

    conn.commit()
    print("تم إضافة الطالب بنجاح!")
    conn.close()


def delete_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = int(input("أدخل رقم الطالب لحذفه: "))

    # التحقق من وجود الطالب
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    if student:
        cursor.execute('DELETE FROM student_lessons WHERE student_id = ?', (student_id,))
        cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
        conn.commit()
        print("تم حذف الطالب بنجاح!")
    else:
        print("الطالب غير موجود في قاعدة البيانات.")

    conn.close()


def update_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = int(input("أدخل رقم الطالب لتعديل معلوماته: "))

    # التحقق من وجود الطالب
    cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
    student = cursor.fetchone()
    if student:
        first_name = input(f"أدخل الاسم الأول الجديد ({student[1]}): ") or student[1]
        last_name = input(f"أدخل الكنية الجديدة ({student[2]}): ") or student[2]
        age = int(input(f"أدخل العمر الجديد ({student[3]}): ") or student[3])
        grade = input(f"أدخل الصف الجديد ({student[4]}): ") or student[4]
        registration_date = input(f"أدخل تاريخ التسجيل الجديد ({student[5]}): ") or student[5]

        cursor.execute('''UPDATE students 
                          SET first_name = ?, last_name = ?, age = ?, grade = ?, registration_date = ?
                          WHERE student_id = ?''', (first_name, last_name, age, grade, registration_date, student_id))

        conn.commit()
        print("تم تعديل معلومات الطالب بنجاح!")
    else:
        print("الطالب غير موجود في قاعدة البيانات.")

    conn.close()


def show_student():
    conn = connect_db()
    cursor = conn.cursor()

    student_id = int(input("أدخل رقم الطالب لعرض معلوماته: "))

    # التحقق من وجود الطالب
    cursor.execute('''SELECT * FROM students WHERE student_id = ?''', (student_id,))
    student = cursor.fetchone()
    if student:
        print(
            f"معلومات الطالب: {student[1]} {student[2]}, العمر: {student[3]}, الصف: {student[4]}, تاريخ التسجيل: {student[5]}")

        cursor.execute('''SELECT lesson_name FROM lessons 
                          JOIN student_lessons ON lessons.lesson_id = student_lessons.lesson_id
                          WHERE student_lessons.student_id = ?''', (student_id,))
        lessons = cursor.fetchall()
        if lessons:
            print("الدروس المشترك فيها الطالب:")
            for lesson in lessons:
                print(lesson[0])
        else:
            print("الطالب غير مسجل في أي دروس.")
    else:
        print("الطالب غير موجود في قاعدة البيانات.")

    conn.close()


def main():
    while True:
        print("\nالرجاء اختيار العملية التي تريد إجرائها:")
        print("* لإضافة طالب إضغط على حرف a")
        print("* لحذف طالب إضغط على حرف d")
        print("* لتعديل معلومات طالب إضغط على حرف u")
        print("* لعرض معلومات طالب إضغط على حرف s")

        choice = input("أدخل اختيارك: ")

        if choice.lower() == 'a':
            add_student()
        elif choice.lower() == 'd':
            delete_student()
        elif choice.lower() == 'u':
            update_student()
        elif choice.lower() == 's':
            show_student()
        else:
            print("اختيار غير صحيح، حاول مرة أخرى.")


if __name__ == '__main__':
    main()
