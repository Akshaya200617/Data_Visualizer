from flask import render_template, request, redirect,session
from db import *

#This flask is for the signup page
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        print("Username:", repr(username))
        print("Password:", repr(password))
        # Validation
        if not username or not password:
            return render_template(
                "signup.html",
                msg="All fields are required"
            )
        if password != confirm_password:
            return render_template(
                "signup.html",
                msg="Passwords do not match"
            )
        try:
            con = get_connect()
            c = con.cursor()
            c.execute(
                """
                INSERT INTO users(username,password)
                VALUES (?,?)
                """,
                (username, password)
            )
            con.commit()
            con.close()
            return redirect("/")

        except Exception as e:
            print("Signup Error:", e)
            return render_template(
                "signup.html",
                msg="Username already exists"
            )
        finally:
            if con:
                con.close()
    return render_template("signup.html")


#This flask is for the signin page
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        con = get_connect()
        c = con.cursor()
        c.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            AND password = ?
            """,
            (username,password)
        )
        user = c.fetchone()
        con.close()
        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            print("Logged in:", session["username"])
            return redirect("/home")
        return render_template(
            "signin.html",
            msg="Invalid Username or Password"
        )
    return render_template("signin.html")

