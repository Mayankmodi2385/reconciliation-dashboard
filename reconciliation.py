import pandas as pd

def reconcile(platform_df, bank_df):
    report = {}

    # Convert to dict for fast lookup
    bank_map = bank_df.set_index("txn_id").to_dict("index")
    platform_map = platform_df.groupby("txn_id").first().to_dict("index")

    # 1. Missing in Bank
    missing_in_bank = []
    for txn in platform_df["txn_id"]:
        if txn not in bank_map:
            missing_in_bank.append(txn)

    report["missing_in_bank"] = missing_in_bank

    # 2. Missing in Platform
    missing_in_platform = []
    for txn in bank_df["txn_id"]:
        if txn not in platform_map:
            missing_in_platform.append(txn)

    report["missing_in_platform"] = missing_in_platform

    # 3. Amount mismatch
    mismatches = []
    for txn in platform_df["txn_id"]:
        if txn in bank_map:
            p_amt = platform_map[txn]["amount"]
            b_amt = bank_map[txn]["amount"]
            if round(p_amt, 2) != round(b_amt, 2):
                mismatches.append((txn, p_amt, b_amt))

    report["amount_mismatch"] = mismatches

    # 4. Duplicate detection
    duplicates = platform_df[platform_df.duplicated(subset=["txn_id"], keep=False)]
    report["duplicates"] = duplicates["txn_id"].unique().tolist()

    # 5. Invalid refunds
    invalid_refunds = []
    refunds = platform_df[platform_df["type"] == "REFUND"]

    for _, row in refunds.iterrows():
        original = row.get("original_txn")
        if original not in platform_df["txn_id"].values:
            invalid_refunds.append(row["txn_id"])

    report["invalid_refunds"] = invalid_refunds

    # 6. Rounding difference (total level)
    total_platform = round(platform_df["amount"].sum(), 2)
    total_bank = round(bank_df["amount"].sum(), 2)

    report["total_platform"] = total_platform
    report["total_bank"] = total_bank

    return report