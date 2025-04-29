from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for session management

# Function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home Page - Show Available Quizzes
@app.route('/')
def index():
    conn = get_db_connection()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return render_template('index.html', quizzes=quizzes)

# Start Quiz - Show Questions
@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
def quiz(quiz_id):
    conn = get_db_connection()
    if request.method == 'POST':
        score = 0
        total = 0
        for key, value in request.form.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                choice_id = int(value)
                correct = conn.execute('SELECT is_correct FROM choices WHERE id = ?', (choice_id,)).fetchone()
                if correct and correct['is_correct']:
                    score += 1
                total += 1
        conn.close()
        return render_template('result.html', score=score, total=total)

    questions = conn.execute('SELECT * FROM questions WHERE quiz_id = ?', (quiz_id,)).fetchall()
    questions_with_choices = []
    for question in questions:
        choices = conn.execute('SELECT * FROM choices WHERE question_id = ?', (question['id'],)).fetchall()
        questions_with_choices.append((question, choices))
    conn.close()
    return render_template('quiz.html', questions_with_choices=questions_with_choices)

# Route to Submit Student Details and Start Quiz
@app.route('/start-quiz', methods=['POST'])
def start_quiz():
    student_name = request.form['student_name']
    college = request.form['college']
    usn = request.form['usn']
    branch = request.form['branch']
    
    # Save data to session
    session['student_name'] = student_name
    session['college'] = college
    session['usn'] = usn
    session['branch'] = branch

    # Assuming you want to start quiz with the first available quiz
    conn = get_db_connection()
    first_quiz = conn.execute('SELECT id FROM quizzes LIMIT 1').fetchone()
    conn.close()

    if first_quiz:
        return redirect(url_for('quiz', quiz_id=first_quiz['id']))
    else:
        return "No quizzes available", 404

if __name__ == '__main__':
    app.run(debug=True)
