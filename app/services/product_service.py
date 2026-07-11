from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.category import Category
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.order import OrderItem
from fastapi import HTTPException

def create_product(db: Session, created_product: ProductCreate) -> Product:
    """
    Creates a new product.
    
    Validates that the category exists.
    Validates that the product does not already exists.
    Creates product.
    
    Args:
        db: DB session.
        created_product: A ProductCreate model that has the name, description, price, stock_quantity
                        and category_id of the product
    
    Returns:
        The created Product model.
    
    Raises:
        HTTPException 404: If category does not exists.
        HTTPException 400: If product already exists.
    """
    existing_category = db.query(Category).filter(Category.id == created_product.category_id).first()
    if not existing_category:
        raise HTTPException(status_code = 404, detail = "Category Not Found")
    existing_product = db.query(Product).filter(Product.name == created_product.name).first()
    if existing_product:
        raise HTTPException(status_code = 400, detail = "Product already exists")
    new_product = Product(
        name = created_product.name,
        description = created_product.description,
        price = created_product.price,
        stock_quantity = created_product.stock_quantity,
        category_id = created_product.category_id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product(db: Session, product_id: int, updated_product: ProductUpdate) -> Product:
    """
    Updates the name, description, price, stock_quantity or/and category_id of a product.
    
    Validates that the product exists.
    Update the products name, description, price and/or stock_quantity.
    Validates that the category_id exists if its provided, and then updates the category_id.
    
    Args:
        db: DB session.
        product_id: ID of the product.
        updated_product: A ProductUpdate model that contains the name, description, price, stock_quantity
                        or/and category_id of the product
                        
    Returns:
        The updated Product model.
        
    Raises:
        HTTPException 404: If products does not exists and/or category_id does not exists.
    """
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    if updated_product.name:
        existing_product.name = updated_product.name
    if updated_product.description:
        existing_product.description = updated_product.description
    if updated_product.price:
        existing_product.price = updated_product.price
    if updated_product.stock_quantity:
        existing_product.stock_quantity = updated_product.stock_quantity
    if updated_product.category_id:
        existing_category = db.query(Category).filter(Category.id == updated_product.category_id).first()
        if not existing_category:
            raise HTTPException(status_code = 404, detail = "Category Not Found")
        existing_product.category_id = updated_product.category_id
    db.commit()
    db.refresh(existing_product)
    return existing_product

def delete_product(db: Session, product_id: int) -> Product:
    """
    Deletes a product
    
    Validates that the product exists.
    Validates that the product is not in any existing order.
    Deletes the product.
    
    Args:
        db: DB session.
        product_id: ID of the product.
        
    Returns:
        The deleted Product model.
        
    Raises:
        HTTPException 404: If product does not exists.
        HTTPException 409: If product is in an existing order.
    """
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code = 404, detail = "Product not found")
    existing_order_items = db.query(OrderItem).filter(OrderItem.product_id == product_id).first()
    if existing_order_items:
        raise HTTPException(status_code=409, detail="Product has existing orders and cannot be deleted")
    db.delete(existing_product)
    db.commit()
    return existing_product

def get_product_by_id(db: Session, product_id: int) -> Product:
    """
    Gets a specific product by its ID.
    
    Validates that the product exists.
    
    Args:
        db: DB session.
        product_id: ID of the product.
        
    Returns:
        The Product model.
        
    Raises:
        HTTPException 404: If product does not exists.
    """
    existing_product = db.query(Product).filter(Product.id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code = 404, detail = "Product does not exists")
    return existing_product
def get_all_product(db: Session) -> list[Product]:
    """Gets all products."""
    return db.query(Product).all()