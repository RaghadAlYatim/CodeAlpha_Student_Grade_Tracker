import sys
import sqlite3

# Database setup
def initialize_database():
    connection = sqlite3.connect("student_grades.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS grades (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        subject TEXT NOT NULL,
                        grade REAL NOT NULL,
                        FOREIGN KEY(student_id) REFERENCES students(id)
                      )''')
    connection.commit()
    connection.close()


def display_menu():
    """
    Displays the main menu of the Student Grade Tracker.
    """
    print("\n===========================")
    print("       Student Grade Tracker")
    print("===========================")
    print("1. Add grades for a student")
    print("2. View all grades")
    print("3. Calculate average grade for a subject")
    print("4. Edit a student grade")
    print("5. Generate detailed grade report")
    print("6. Exit")


def add_grade():
    """
    Adds a grade for a specific student and subject.
    """
    connection = sqlite3.connect("student_grades.db")
    cursor = connection.cursor()

    student_name = input("Enter student name: ").strip()
    if not student_name:
        print("Student name cannot be empty.")
        return

    # Ensure the student exists or add them to the database
    cursor.execute("SELECT id FROM students WHERE name = ?", (student_name,))
    result = cursor.fetchone()

    if result:
        student_id = result[0]
    else:
        cursor.execute("INSERT INTO students (name) VALUES (?)", (student_name,))
        student_id = cursor.lastrowid
        connection.commit()

    subject = input("Enter subject name: ").strip()
    if not subject:
        print("Subject name cannot be empty.")
        return

    try:
        grade = float(input(f"Enter grade for {subject} (0 - 100): "))
        if grade < 0 or grade > 100:
            print("Grade must be between 0 and 100.")
            return
    except ValueError:
        print("Invalid input. Please enter a numeric grade.")
        return

    cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)", (student_id, subject, grade))
    connection.commit()
    connection.close()

    print(f"Grade {grade:.2f} added for {student_name} in {subject}.")


def view_grades():
    """
    Displays all grades by student and subject.
    """
    connection = sqlite3.connect("student_grades.db")
    cursor = connection.cursor()

    cursor.execute('''SELECT students.name, grades.subject, grades.grade 
                       FROM grades 
                       JOIN students ON grades.student_id = students.id''')
    rows = cursor.fetchall()
    connection.close()

    if not rows:
        print("No grades available.")
        return

    print("\nGrades by Student and Subject:")
    print("==============================")
    for row in rows:
        print(f"Student: {row[0]}, Subject: {row[1]}, Grade: {row[2]:.2f}")


def calculate_average():
    """
    Calculates and displays the average grade for a specific subject.
    """
    connection = sqlite3.connect("student_grades.db")
    cursor = connection.cursor()

    subject = input("Enter the subject name to calculate the average grade: ").strip()
    if not subject:
        print("Subject name cannot be empty.")
        return

    cursor.execute("SELECT AVG(grade) FROM grades WHERE subject = ?", (subject,))
    result = cursor.fetchone()
    connection.close()

    if result[0] is None:
        print(f"No grades available for the subject: {subject}.")
    else:
        print(f"\nAverage grade for {subject}: {result[0]:.2f}")


def edit_grade():
    """
    Allows editing an existing grade for a student and subject.
    """
    connection = sqlite3.connect("student_grades.db")
    cursor = connection.cursor()

    student_name = input("Enter the student name: ").strip()
    subject = input("Enter the subject name: ").strip()

    cursor.execute('''SELECT grades.id, grades.grade FROM grades
                       JOIN students ON grades.student_id = students.id
                       WHERE students.name = ? AND grades.subject = ?''', (student_name, subject))
    result = cursor.fetchone()

    if result:
        grade_id, current_grade = result
        print(f"Current grade for {student_name} in {subject}: {current_grade:.2f}")
        try:
            new_grade = float(input("Enter the new grade: "))
            if 0 <= new_grade <= 100:
                cursor.execute("UPDATE grades SET grade = ? WHERE id = ?", (new_grade, grade_id))
                connection.commit()
                print("Grade updated successfully.")
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric grade.")
    else:
        print("No matching grade found for the given student and subject.")

    connection.close()


def generate_grade_report():
    """
    Generates a detailed grade report by student and subject.
    """
    connection = sqlite3.connect("student_grades.db")
    cursor = connection.cursor()

    cursor.execute('''SELECT students.name, grades.subject, AVG(grades.grade) as average_grade 
                       FROM grades 
                       JOIN students ON grades.student_id = students.id
                       GROUP BY students.name, grades.subject
                       ORDER BY students.name, grades.subject''')
    rows = cursor.fetchall()
    connection.close()

    if not rows:
        print("No grades available for the report.")
        return

    print("\nDetailed Grade Report:")
    print("=======================")
    for row in rows:
        print(f"Student: {row[0]}, Subject: {row[1]}, Average Grade: {row[2]:.2f}")


def main():
    """
    Main function to run the Student Grade Tracker program.
    """
    initialize_database()

    while True:
        display_menu()
        choice = input("\nChoose an option (1-6): ").strip()

        if choice == "1":
            add_grade()
        elif choice == "2":
            view_grades()
        elif choice == "3":
            calculate_average()
        elif choice == "4":
            edit_grade()
        elif choice == "5":
            generate_grade_report()
        elif choice == "6":
            print("Exiting Student Grade Tracker. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option from the menu.")


if __name__ == "__main__":
    main()
