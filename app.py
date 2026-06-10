from flask import Flask, render_template, request, redirect
import sqlite3
import pickle
import re
from datetime import datetime

app = Flask(__name__)

model = pickle.load(open("health_model.pkl", "rb"))

DATABASE = "database.db"

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_connection()
    patients = conn.execute(
        'SELECT * FROM patients'
    ).fetchall()
    conn.close()

    return render_template(
        'index.html',
        patients=patients
    )


@app.route('/add', methods=['GET','POST'])
def add_patient():

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']
        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid Email"

        if datetime.strptime(dob,"%Y-%m-%d").date() > datetime.today().date():
            return "DOB cannot be future date"

        prediction = model.predict(
            [[glucose, haemoglobin, cholesterol]]
        )[0]

        remarks = (
            "High Disease Risk"
            if prediction == 1
            else "Low Disease Risk"
        )

        conn = get_connection()

        conn.execute(
            '''
            INSERT INTO patients
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
            VALUES
            (?,?,?,?,?,?,?)
            ''',
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_patient.html')


@app.route('/delete/<int:id>')
def delete_patient(id):

    conn = get_connection()

    conn.execute(
        'DELETE FROM patients WHERE id=?',
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_patient(id):

    conn = get_connection()

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']
        glucose = float(request.form['glucose'])
        haemoglobin = float(request.form['haemoglobin'])
        cholesterol = float(request.form['cholesterol'])

        prediction = model.predict(
            [[glucose, haemoglobin, cholesterol]]
        )[0]

        remarks = (
            "High Disease Risk"
            if prediction == 1
            else "Low Disease Risk"
        )

        conn.execute(
            '''
            UPDATE patients
            SET
                full_name=?,
                dob=?,
                email=?,
                glucose=?,
                haemoglobin=?,
                cholesterol=?,
                remarks=?
            WHERE id=?
            ''',
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                id
            )
        )

        conn.commit()

        return redirect('/')

    patient = conn.execute(
        'SELECT * FROM patients WHERE id=?',
        (id,)
    ).fetchone()

    conn.close()

    return render_template(
        'edit_patient.html',
        patient=patient
    )


if __name__ == "__main__":
    app.run(debug=True)