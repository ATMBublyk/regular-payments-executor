import io
import json
import os
from datetime import timedelta

import requests
from dateutil.relativedelta import relativedelta
from sqlalchemy import select

from account import Account
from regular_transfer import RegularTransferModel

BASE_URL = 'https://atm-bublyk.herokuapp.com'
LOGIN_URL = f'{BASE_URL}/login'
TRANSFER_URL = f'{BASE_URL}/transfer'


def login(card_number: str, pin: str) -> str:
    data = {
        "cardNumber": card_number,
        "pin": pin
    }
    response = requests.post(url=LOGIN_URL, data=data)
    if response.status_code != 200:
        return None
    return response.json()['accessToken']


def make_transfer(destination_card: str, amount: float, access_token: str, account) -> bool:
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "destinationCard": destination_card,
        "amount": amount,
        "isRegular": True
    }
    response = requests.post(url=TRANSFER_URL, data=data, headers=headers)
    print(response.json().get('message'))
    if response.status_code != 201:
        print(f"Status code is not 201, it is {response.status_code}")
        return False
    print("successfully make transfer")
    return True


def change_next_payment_date(account: Account, session):
    regular_transfer_model: RegularTransferModel = session.query(RegularTransferModel).filter_by(
        id=account.regular_transfer_id).first()
    if account.periodicity == 'everyday':
        account.next_payment_date += timedelta(days=1)
    elif account.periodicity == 'weekly':
        account.next_payment_date += timedelta(days=7)
    elif account.periodicity == 'monthly':
        account.next_payment_date += relativedelta(months=1)
    elif account.periodicity == 'annually':
        account.next_payment_date += relativedelta(years=1)
    else:
        raise Exception('incorrect periodicity')
    regular_transfer_model.next_payment_date = account.next_payment_date
    regular_transfer_model.save_to_db()


def update_regular_transfers(session):
    regular_transfers = session.execute(select(RegularTransferModel)).scalars().all()
    accounts = []
    # creating accounts list
    for regular_transfer in regular_transfers:
        accounts.append(Account(regular_transfer.card, regular_transfer.pin, regular_transfer.destination_card,
                                regular_transfer.amount, regular_transfer.periodicity,
                                regular_transfer.first_payment_date, regular_transfer.next_payment_date,
                                regular_transfer.id))
    # login to accounts
    for account in accounts:
        if account.access_token == "":
            access_token = login(account.card_number, account.pin)
            account.add_access_token(access_token)
    return accounts
