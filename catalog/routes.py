from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.db import get_db
from auth.dependencies import require_role , get_current_user
from auth.alchemy_model import Users
from catalog.pydantic_schema import Categorycreate, CategoryOut, ProductCreate , ProductOut
from catalog import crud

router = APIRouter(prefix="/categories", tags=["Categories"])

#  PUBLIC ROUTE Category
@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return crud.get_all_categories(db)


# ADMIN-ONLY Category ROUTE 
@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: Categorycreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_role("admin"))
):
    existing = crud.get_category_by_name(db, category_in.name)
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    return crud.create_category(db, category_in)

# ADMIN-ONLY Category ROUTE 
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_role("admin"))
):
    category = crud.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    crud.delete_category(db, category)
    return None

# -----------------------------------------------------------------------------------------------------

product_router = APIRouter(prefix="/products", tags=["Products"])

# ---------- PUBLIC ROUTE ----------
@product_router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)


# ADMIN-ONLY Product ROUTE ----------
@product_router.post("/products/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_role("admin"))
):
    category = crud.get_category_by_id(db, product_in.category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return crud.create_product(db, product_in)


# ADMIN-ONLY Product ROUTE
@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_role("admin"))
):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    crud.delete_product(db, product)
    return None