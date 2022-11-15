from sqlalchemy import Column, Integer, String
from database import Base
from datetime import datetime

class Orders(Base):
    __tablename__  = 'orders' 
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(80), unique=True)
    status = Column (String, default="Initialized")
   