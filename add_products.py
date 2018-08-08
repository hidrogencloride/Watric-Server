
from app import app, db
from app.models import Products


def add_products():
    p_names = [
        "black hoodie logo original", "black hoodie logo secondary",
        "black hoodie logo small", "black shirt logo original",
        "black shirt logo secondary", "black shirt logo secondary left",
        "stickers", "white hoodie logo original", "white hoodie logo secondary",
        "white shirt logo original", "white shirt logo original left", "white shirt logo secondary left"
    ],
    for product in p_names[0]:
        print(product)
        if "hoodie" in product:
            price = 50
        elif "shirt" in product:
            price = 15
        else:
            price = 5
        new_product = Products(p_name=product, price=price, accessory=True)
        db.session.add(new_product)
        db.session.commit()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    add_products()