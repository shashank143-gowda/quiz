import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Drop tables if they already exist
cursor.execute('DROP TABLE IF EXISTS quizzes;')
cursor.execute('DROP TABLE IF EXISTS questions;')
cursor.execute('DROP TABLE IF EXISTS choices;')

# Create tables
cursor.execute('''
CREATE TABLE quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);
''')

cursor.execute('''
CREATE TABLE questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER,
    question_text TEXT NOT NULL,
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
);
''')

cursor.execute('''
CREATE TABLE choices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    choice_text TEXT NOT NULL,
    is_correct BOOLEAN,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
''')

# Insert sample quiz
cursor.execute("INSERT INTO quizzes (title) VALUES ('Computer Science Technical Quiz');")

# Questions and choices
questions = [
    ("What does CPU stand for?", ["Central Processing Unit", "Central Programming Unit", "Computer Personal Unit", "Control Process Unit"], 0),
    ("Which programming language is known as the backbone of web development?", ["Python", "Java", "JavaScript", "C++"], 2),
    ("What is the full form of HTTP?", ["HyperText Transfer Protocol", "Hyperlink Transfer Text Protocol", "Hyper Transfer Text Protocol", "HyperText Translation Protocol"], 0),
    ("Which data structure uses LIFO (Last In First Out)?", ["Queue", "Stack", "Array", "Linked List"], 1),
    ("Which company developed the Java programming language?", ["Microsoft", "Sun Microsystems", "Apple", "IBM"], 1),
    ("What does RAM stand for?", ["Random Access Memory", "Read Access Memory", "Run Access Memory", "Random Allocation Memory"], 0),
    ("Which SQL command is used to fetch data from a database?", ["GET", "SELECT", "EXTRACT", "OPEN"], 1),
    ("Who is known as the father of computers?", ["Charles Babbage", "Alan Turing", "Tim Berners-Lee", "Bill Gates"], 0),
    ("Which of the following is not a programming language?", ["HTML", "Python", "Java", "C#"], 0),
    ("What does IDE stand for?", ["Integrated Development Environment", "Integrated Design Environment", "Internal Development Environment", "International Development Engine"], 0),
    ("Which one is a NoSQL database?", ["MySQL", "MongoDB", "Oracle", "PostgreSQL"], 1),
    ("What is the extension of Python files?", [".py", ".java", ".html", ".css"], 0),
    ("Which sorting algorithm is generally fastest on average?", ["Bubble Sort", "Merge Sort", "Selection Sort", "Insertion Sort"], 1),
    ("Which part of the computer carries out instructions of a computer program?", ["Hard Disk", "CPU", "Monitor", "RAM"], 1),
    ("In networking, what does LAN stand for?", ["Local Area Network", "Large Area Network", "Lightweight Area Network", "Low Area Network"], 0),
]

# Insert questions and choices into the database
for idx, (question_text, options, correct_index) in enumerate(questions, start=1):
    cursor.execute("INSERT INTO questions (quiz_id, question_text) VALUES (1, ?);", (question_text,))
    question_id = cursor.lastrowid
    for i, option in enumerate(options):
        cursor.execute("INSERT INTO choices (question_id, choice_text, is_correct) VALUES (?, ?, ?);",
                       (question_id, option, 1 if i == correct_index else 0))

# Save and close
conn.commit()
conn.close()

print("Database with 15 technical questions created successfully!")
