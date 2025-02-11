# Student_Grade_Tracker_CodeAlpha

#Description:

The Student Grade Tracker is a Python-based application designed to help users track student grades and calculate averages for different subjects. The project integrates with an SQLite database to store student information and their respective grades, providing a persistent and organized way to manage academic records.

#Features

Add Grades: Users can add grades for students in specific subjects. The program automatically stores student data if they are new entries.

View Grades: Displays all grades stored in the database, organized by student and subject.

Edit Grades: Allows users to update existing grades for a student and subject.

Calculate Average: Computes the average grade for a specified subject based on all student records.

#Other Details

Database: SQLite is used for lightweight and file-based storage.

.Database Schema:

students table: Stores student names with a unique ID.

grades table: Stores subject names and grades associated with student IDs.

.Core Functions:

initialize_database(): Sets up the database with the required tables.

add_grade(): Handles grade input and student record creation.

view_grades(): Retrieves and displays all grades from the database.

calculate_average(): Computes and displays the average grade for a given subject.

edit_grade(): Allows users to modify an existing grade entry

#Run the Application:

python student_grade_tracker.py
