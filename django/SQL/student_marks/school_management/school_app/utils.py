import os
import csv
import bcrypt

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# CSV file paths (relative to the script directory)
STUDENT_FILE = os.path.join(SCRIPT_DIR, 'data', 'students.csv')
MARKS_FILE = os.path.join(SCRIPT_DIR, 'data', 'marks.csv')
ATTENDANCE_FILE = os.path.join(SCRIPT_DIR, 'data', 'attendance.csv')
MODULES_FILE = os.path.join(SCRIPT_DIR, 'data', 'modules.csv')
QUIZZES_FILE = os.path.join(SCRIPT_DIR, 'data', 'quizzes.csv')
NOTES_FILE = os.path.join(SCRIPT_DIR, 'data', 'notes.csv')
DISCUSSION_FILE = os.path.join(SCRIPT_DIR, 'data', 'discussion.csv')

# Initialize CSV files with headers if they don't exist
def initialize_files():
    os.makedirs(os.path.join(SCRIPT_DIR, 'data'), exist_ok=True)
    
    if not os.path.exists(STUDENT_FILE):
        with open(STUDENT_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student ID', 'Name', 'Age', 'Class', 'Address', 'Medical Info', 'Password', 'Cohort'])

    if not os.path.exists(MARKS_FILE):
        with open(MARKS_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student ID', 'Subject', 'Marks', 'Comments'])

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student ID', 'Subject', 'Attendance'])

    if not os.path.exists(MODULES_FILE):
        with open(MODULES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Student ID', 'Module', 'Subject'])

    if not os.path.exists(QUIZZES_FILE):
        with open(QUIZZES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Module', 'Quiz', 'Answer'])

    if not os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Module', 'Note'])

    if not os.path.exists(DISCUSSION_FILE):
        with open(DISCUSSION_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Module', 'User', 'Message'])

initialize_files()

# Function to read data from CSV
def read_csv(file):
    with open(file, mode='r') as f:
        return list(csv.reader(f))

# Function to write data to CSV
def write_csv(file, data):
    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Function to update data in CSV
def update_csv(file, data):
    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')  # Convert bytes to string for storage
import bcrypt

def verify_password(password, hashed):
    if isinstance(hashed, str):
        hashed = hashed.encode('utf-8')  # Convert string to bytes
    return bcrypt.checkpw(password.encode('utf-8'), hashed)