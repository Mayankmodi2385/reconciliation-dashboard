from data_generator import generate_data
from reconciliation import reconcile

def main():
    platform_df, bank_df = generate_data()

    print("\n--- PLATFORM DATA ---")
    print(platform_df)

    print("\n--- BANK DATA ---")
    print(bank_df)

    report = reconcile(platform_df, bank_df)

    print("\n=== RECONCILIATION REPORT ===")

    print(f"\nMissing in Bank: {report['missing_in_bank']}")
    print(f"Missing in Platform: {report['missing_in_platform']}")
    print(f"Duplicates: {report['duplicates']}")
    print(f"Invalid Refunds: {report['invalid_refunds']}")

    print("\nAmount Mismatches:")
    for txn in report["amount_mismatch"]:
        print(f"  {txn}")

    print("\nTotal Comparison:")
    print(f"Platform Total: {report['total_platform']}")
    print(f"Bank Total: {report['total_bank']}")

if __name__ == "__main__":
    main()