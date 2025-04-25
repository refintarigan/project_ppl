from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Koneksi ke MongoDB
client = MongoClient("mongodb+srv://refintarigan:REFIN@cluster0.wm5gntz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["mydatabase"]
collection = db["users"]

@app.route("/form")
def index():
    return render_template("form.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form["name"]
    email = request.form["email"]

    # Simpan ke MongoDB
    data = {"name": name, "email": email}
    collection.insert_one(data)

    return redirect("form")

# Hapus satu dokumen
result = collection.delete_one({"email": "khairunisa050802@gmail.com"})
print(f"{result.deleted_count} document deleted")
if __name__ == "__main__":
    app.run(debug=True)
