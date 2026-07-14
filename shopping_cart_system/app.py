from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import random

app = Flask(__name__)


products = [
    {"id": 1, "name": "Laptop", "price": 55000, "stock": 10, "image": "laptop.jpg"},
    {"id": 2, "name": "Mobile", "price": 18000, "stock": 15, "image": "mobile.jpg"},
    {"id": 3, "name": "Headphone", "price": 2500, "stock": 20, "image": "headphone.jpg"},
    {"id": 4, "name": "Keyboard", "price": 1500, "stock": 12, "image": "keyboard.jpg"},
    {"id": 5, "name": "Mouse", "price": 800, "stock": 30, "image": "mouse.jpg"},
    {"id": 6, "name": "Monitor", "price": 12000, "stock": 8, "image": "monitor.jpg"},
    {"id": 7, "name": "Printer", "price": 8500, "stock": 5, "image": "printer.jpg"},
    {"id": 8, "name": "Webcam", "price": 2200, "stock": 18, "image": "webcam.jpg"},
    {"id": 9, "name": "SSD 1TB", "price": 6500, "stock": 14, "image": "ssd.jpg"},
    {"id": 10, "name": "Smart Watch", "price": 4500, "stock": 10, "image": "smartwatch.jpg"},
]

cart = []



@app.route("/")
def dashboard():

    search = request.args.get("search", "").lower()

    if search:
        filtered = [
            p for p in products
            if search in p["name"].lower()
        ]
    else:
        filtered = products

    return render_template(
        "dashboard.html",
        products=filtered,
        cart_count=len(cart)
    )



@app.route("/add_product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        new_product = {
            "id": len(products) + 1,
            "name": request.form["name"],
            "price": int(request.form["price"]),
            "stock": int(request.form["stock"]),
            "image": request.form["image"]
        }

        products.append(new_product)

        return redirect(url_for("dashboard"))

    return render_template("add_product.html")



@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):

    product = next((p for p in products if p["id"] == id), None)

    if request.method == "POST":

        product["name"] = request.form["name"]
        product["price"] = int(request.form["price"])
        product["stock"] = int(request.form["stock"])
        product["image"] = request.form["image"]

        return redirect(url_for("dashboard"))

    return render_template("edit_product.html", product=product)



@app.route("/delete/<int:id>")
def delete(id):

    global products

    products = [p for p in products if p["id"] != id]

    return redirect(url_for("dashboard"))



@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):

    product = next((p for p in products if p["id"] == id), None)

    if product:

        found = False

        for item in cart:

            if item["id"] == id:
                item["qty"] += 1
                found = True
                break

        if not found:
            cart.append({
                "id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "image": product["image"],
                "qty": 1
            })

    return redirect(url_for("dashboard"))



@app.route("/increase/<int:id>")
def increase(id):

    for item in cart:
        if item["id"] == id:
            item["qty"] += 1

    return redirect(url_for("view_cart"))



@app.route("/decrease/<int:id>")
def decrease(id):

    for item in cart:

        if item["id"] == id:

            item["qty"] -= 1

            if item["qty"] <= 0:
                cart.remove(item)

            break

    return redirect(url_for("view_cart"))



@app.route("/remove/<int:id>")
def remove(id):

    for item in cart:

        if item["id"] == id:
            cart.remove(item)
            break

    return redirect(url_for("view_cart"))



@app.route("/empty")
def empty():

    cart.clear()

    return redirect(url_for("view_cart"))



@app.route("/cart")
def view_cart():

    subtotal = sum(i["price"] * i["qty"] for i in cart)

    gst = subtotal * 0.18

    grand = subtotal + gst

    return render_template(
        "cart.html",
        cart=cart,
        subtotal=subtotal,
        gst=gst,
        grand=grand
    )



@app.route("/receipt")
def receipt():

    subtotal = sum(i["price"] * i["qty"] for i in cart)

    gst = subtotal * 0.18

    grand = subtotal + gst

    invoice = random.randint(100000, 999999)

    return render_template(
        "receipt.html",
        cart=cart,
        subtotal=subtotal,
        gst=gst,
        grand=grand,
        invoice=invoice,
        date=datetime.now()
    )


if __name__ == "__main__":
    app.run(debug=True)