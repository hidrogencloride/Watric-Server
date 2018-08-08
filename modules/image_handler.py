
from app import app, db
from app.model import Products


def add_products():

    # p_names = [
    #     "black hoodie logo original", "black hoodie logo secondary",
    #     "black hoodie logo small", "black shirt logo original",
    #     "black shirt logo secondary", "black shirt logo secondary left",
    #     "stickers", "white hoodie logo original", "white hoodie logo secondary",
    #     "white shirt logo original", "white shirt logo original left", "white shirt logo secondary left"
    # ],
    product1 = Products(p_name="black hoodie logo original", price=50, accessory=True)
    # product2 = Products(p_name=p_names[1] , price=50, accessory=True)
    # product3 = Products(p_name=p_names[2], price)
    # for product in range(len(p_names)):
    #     print(product)
    #     if "hoodie" in p_names[product]:
    #         price = 50
    #     elif "shirt" in p_names[product]:
    #         price = 15
    #     else:
    #         price = 5
    #     new_product = Products(p_name=p_names[product], price=price, accessory=True)
    #     print(new_product)
    #     db.session.add(new_product)
    #     db.session.commit()
    db.session.add(product1)
    db.session.commit()


if __name__ == "__main__":
    add_products()