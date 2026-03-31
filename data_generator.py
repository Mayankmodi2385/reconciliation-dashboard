import pandas as pd
import random
from datetime import datetime, timedelta

def generate_data():
    base_date = datetime(2026, 3, 25)

    platform_data = []
    bank_data = []

    # Generate normal transactions
    for i in range(1, 11):
        txn_id = f"TXN{i:03}"
        amount = round(random.uniform(100, 1000), 2)
        date = base_date + timedelta(days=random.randint(0, 5))

        platform_data.append({
            "txn_id": txn_id,
            "amount": amount,
            "date": date,
            "type": "PAYMENT"
        })

        # Bank settles 1–2 days later
        bank_data.append({
            "txn_id": txn_id,
            "amount": amount,
            "date": date + timedelta(days=random.randint(1, 2)),
            "type": "PAYMENT"
        })

    # 1. Settlement next month
    txn_id = "TXN_DELAY"
    platform_data.append({
        "txn_id": txn_id,
        "amount": 500,
        "date": datetime(2026, 3, 31),
        "type": "PAYMENT"
    })

    bank_data.append({
        "txn_id": txn_id,
        "amount": 500,
        "date": datetime(2026, 4, 1),  # next month
        "type": "PAYMENT"
    })

    # 2. Duplicate in platform
    duplicate_txn = platform_data[0].copy()
    platform_data.append(duplicate_txn)

    # 3. Rounding issue
    platform_data.append({
        "txn_id": "TXN_ROUND",
        "amount": 10.005,
        "date": base_date,
        "type": "PAYMENT"
    })

    bank_data.append({
        "txn_id": "TXN_ROUND",
        "amount": 10.00,
        "date": base_date + timedelta(days=1),
        "type": "PAYMENT"
    })

    # 4. Refund without original
    platform_data.append({
        "txn_id": "TXN_REFUND",
        "amount": -300,
        "date": base_date,
        "type": "REFUND",
        "original_txn": "TXN_UNKNOWN"
    })

    return pd.DataFrame(platform_data), pd.DataFrame(bank_data)