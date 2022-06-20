
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session

# from app import schemas, crud

# from app.schemas import product as product_schema
# from app.schemas import message as message_schema
# from app.api.deps import get_db

# router = APIRouter()


# @router.get("", response_model=List[product_schema.ProductResponse])
# def read_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
#     """
#     Retrieve all products.
#     """
#     products = crud.product.get_multi(db, skip=skip, limit=limit)
#     return products
