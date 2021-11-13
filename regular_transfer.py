import os

from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine(os.environ.get('DATABASE_URI'))
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

session = Session()


class RegularTransferModel(Base):
    __tablename__ = 'regular_transfers'

    id = Column(Integer, primary_key=True)
    destination_card = Column(String)
    amount = Column(Float)
    periodicity = Column(String)
    first_payment_date = Column(DateTime)
    next_payment_date = Column(DateTime)
    card = Column(String)
    pin = Column(String)

    def json(self):
        return {
            'id': self.id,
            'destinationCard': self.destination_card,
            'amount': self.amount,
            'periodicity': self.periodicity,
            'firstPaymentDate': self.first_payment_date.isoformat(),
            'card': self.card,
            'pin': self.pin
        }

    def save_to_db(self):
        session.add(self)
        session.commit()
