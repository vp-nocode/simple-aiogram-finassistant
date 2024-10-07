from sqlalchemy import create_engine, Column, Integer, String, Float, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///fa.db'

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    name = Column(String)
    category1 = Column(String)
    category2 = Column(String)
    category3 = Column(String)
    expenses1 = Column(Float)
    expenses2 = Column(Float)
    expenses3 = Column(Float)

def user_exists(session, telegram_id, name):
    user = session.query(User).filter(
        and_(
            User.telegram_id == telegram_id,
            User.name == name
        )
    ).first()
    return user is not None


def update_user_expenses(session, telegram_id, new_category1=None, new_category2=None,
                         new_category3=None,  new_expenses1=None, new_expenses2=None,
                         new_expenses3=None):
    user = session.query(User).filter(User.telegram_id == telegram_id).first()

    if user:
        if new_category1 is not None:
            user.category1 = new_category1
        if new_category2 is not None:
            user.category2 = new_category2
        if new_category3 is not None:
            user.category3 = new_category3
        if new_expenses1 is not None:
            user.expenses1 = new_expenses1
        if new_expenses2 is not None:
            user.expenses2 = new_expenses2
        if new_expenses3 is not None:
            user.expenses3 = new_expenses3

        session.commit()
    else:
        print("User not found. Unable to update.")

    session.close()


Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)
