from datetime import datetime


class Account:
    def __init__(self, card_number: str, pin: str, destination_card: str, amount: float, periodicity: str,
                 first_payment_date: datetime, regular_transfer_id: int):
        self.card_number = card_number
        self.pin = pin
        self.destination_card = destination_card
        self.amount = amount
        self.periodicity = periodicity
        self.first_payment_date = first_payment_date
        self.next_payment_date = first_payment_date
        self.access_token = ""
        self.regular_transfer_id = regular_transfer_id

    def add_access_token(self, access_token: str):
        self.access_token = access_token
