import random
from datetime import datetime, timedelta
from Data import *

def generate_birth_date():
    year = random.randint(1940, 2006)
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randint(0, days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    return random_date.date()

def generate_pesel(birth_date, sex):
    year = birth_date.year
    month = birth_date.month
    day = birth_date.day

    if year >= 2000:
        month += 20

    serial = random.randint(0, 999)

    gender_digit = random.choice([0, 2, 4, 6, 8]) if sex == 'F' else random.choice([1, 3, 5, 7, 9])

    pesel = f"{year % 100:02d}{month:02d}{day:02d}{serial:03d}{gender_digit}"

    weights = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
    checksum = sum(int(pesel[i]) * weights[i] for i in range(10)) % 10
    checksum = (10 - checksum) % 10
    pesel += str(checksum)

    return pesel

def generate_phone_number():
    return f"48{random.randint(501000000, 819999999)}"

def generate_surname(gender):
    if gender == 'F':
        return random.choice(possible_female_surnames)
    else:
        return random.choice(possible_male_surnames)

def generate_customer():
    name = random.choice(possible_names)
    sex = 'F' if name[-1] == 'a' else 'M'
    surname = generate_surname()
    birth_date = generate_birth_date()
    pesel = generate_pesel(birth_date, sex)
    street = random.choice(possible_streets)
    city = random.choice(possible_cities)
    house_number = random.randint(1, 100)
    return {
        "name": name + ' ' + surname,
        "birth_date": birth_date,
        "pesel": pesel,
        "phone_number": generate_phone_number(),
        "city": city,
        "address": street + ' ' + str(house_number),
        "email": name.lower() + '.' + surname.lower() + '@gmail.com'
    }

def generate_adjuster():
    name = random.choice(possible_names)
    sex = 'F' if name[-1] == 'a' else 'M'
    surname = generate_surname()
    email = name.lower() + '.' + surname.lower() + '@gmail.com'
    return {
        "name": name + ' ' + surname,
        "email": email
    }

def generate_agent():
    name = random.choice(possible_names)
    sex = 'F' if name[-1] == 'a' else 'M'
    surname = generate_surname()
    email = name.lower() + '.' + surname.lower() + '@gmail.com'
    return {
        "name": name + ' ' + surname,
        "email": email,
        "phone_number": generate_phone_number(),
    }

def generate_policy():
    policy_id = random.randint(100000, 999999)
    start_date = datetime(random.randint(2010, 2020), random.randint(1, 12), random.randint(1, 28))
    end_date = start_date + timedelta(days=random.randint(1, 365))
    return {
        "policy_id": policy_id,
        "start_date": start_date,
        "end_date": end_date
    }

def generate_claim():
    claim_id = random.randint(100000, 999999)
    return {
        "claim_id": claim_id
    }

print(generate_customer())