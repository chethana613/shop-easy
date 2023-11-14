'''
Student Cart related function definitions
'''
import logging
from website.models import Cart, db, InvetoryCartRelation
from flask_login import current_user

def add_cart(product_id, quantity):
    try:

        existing_user_cart_relation = Cart.query.filter_by(user_id=current_user.user_id).first()
        print("Fetched Existing cart relation")
        if not existing_user_cart_relation:
            cart = Cart(user_id=current_user.user_id)
            db.session.add(cart)
            db.session.commit()
        print("Added user relation to the cart")
        # Get the cart ID for the current user
        cart_record = Cart.query.filter_by(user_id=current_user.user_id).first()

        # Check if the item is already in the cart
        existing_relation = InvetoryCartRelation.query.filter_by(cart_id=cart_record.cart_id, sku=product_id).first()
        print("Existing relation check done")
        if existing_relation:
            # If the item is already in the cart, update the quantity
            existing_relation.quantity += quantity
        else:
            # If the item is not in the cart, create a new relation
            inventoty_cart= InvetoryCartRelation(cart_id=cart_record.cart_id, sku=product_id, quantity=quantity)
            db.session.add(inventoty_cart)

        db.session.commit()
        print("Added to cart successfully")
        return True
    except Exception as e:
        logging.exception(e)
        print("Sorry! Unable to add the Inventory")
        return False