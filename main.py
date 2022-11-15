from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import models
from database import SessionLocal, engine



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
   db = SessionLocal()
   try:
       yield db
   finally:
       db.close()

class Order(BaseModel):
    product_name : str = Field(min_length=1)
    
    

# Read Data

@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Orders).all()


# Search by name

@app.get("/search")
def search_order(name : str, db : Session = Depends(get_db)):
    search = db.query(models.Orders).filter(models.Orders.product_name==name).first()
    if not search:
            raise HTTPException(status_code=404, detail="Order does not exist")
    return search

# Post Data

@app.post("/")
def create_order(order : Order, db : Session = Depends(get_db)):
    exists = db.query(models.Orders).filter(models.Orders.product_name==order.product_name).first()
    if exists:
        raise HTTPException(status_code=403, detail="Already exists")
    
    
    order_model = models.Orders()
    order_model.product_name = order.product_name
    

    db.add(order_model)
    db.commit()

    return f"{order.product_name} is added"

# Delete Data

@app.delete("/")
def delete_order(order_id : int, db : Session = Depends(get_db)):
    id_model = db.query(models.Orders).get(order_id)
    if not id_model:
            raise HTTPException(status_code=404, detail="Id not found")

    name = id_model.product_name

    db.delete(id_model)
    db.commit()

    return f"{name} is deleted"

 # Update Data

@app.put("/")
def update_order(order_id : int, new_order : str, db : Session = Depends(get_db)):
    find_order = db.query(models.Orders).get(order_id)
    if not find_order:
            raise HTTPException(status_code=404, detail="Id not found")
    find_order.product_name = new_order
    

    db.add(find_order)
    db.commit()

    return f" Order no. {order_id} is updated to {new_order}"

    
