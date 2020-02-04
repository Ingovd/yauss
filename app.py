from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Setting up DB schema?
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Note {self.id}>"

@app.route('/delete/<int:id>')
def delete(id):
    note_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(note_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return f"Something went wrong at the DB while deleting note {id}"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    note = Todo.query.get_or_404(id)
    if request.method == 'POST':
        note.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return f"There was an issue with the DB while updating note {id}"
    else:
        return render_template('update.html', note=note)

# Route the root to this function.
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        note_content = request.form['content']
        new_note = Todo(content=note_content)

        try:
            db.session.add(new_note)
            db.session.commit()
            return redirect('/')
        except:
            return 'Oops, something went wrong.'
    else:
        notes = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', notes=notes)

# Running the scripts starts server in Debug
if __name__ == "__main__":
    app.run(debug=True)