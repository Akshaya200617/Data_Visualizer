from flask import Flask, render_template, request, redirect, url_for,session
import pandas as pd
from visuals import visuals
from auth import signup,signin
from db import get_connect


app = Flask(__name__)
app.secret_key="mysecretkey"
v = visuals()
df = None
columns = []
chart_file = None
chart_type_global = None 

#Signin page
@app.route("/", methods=["GET", "POST"])
def signin_route():
    return signin()

#Signup page
@app.route("/signup", methods=["GET", "POST"])
def signup_route():
    return signup()

# HOME PAGE (To UPLOAD an excel file , The column headers are selected for Category and Value )
@app.route("/home", methods=["GET", "POST"]) #route for the home page
def home():
    if "user_id" not in session:
        return redirect("/") #function to 
    print("Session:", dict(session))#temp
    try:
        global df, columns
        if request.method == "POST":
            file = request.files.get("file")
            if file:
                df_local = v.analysis(file)
                if df_local is None:
                    df = None            
                    columns = []
                    return render_template("home.html", a="Only Excel files allowed", columns=columns)
                df = df_local
                columns = df.columns.tolist()
                return redirect(url_for("next"))
        return render_template("home.html", a="", columns=columns)
    except Exception as e:
        print("HOME ERROR:", e)
        return render_template("home.html", a=str(e), columns=columns)
    
# Chart page
@app.route("/index", methods=["GET", "POST"])
def next():
    if "user_id" not in session:
        return redirect("/")
    try:
        global df, columns, chart_file, chart_type_global
        chart_file = None
        if request.method == "POST":
            chart_type_global = request.form.get("chart_type")  
            x = request.form.get("x_col")
            y = request.form.get("y_col")
            label = request.form.get("x_col")
            value = request.form.get("y_col")
            title = request.form.get("title")
            if chart_type_global == "line":
                chart_file = v.line_chart(df, x, y, title)
            elif chart_type_global == "bar":
                chart_file = v.bar_chart(df, x, y, title)
            elif chart_type_global == "hist":
                chart_file = v.histogram(df, x, title)
            elif chart_type_global == "pie":
                chart_file = v.pie_chart(df, x, y, title)
                if chart_file is None:
                    chart_file = None
            elif chart_type_global == "scatter":
                chart_file = v.scatter_chart(df, x, y, title)
            if chart_file:
                con = get_connect()
                c = con.cursor()
                c.execute("""
                INSERT INTO chart_history(
                    user_id,
                    chart_type,
                    x_column,
                    y_column,
                    chart_file
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session["user_id"],
                    chart_type_global,
                    x,
                    y,
                    chart_file
                ))
                con.commit()
                con.close()
        return render_template(
            "index.html",
            columns=columns,
            chart_file=chart_file,
            chart_type=chart_type_global   
        )
    except Exception as e:
        print("INDEX ERROR:", e)
        return render_template(
        "index.html",
        a=str(e),
        columns=columns,
        chart_file=None,
        chart_type=chart_type_global
)
    
#route to see history
@app.route("/history")
def history():
    if "user_id" not in session:
        return redirect("/")
    con = get_connect()
    c = con.cursor()
    c.execute("""
    SELECT *
    FROM chart_history
    WHERE user_id = ?
    ORDER BY created_at DESC
    """, (session["user_id"],))
    charts = c.fetchall()
    con.close()
    return render_template(
        "history.html",
        charts=charts
    )
#route to logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)