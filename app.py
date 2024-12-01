from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supply_chain_secret_key"

# 模擬的資料庫
products = []
locations = {
    "TP": "台北",
    "TY": "桃園",
    "TC": "台中",
    "TN": "台南",
    "KS": "高雄",
    "YL": "宜蘭",
    "TT": "台東",
}
categories = ["牛奶", "羊奶", "雞蛋"]
statuses = ["出貨中", "運送中", "已抵達"]
roles = [
    "北部加工廠", "中部加工廠", "南部加工廠", "東部加工廠",
    "北部物流中心", "中部物流中心", "南部物流中心", "東部物流中心",
    "北部倉庫", "中部倉庫", "南部倉庫", "東部倉庫", "離島專用倉庫"
]

# 自動生成產品編號
def generate_product_id(location_code):
    today = datetime.now().strftime("%Y%m%d")
    count = len([p for p in products if p["location_code"] == location_code and p["date"] == today]) + 1
    return f"{location_code}-{today}-{str(count).zfill(3)}"

# 設定角色
@app.route("/set_role/<role>")
def set_role(role):
    if role in roles:
        session["role"] = role
        return redirect(url_for("index"))
    return "無效角色", 400

@app.route("/")
def index():
    role = session.get("role", "未指定角色")
    return render_template("index.html", role=role, roles=roles)

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        location_code = request.form["location"]
        category = request.form["category"]
        description = request.form["description"]

        product_id = generate_product_id(location_code)
        product = {
            "id": product_id,
            "location_code": location_code,
            "location": locations[location_code],
            "category": category,
            "description": description,
            "status": "出貨中",
            "current_location": "原產地",
            "date": datetime.now().strftime("%Y%m%d"),
            "history": [{"status": "出貨中", "location": "原產地", "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
        }
        products.append(product)
        return render_template("add_product.html", success=True, product_id=product_id, location=locations[location_code], categories=categories, locations=locations)
    return render_template("add_product.html", categories=categories, locations=locations)

@app.route("/overview")
def overview():
    return render_template("overview.html", products=products)

@app.route("/update_status/<product_id>", methods=["GET", "POST"])
def update_status(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "產品不存在", 404

    if request.method == "POST":
        new_status = request.form["status"]
        new_location = request.form["location"]

        product["status"] = new_status
        product["current_location"] = new_location
        product["history"].append({"status": new_status, "location": new_location, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        return redirect(url_for("overview"))

    return render_template("update_status.html", product=product, statuses=statuses, roles=roles)

@app.route("/query_product", methods=["GET", "POST"])
def query_product():
    if request.method == "POST":
        product_id = request.form["product_id"]
        product = next((p for p in products if p["id"] == product_id), None)
        if product:
            return render_template("product_details.html", product=product)
        return render_template("query_product.html", error="未找到產品")
    return render_template("query_product.html")

@app.route("/view_blockchain")
def view_blockchain():
    return render_template("view_blockchain.html", blockchain=products)

@app.route("/visualization")
def visualization():
    return render_template("visualization.html", blockchain=products)

if __name__ == "__main__":
    app.run(debug=True)
