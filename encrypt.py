# generate_bank_data.py

import csv
import hashlib
import random
import faker

# Initialize Faker
fake = faker.Faker()

# Function to hash sensitive information
def sha1_hash(data):
    return hashlib.sha1(data.encode('utf-8')).hexdigest()

# Functions to generate random SSN, Account Numbers, Routing
def generate_ssn():
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}"

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def generate_routing_number():
    return str(random.randint(100000000, 999999999))

# Number of dummy entries
NUM_ENTRIES = 100

# Output files
encrypted_file = "encrypted_bank_data.csv"
reference_file = "decryption_reference.csv"

# Write both files
with open(encrypted_file, mode='w', newline='') as enc_file, open(reference_file, mode='w', newline='') as ref_file:
    enc_writer = csv.DictWriter(enc_file, fieldnames=['Name', 'Social Security Number', 'Account Number', 'Routing Number'])
    ref_writer = csv.DictWriter(ref_file, fieldnames=['Name', 'Social Security Number (Plain)', 'Account Number (Plain)', 'Routing Number'])

    enc_writer.writeheader()
    ref_writer.writeheader()

    for _ in range(NUM_ENTRIES):
        name = fake.name()
        ssn = generate_ssn()
        account_number = generate_account_number()
        routing_number = generate_routing_number()

        enc_writer.writerow({
            'Name': name,
            'Social Security Number': sha1_hash(ssn),
            'Account Number': sha1_hash(account_number),
            'Routing Number': routing_number
        })

        ref_writer.writerow({
            'Name': name,
            'Social Security Number (Plain)': ssn,
            'Account Number (Plain)': account_number,
            'Routing Number': routing_number
        })

print(f"Generated {NUM_ENTRIES} bank records into {encrypted_file} and {reference_file}.")
