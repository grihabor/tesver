from sqlalchemy import (
    Integer, String, ForeignKey, Column
)
from sqlalchemy.orm import relationship

from database import Base


class Repository(Base):
    __tablename__ = 'repository'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', back_populates='repositories')
    
    url = Column(String(2000), nullable=False)  # https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers
    identity_file = Column(String(255), nullable=False)

