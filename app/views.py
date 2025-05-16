from app import app
from flask import render_template, request, redirect, url_for
import os
import json
from datetime import datetime

@app.route('/')
def index():
    return render_template("index.html")

def parse_date(date_str):
    if date_str:
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None
    return None

@app.route('/extract', methods=["GET", "POST"])
def extract():
    if request.method == "POST":
        product_id = request.form.get("product_id")
        if product_id and product_id.isdigit():
            return redirect(url_for("product", product_id=int(product_id)))
        url = f"https://www.ceneo.pl/{product_id}#tab=reviews"
        response = requests.get(url)
    return render_template("extract.html")

@app.route('/products')
def products():
    products = []
    products_dir = "./app/static/products"
    
    for filename in os.listdir(products_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(products_dir, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                product_data = json.load(file)
                products.append(product_data)
    
    return render_template("products.html", products=products)

@app.route('/download_json/<product_id>')
def download_json(product_id):
    opinions_directory = os.path.abspath("./app/data/opinions")
    opinion_file_name = f"{product_id}.json"
    opinion_file_path = os.path.join(opinions_directory, opinion_file_name)
    if not os.path.exists(opinion_file_path):
        return f"Plik z opiniami dla produktu {product_id} nie istnieje.", 404
    return send_from_directory(directory=opinions_directory, path=opinion_file_name, as_attachment=True)

@app.route('/author')
def author():
    return render_template("author.html")

@app.route('/product/<int:product_id>')
def product(product_id: int):
    return render_template("product.html", product_id=product_id)