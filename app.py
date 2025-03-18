from flask import Flask, render_template, request, redirect, flash
from models import db, Appointment
from datetime import datetime
import html  # For escaping user input

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # For flash messages
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/schedule', methods=['GET', 'POST'])
def schedule_appointment():
    if request.method == 'POST':
        name = request.form['name']
        time = request.form['time']
        date = request.form['date']
        attendant = request.form['attendant']

        # Escape the user inputs to prevent XSS
        name = html.escape(name)
        attendant = html.escape(attendant)

        try:
            new_appointment = Appointment(
                name=name,
                time=datetime.strptime(time, '%H:%M').time(),
                date=datetime.strptime(date, '%Y-%m-%d').date(),
                attendant=attendant
            )

            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment scheduled successfully!', 'success')
            return redirect('/appointments')
        except Exception as e:
            flash(f'Error scheduling appointment: {str(e)}', 'danger')

    return render_template('schedule_appointment.html')

@app.route('/appointments')
def appointment_list():
    appointments = Appointment.query.all()
    return render_template('appointment_list.html', appointments=appointments)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_appointment(id):
    appointment = Appointment.query.get(id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        flash('Appointment deleted successfully!', 'success')
    else:
        flash('Appointment not found!', 'danger')
    return redirect('/appointments')

if __name__ == '__main__':
    app.run(debug=True)
