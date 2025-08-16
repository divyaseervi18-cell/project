from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # your MySQL username
        password="",        # your MySQL password
        database="resume_db"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "dob": request.form["dob"],
            "address": request.form["address"],
            "linkedin": request.form["linkedin"],
            "certification": request.form["certification"],
            "interest": request.form["interest"],
            "projects": request.form["projects"],
            "education": request.form["education"],
            "skills": request.form["skills"],
            "experience": request.form["experience"],
            "languages": request.form["languages"]
        }

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO resumes
            (name, email, phone, dob, address, linkedin, certification, interest, projects, education, skills, experience, languages)
            VALUES (%(name)s, %(email)s, %(phone)s, %(dob)s, %(address)s, %(linkedin)s, %(certification)s, %(interest)s, %(projects)s, %(education)s, %(skills)s, %(experience)s, %(languages)s)
        """, data)
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("summary", name=data["name"]))

    return render_template("form.html")

@app.route("/user")
def user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, email FROM resumes ORDER BY id DESC")
    all_user = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("user.html", user=all_user)

@app.route("/summary/<name>")
def summary(name):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumes WHERE name=%s ORDER BY id DESC LIMIT 1", (name,))
    resume = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("summary.html", resume=resume)


if __name__ == "__main__":
    app.run(debug=True)
