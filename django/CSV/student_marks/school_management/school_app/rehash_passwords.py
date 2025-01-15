import csv
from school_app.utils import hash_password

STUDENT_FILE = 'school_app/data/students.csv'

# Read the CSV file
with open(STUDENT_FILE, mode='r') as file:
    reader = csv.reader(file)
    rows = list(reader)

# Rehash passwords
for row in rows[1:]:  # Skip the header
    if len(row) >= 7:  # Ensure the row has a password field
        plain_password = row[6]  # Assuming the password is in the 7th column
        row[6] = hash_password(plain_password)

# Write the updated data back to the CSV file
with open(STUDENT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

print("Passwords rehashed successfully!")