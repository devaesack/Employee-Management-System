
from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)
def get_connection():
    return psycopg2.connect(
        os.environ.get("DATABASE_URL")
    )
@app.route("/")
def home():
    conn = get_connection()

    cur = conn.cursor()

    search = request.args.get("search")

    no_results = False

    if search:

        cur.execute(
            """
            SELECT *
            FROM employees
            WHERE
                name ILIKE %s
                OR email ILIKE %s
                OR department ILIKE %s
            """,
            (
                f"%{search}%",
                f"%{search}%",
                f"%{search}%"
            )
        )

        employees = cur.fetchall()

        if len(employees) == 0:

            no_results = True

            cur.execute("SELECT * FROM employees")
            employees = cur.fetchall()

    else:

        cur.execute("SELECT * FROM employees")
        employees = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        employees=employees,
        count=len(employees),
        search=search,
        no_results=no_results
    )

@app.route("/add", methods=["POST"])
def add_employee():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO employees(name,email,department)
        VALUES(%s,%s,%s)
        """,
        (name, email, department)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_employee(id):
    conn = get_connection()

    
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM employees WHERE id = %s",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/edit/<int:id>")
def edit_employee(id):
    conn = get_connection()

    

    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM employees WHERE id = %s",
        (id,)
    )

    employee = cur.fetchone()

    conn.close()

    return render_template(
        "edit.html",
        employee=employee
    )

@app.route("/update/<int:id>", methods=["POST"])
def update_employee(id):

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]
    conn = get_connection()

    

    cur = conn.cursor()

    cur.execute(
        """
        UPDATE employees
        SET name=%s,
            email=%s,
            department=%s
        WHERE id=%s
        """,
        (name, email, department, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)