import time
from datetime import datetime

from functions import login, make_transfer, change_next_payment_date, update_regular_transfers
from regular_transfer import session

try:
    while True:
        accounts = update_regular_transfers(session)
        for account in accounts:
            current_date = datetime.utcnow()
            if account.next_payment_date.date() == current_date.date():
                print('inside first')
                if account.next_payment_date.hour == current_date.hour and \
                        account.next_payment_date.minute == current_date.minute:
                    print('inside second')
                    if not make_transfer(account.destination_card, account.amount, account.access_token, account):
                        account.access_token = login(account.card_number, account.pin)
                        make_transfer(account.destination_card, account.amount, account.access_token, account)
                        print("making transfer with login")
                    print('making transfer')
                    change_next_payment_date(account, session)
        time.sleep(15)
except Exception as e:
    session.close()
    raise e