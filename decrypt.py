# decrypt_bank_data.py

import csv
import hashlib
import sys

# Function to hash using SHA1
def sha1_hash(data):
    return hashlib.sha1(data.encode('utf-8')).hexdigest()

# Make sure to pass 2 input files
if len(sys.argv) != 3:
    print("Usage: python3 decrypt_bank_data.py <encrypted_csv_file> <reference_csv_file>")
    sys.exit(1)

encrypted_file = sys.argv[1]
reference_file = sys.argv[2]
output_file = "decrypted_bank_data.csv"

# Build lookup tables
ssn_lookup = {}
account_lookup = {}

with open(reference_file, mode='r') as ref_file:
    reader = csv.DictReader(ref_file)
    for row in reader:
        ssn_plain = row['Social Security Number (Plain)']
        account_plain = row['Account Number (Plain)']
        ssn_lookup[sha1_hash(ssn_plain)] = ssn_plain
        account_lookup[sha1_hash(account_plain)] = account_plain

# Perform decryption
with open(encrypted_file, mode='r') as enc_file, open(output_file, mode='w', newline='') as out_file:
    reader = csv.DictReader(enc_file)
    fieldnames = ['Name', 'Social Security Number (Decrypted)', 'Account Number (Decrypted)', 'Routing Number']
    writer = csv.DictWriter(out_file, fieldnames=fieldnames)

    writer.writeheader()

    for row in reader:
        name = row['Name']
        ssn_hashed = row['Social Security Number']
        acc_hashed = row['Account Number']
        routing_number = row['Routing Number']

        ssn_decrypted = ssn_lookup.get(ssn_hashed, 'UNKNOWN')
        acc_decrypted = account_lookup.get(acc_hashed, 'UNKNOWN')

        writer.writerow({
            'Name': name,
            'Social Security Number (Decrypted)': ssn_decrypted,
            'Account Number (Decrypted)': acc_decrypted,
            'Routing Number': routing_number
        })

print(f"Decryption completed successfully. Output written to {output_file}.")
