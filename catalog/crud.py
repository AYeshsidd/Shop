from sqlalchemy.orm import Session
from catalog.alchemy_model import Category
from catalog.pydantic_schema import Categorycreate
from catalog.alchemy_model import Category, Products
from catalog.pydantic_schema import Categorycreate, ProductCreate

def get_all_categories(db: Session):
    return db.query(Category).all()


def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.category_id == category_id).first()


def get_category_by_name(db: Session, name: str):
    return db.query(Category).filter(Category.name == name).first()

def create_category(db: Session, category_in: Categorycreate):
    new_category = Category(
        name=category_in.name,
        description=category_in.description
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def delete_category(db: Session, category: Category):
    db.delete(category)
    db.commit()

def get_all_products(db: Session):
    return db.query(Products).all()


def get_product_by_id(db: Session, product_id: int):
    return db.query(Products).filter(Products.product_id == product_id).first()

# PRODUCTS 

def create_product(db: Session, product_in: ProductCreate):
    new_product = Products(
        category_id=product_in.category_id,
        product_name=product_in.product_name,
        product_description=product_in.product_description,
        price=product_in.price,
        quantity=product_in.quantity,
        image_url=product_in.image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def delete_product(db: Session, product: Products):
    db.delete(product)
    db.commit()