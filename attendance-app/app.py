
from flask import Flask, render_template,request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    with sqlite3.connect('attendance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL
            )
        ''')   
        conn.commit()

init_db()

@app.route('/', methods=['GET', 'POST'])    
def index():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        status = request.form.get('status', '').strip()
        
        if not name or not status:
            return redirect(url_for('index'))
        
        # Save to database
        with sqlite3.connect('attendance.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO attendance (name, status) VALUES (?, ?)', (name, status))
            conn.commit()
            
        return redirect(url_for('view_attendance'))
        
    return render_template('index.html')

@app.route('/view')
def view_attendance():
    # Fetch all records from database
    with sqlite3.connect('attendance.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM attendance ORDER BY date DESC')
        records = cursor.fetchall()
        
    return render_template('view.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)
    