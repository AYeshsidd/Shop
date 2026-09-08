from sqlalchemy.orm import Session
from cart.alchemy_model import CartItem
from catalog.alchemy_model import Products


def get_cart_items(db: Session, user_id: int):
    return (
        db.query(CartItem, Products)
        .join(Products, CartItem.product_id == Products.product_id)
        .filter(CartItem.user_id == user_id)
        .all()
    )


def get_cart_item_by_product(db: Session, user_id: int, product_id: int):
    return db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == product_id
    ).first()


def get_cart_item_by_id(db: Session, cart_item_id: int, user_id: int):
    return db.query(CartItem).filter(
        CartItem.cart_item_id == cart_item_id,
        CartItem.user_id == user_id
    ).first()


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    existing_item = get_cart_item_by_product(db, user_id, product_id)

    if existing_item:
        existing_item.quantity += quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item

    new_item = CartItem(user_id=user_id, product_id=product_id, quantity=quantity)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


def update_cart_item(db: Session, cart_item: CartItem, quantity: int):
    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_cart_item(db: Session, cart_item: CartItem):
    db.delete(cart_item)
    db.commit()