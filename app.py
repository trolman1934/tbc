from ext import app
from route import login, register, logout, index, product_list, create_product, delete_product, allowed_file, edit_product

app.run(debug=True , host=("0.0.0.0"))
