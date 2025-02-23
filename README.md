# Student Management System

## Overview
This is a **Student Management System** built using **PyQt6** and **SQLite**. It provides an intuitive GUI for managing student records, allowing users to add, edit, search, and delete student information efficiently.

## Description
This application is designed to simplify the management of student data. It features a clean and user-friendly interface, making it easy to perform database operations. Users can store student details such as **ID, Name, Course, and Mobile Number** in a local SQLite database.

## Features
- **Add Students**: Input and store student records.
- **Edit Records**: Modify existing student details.
- **Search Students**: Look up students by name.
- **Delete Students**: Remove student records from the database.
- **User-Friendly GUI**: Built using PyQt6 for a seamless experience.
- **Database Storage**: Uses SQLite for efficient data handling.

## Installation
To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/student-management.git
   cd student-management
   ```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the required dependencies:
   ```bash
   pip install pyqt6 sqlite3
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Open the application.
2. Use the **File Menu** to add students.
3. Click on a student record to **edit or delete** it.
4. Use the **Search Feature** to find students by name.
5. Confirm deletions when prompted.

## Technologies Used
- **PyQt6** - For the GUI interface.
- **SQLite** - To store student records.
- **Python** - Backend programming language.

## Future Enhancements
- **Export data** to CSV or Excel format.
- **Import student records** from external files.
- **Advanced filtering** options for student search.
- **User authentication** for restricted access.

## License
This project is licensed under the MIT License.

---
Feel free to contribute by adding new features or improving the existing ones!

