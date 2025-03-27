import random
from datetime import datetime, timedelta
from Data import *
import csv

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
    for _ in range(number_of_customers):
        name = random.choice(possible_names)
        sex = 'F' if name[-1] == 'a' else 'M'
        surname = generate_surname(sex)
        birth_date = generate_birth_date()
        pesel = generate_pesel(birth_date, sex)
        street = random.choice(possible_streets)
        city = random.choice(possible_cities)
        house_number = random.randint(1, 100)
        customer = {
            "name": name + ' ' + surname,
            "birth_date": birth_date,
            "pesel": pesel,
            "phone_number": generate_phone_number(),
            "city": city,
            "address": street + ' ' + str(house_number),
            "email": name.lower() + '.' + surname.lower() + '@gmail.com'
        }
        customers.append(customer)

    with open('first_customer.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=customers[0].keys())
        writer.writeheader()
        writer.writerows(customers)
    
    return customers

def generate_adjuster():
    for _ in range(number_of_adjusters):
        name = random.choice(possible_names)
        sex = 'F' if name[-1] == 'a' else 'M'
        surname = generate_surname(sex)
        email = name.lower() + '.' + surname.lower() + '@gmail.com'
        specialization=random.choice(possible_specialization)
        adjuster = {
            "name": name + ' ' + surname,
            "email": email,
            "specialization":specialization
        }
        adjusters.append(adjuster)

    with open('first_adjusters.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=adjusters[0].keys())
        writer.writeheader()
        writer.writerows(adjusters)
    
    return adjusters
        

def generate_agent():
    for _ in range(number_of_agents):
        name = random.choice(possible_names)
        sex = 'F' if name[-1] == 'a' else 'M'
        surname = generate_surname(sex)
        email = name.lower() + '.' + surname.lower() + '@gmail.com'
        agent = {
            "name": name + ' ' + surname,
            "email": email,
            "phone_number": generate_phone_number(),
            "branch": random.choice(possible_cities)
        }
        agents.append(agent)

    with open('first_agents.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=agents[0].keys())
        writer.writeheader()
        writer.writerows(agents)

    return agents

def generate_policy():
    for _ in range(number_of_policies):
        policy_id = random.randint(100000, 999999)
        start_date = datetime(random.randint(2010, 2020), random.randint(1, 12), random.randint(1, 28))
        end_date = start_date + timedelta(days=random.randint(1, 365))
        coverage = random.choice(possible_coverage_details)
        policy = {
            "policy_id": policy_id,
            "start_date": start_date.date(),
            "end_date": end_date.date(),
            "coverage": coverage,
            "agent_foreign_key": agents[random.randint(0, number_of_agents - 1)]["name"],
            "customer_foreign_key": customers[random.randint(0, number_of_customers - 1)]["pesel"]
        }
        policies.append(policy)

        insurance_price=random.choice(possible_insurance_price)
        minimal_payout=insurance_price*100
        maximal_payout=random.randint(400000, 500000)
        policy_data= {
            "policy_id":policy_id,
            "insurance_price":insurance_price,
            "minimal_payout":minimal_payout,
            "maximal_payout":maximal_payout,
            "duration_of_policy":(end_date-start_date).days
        }
        policies_data.append(policy_data)

    with open('first_policies.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=policies[0].keys())
        writer.writeheader()
        writer.writerows(policies)

    with open('first_policies_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=policies_data[0].keys())
        writer.writeheader()
        writer.writerows(policies_data)
    
    return policies, policies_data

def generate_claim():
    for _ in range(number_of_claims):
        claim_id = random.randint(100000, 999999)
        status = random.choice(possible_status)
        claim = {
            "claim_id": claim_id,
            "status": status,
            "policy_foreign_key": policies[random.randint(0, number_of_policies - 1)]["policy_id"],
            "adjuster_foreign_key": adjusters[random.randint(0, number_of_adjusters - 1)]["name"]
        }
        claims.append(claim)

        policy_associated = policies["id" == claim["policy_foreign_key"]]
        start_date = policy_associated["start_date"]

        date_of_submission = start_date + timedelta(days=random.randint(1, 365))
        date_of_decision = date_of_submission + timedelta(days=random.randint(1, 60)) # acceptance or rejection date
        date_of_payout = date_of_decision + timedelta(days=random.randint(1, 14))

        claim_data = {
            "claim_id": claim_id,
            "date_of_submission": date_of_submission,
            "date_of_decision": date_of_decision,
            "date_of_payout": date_of_payout,
            "amount_of_payout": random.randint(35000, 400000),
            "suspicion_of_fraud": random.choices(["YES", "NO"], weights=[1, 9], k=1)[0]
        }
        claims_data.append(claim_data)

    with open('first_claims.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=claims[0].keys())
        writer.writeheader()
        writer.writerows(claims)

    with open('first_claims_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=claims_data[0].keys())
        writer.writeheader()
        writer.writerows(claims_data)
    
    return claims
