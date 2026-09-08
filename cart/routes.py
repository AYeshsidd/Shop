from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.db import get_db
from auth.dependencies import get_current_user
from auth.alchemy_model import Users
from catalog.alchemy_model import Products
from cart.pydantic_schema import CartItemCreate, CartItemUpdate, CartItemOut
from cart import crud

router = APIRouter(prefix="/cart", tags=["Cart"])


@router.get("/", response_model=list[CartItemOut])
def view_cart(
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    results = crud.get_cart_items(db, current_user.user_id)

    cart_response = []
    for cart_item, product in results:
        cart_response.append(CartItemOut(
            cart_item_id=cart_item.cart_item_id,
            product_id=product.product_id,
            quantity=cart_item.quantity,
            product_name=product.product_name,
            price=float(product.price),
            subtotal=float(product.price) * cart_item.quantity
        ))
    return cart_response


@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_item_to_cart(
    item_in: CartItemCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    product = db.query(Products).filter(Products.product_id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.quantity < item_in.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock available")

    crud.add_to_cart(db, current_user.user_id, item_in.product_id, item_in.quantity)
    return {"message": "Item added to cart"}


@router.put("/items/{cart_item_id}")
def update_cart_item_quantity(
    cart_item_id: int,
    item_in: CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    cart_item = crud.get_cart_item_by_id(db, cart_item_id, current_user.user_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    crud.update_cart_item(db, cart_item, item_in.quantity)
    return {"message": "Cart item updated"}


@router.delete("/items/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_item_from_cart(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(get_current_user)
):
    cart_item = crud.get_cart_item_by_id(db, cart_item_id, current_user.user_id)
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    crud.remove_cart_item(db, cart_item)
    return None