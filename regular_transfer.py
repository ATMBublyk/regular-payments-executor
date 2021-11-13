import os

from sqlalchemy import Column, Integer, String, DateTime, Float, create_engine, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://lxoxahalzpfums:44af64654c0c9cad1a5600aeb784ca48ddad5a4845ec780bd6ffe4dc451fe707@ec2-54-220-53-223.eu-west-1.compute.amazonaws.com:5432/dae576orog172q')
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
