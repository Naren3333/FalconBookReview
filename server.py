from flask import Flask 
from flask import render_template 
from flask import request
from flask import redirect
import sqlite3

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    con = sqlite3.connect("LibraryWebapp.db")
    try :
        reviews = con.execute("SELECT * FROM Review").fetchall()
    finally :
        con.close()
    #f = open("customers.txt", 'r')
    #lines = f.readlines()
    #data=[]
    #for line in lines:
    #    data.append(line.strip().split("*"))
    return render_template("index.html", jin_data = reviews)
@app.route("/search", methods=["POST"])
def search_books():
    con = sqlite3.connect("LibraryWebapp.db")
    Search = request.form.get("search")
    if Search != "" :
        search_data = (str("%"+Search+"%"))
        try :
            search_results = con.execute("SELECT * FROM Review WHERE BookTitle LIKE ?", (search_data,)).fetchall()
        finally :
            con.close()
        return render_template("search.html", jin_data = (Search,search_results))
    else :
        return redirect("/")

@app.route("/form", methods=["GET"])
def show_form():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def form_submit():
    con = sqlite3.connect("LibraryWebapp.db")
    try :
        book_name = request.form.get("book_name")
        book_review = request.form.get("book_review")
        book_author = request.form.get("book_author")
        reviewer_name = request.form.get("reviewer_name")
        img_file_name=""
        img = request.files.get("image_file")
        if len(book_review) >= 4 and book_author != "" and book_name != "":
            if img:
               img_file_name=img.filename
               img.save("static/{}".format(img_file_name))
            cursor = con.cursor()
            cursor.execute("PRAGMA ignore_check_constraints = ON;")
            data = (book_name,book_review,book_author,img_file_name,reviewer_name)
            cursor.execute("INSERT INTO [Review] VALUES (?,?,?,?,?)",data)
            con.commit()
        return redirect("/")
    finally :
        con.close()
    #try :
        #ret=""
        #cust_name = request.form.get("book_name")
        #cust_review = request.form.get("book_review")
        #
        #img_file_name=""
        #img = request.files.get("image_file")
        #if len(cust_review) >= 4 :
        #    if img:
        #       img_file_name=img.filename
        #       img.save("static/{}".format(img_file_name))
        #    ret= str("{}*{}*{}*{}*{}".format(cust_name,cust_review,img_file_name))
        #    f = open("customers.txt", "a")
        #    f.write(ret+"\n")
        #    f.close()
        #return redirect("/")
    #except Exception as e:
        #print("************RUUUUUUUUUUNNNNNNTIMEEEE ERRRROOOORRRR")
        #print(e)


print("server waiting ...")
app.run(debug=True)
