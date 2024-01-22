from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import SelectField
from wtforms.fields import DateField, EmailField, TelField
from wtforms.fields import StringField, PasswordField
from wtforms.fields import DateTimeField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtforms import SelectField, StringField
from wtforms.fields import DateTimeField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Zz123456@localhost/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the Task_manager model
class Task_manager(db.Model):
    __table_args__ = {'extend_existing': True}  # Add this line to extend the existing table
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100), nullable=False)
    task_created_date = db.Column(db.DateTime, nullable=False)
    task_priority = db.Column(db.String(20), nullable=True)

class TaskForm(FlaskForm):
    task_name = StringField('Название задачи:', validators=[DataRequired()])
    task_created_date = DateTimeField('Дата создания:', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    task_priority = SelectField('Приоритет:', choices=[('Низкий', 'Низкий'), ('Средний', 'Средний'), ('Высокий', 'Высокий')], validators=[DataRequired()])



@app.route('/')
def index():
    items = Task_manager.query.all()
    return render_template('index.html', items=items)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        item_name = request.form['task_name']
        task_priority = request.form['task_priority']  # Get task_priority from the form

        print(f"Received form data: task_name={item_name}, task_priority={task_priority}")

        new_item = Task_manager(task_name=item_name, task_created_date=datetime.now(), task_priority=task_priority)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    item = Task_manager.query.get(id)

    if request.method == 'POST':
        try:
            item.task_name = request.form['task_name']
            item.task_priority = request.form['task_priority']
            item.task_created_date = datetime.strptime(request.form['task_created_date'], '%Y-%m-%dT%H:%M')
            db.session.commit()
            return redirect(url_for('index'))
        except ValueError as e:
            # Handle the ValueError, for example, log it or return an error page.
            print(f"Error updating task: {e}")
            db.session.rollback()  # Rollback changes to avoid partial updates

    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete(id):
    item = Task_manager.query.get(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))
