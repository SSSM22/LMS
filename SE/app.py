
from flask import Flask,render_template, request, redirect
from flask_mysqldb import MySQL

app=Flask(__name__)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '7951'
app.config['MYSQL_DB'] = 'selms'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql=MySQL(app)
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/alogin")
def admin_login():
    return render_template("alogin.html")

@app.route("/slogin")
def stu_login():
    return render_template("slogin.html")

@app.route("/admin",methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get("user")
        password = request.form.get("pass")
        print(username)
        print(password)
        if(username == "admin@gmail.com" and password =="123"):
            return render_template("admin.html");
        else :
            return "login failed"

@app.route("/display_books")
def display():
    try:
        cur = mysql.connection.cursor()
        cur.execute(''' call all_books''')
        books = cur.fetchall()
        print(len(books))
        cur.close()
        return render_template("books.html", books=books  )
    
    except mysql.connection.Error as err:
            return f"Error: {err}" 

@app.route("/add_student")
def add_student():    
    return render_template("add_student.html")

@app.route("/added",methods=['GET', 'POST'])
def added_student():
    if request.method == 'POST':
        id=request.form.get("id")
        name=request.form.get("name")
        mail=request.form.get("mail")
        passw=request.form.get("pass")
        t=(id,name,mail,passw)
        try:
            cur = mysql.connection.cursor()
            # cur.execute('''call add_student''',(t,))
            cur.callproc('add_student',(id,name,mail,passw))
            mysql.connection.commit()
            return "added succesfully"
        
        except mysql.connection.Error as err:
            return f"Error: {err}"    
@app.route("/add_book")
def book():
    return render_template("add_book.html")      

@app.route("/added_book",methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        id=int(request.form.get("id"))
        name=request.form.get("name")
        genre=int(request.form.get("Genre"))
        print(id )
        
        try:
            cur = mysql.connection.cursor()
            # cur.execute('''call add_student''',(t,))
            cur.callproc('add_book',(id,name,genre))
            mysql.connection.commit()
            return "added succesfully"
        
        except mysql.connection.Error as err:
            return f"Error: {err}" 
       
         
         
         
         
         
         
            
@app.route("/student",methods=['GET', 'POST'])
def student():
    try:
            cur = mysql.connection.cursor()
            cur.execute('''call all_students''')
            acc_det = cur.fetchall()
            cur.close()
            if request.method == 'POST':
                username = request.form.get("user")
                password = request.form.get("pass")
                print(username,password)
            for i in acc_det:
                if (i['email'] == username and i['password'] == password):
                    return redirect("/display_books") 
    except mysql.connection.Error as err:
        
            return f"Error: {err}"                  
    
    
                

    
if __name__ == '__main__':
        app.run(debug=True)