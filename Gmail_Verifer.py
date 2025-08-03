import requests
import random
import string

BANNER = r"""
 ____  _____ ____  _   _  ___   ___  ____      ____ __  __    _    ___ _     
|  _ \| ____|  _ \| | | |/ _ \ / _ \|  _ \    / ___|  \/  |  / \  |_ _| |    
| |_) |  _| | | | | |_| | | | | | | | | | |  | |  _| |\/| | / _ \  | || |    
|  _ <| |___| |_| |  _  | |_| | |_| | |_| |  | |_| | |  | |/ ___ \ | || |___ 
|_| \_\_____|____/|_| |_|\___/ \___/|____/    \____|_|  |_/_/   \_\___|_____|
                                                                             
__     _______ ____  ___ _____ _____ ____  
\ \   / / ____|  _ \|_ _|  ___| ____|  _ \ 
 \ \ / /|  _| | |_) || || |_  |  _| | |_) |
  \ V / | |___|  _ < | ||  _| | |___|  _ < 
   \_/  |_____|_| \_\___|_|   |_____|_| \_\
                                           
"""

def verify_email_hunter(email, api_key):
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        status = data.get('data', {}).get('status', 'unknown')
        return status
    except Exception as e:
        print(f"Error checking {email} with Hunter.io: {e}")
        return "error"

def verify_email_mailboxlayer(email, api_key):
    url = f"http://apilayer.net/api/check?access_key={api_key}&email={email}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('format_valid') and data.get('smtp_check'):
            return "valid"
        elif not data.get('format_valid'):
            return "invalid"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error checking {email} with Mailboxlayer: {e}")
        return "error"

def verify_email_abstract(email, api_key):
    url = f"https://emailvalidation.abstractapi.com/v1/?api_key={api_key}&email={email}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('deliverability') == "DELIVERABLE":
            return "valid"
        elif data.get('deliverability') == "UNDELIVERABLE":
            return "invalid"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error checking {email} with AbstractAPI: {e}")
        return "error"

def verify_email_emailrep(email):
    url = f"https://emailrep.io/{email}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('deliverable') is True:
            return "valid"
        elif data.get('deliverable') is False:
            return "invalid"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error checking {email} with EmailRep: {e}")
        return "error"

def verify_email_zerobounce(email, api_key):
    url = f"https://api.zerobounce.net/v2/validate?api_key={api_key}&email={email}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == "valid":
            return "valid"
        elif data.get('status') == "invalid":
            return "invalid"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error checking {email} with ZeroBounce: {e}")
        return "error"

def verify_email_kickbox(email, api_key):
    url = f"https://api.kickbox.com/v2/verify?email={email}&apikey={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('result') == "deliverable":
            return "valid"
        elif data.get('result') == "undeliverable":
            return "invalid"
        else:
            return "unknown"
    except Exception as e:
        print(f"Error checking {email} with Kickbox: {e}")
        return "error"

def get_api_choice():
    print("\nChoose API to use:")
    print("1. Hunter.io")
    print("2. Mailboxlayer")
    print("3. AbstractAPI")
    print("4. EmailRep (no API key needed)")
    print("5. ZeroBounce")
    print("6. Kickbox")
    api_choice = input("Your choice (1-6): ").strip()
    return api_choice

def get_api_key(api_choice):
    if api_choice == "1":
        return input("Enter your Hunter.io API key: ").strip()
    elif api_choice == "2":
        return input("Enter your Mailboxlayer API key: ").strip()
    elif api_choice == "3":
        return input("Enter your AbstractAPI key: ").strip()
    elif api_choice == "5":
        return input("Enter your ZeroBounce API key: ").strip()
    elif api_choice == "6":
        return input("Enter your Kickbox API key: ").strip()
    else:
        return None

def verify_email(email, api_choice, api_key=None):
    if api_choice == "1":
        return verify_email_hunter(email, api_key)
    elif api_choice == "2":
        return verify_email_mailboxlayer(email, api_key)
    elif api_choice == "3":
        return verify_email_abstract(email, api_key)
    elif api_choice == "4":
        return verify_email_emailrep(email)
    elif api_choice == "5":
        return verify_email_zerobounce(email, api_key)
    elif api_choice == "6":
        return verify_email_kickbox(email, api_key)
    else:
        return "unknown"

def option_name_mode(api_choice, api_key):
    first = input("Enter first name: ").strip().lower()
    last = input("Enter last name: ").strip().lower()
    phone = input("Enter phone number (optional, digits only): ").strip()
    print("\n[+] Choose a sub-option:")
    print("1. Include birthday in permutations")
    print("2. No birthday — just names + common numbers")
    sub = input("Your choice (1/2): ").strip()
    birthday_info = {}
    if sub == "1":
        b_day = input("Enter birth day (1-31): ").zfill(2)
        b_month = input("Enter birth month (1-12): ").zfill(2)
        b_year = input("Enter birth year (yyyy): ")
        birthday_info = {
            "day": b_day,
            "month": b_month,
            "year": b_year,
            "yy": b_year[-2:]
        }
    domain = "gmail.com"
    numbers = ["", "1", "12", "123", "111", "01", "02", "007"]
    emails = []
    def add_permutations(base):
        for n in numbers:
            emails.append(f"{base}{n}@{domain}")
        if birthday_info:
            emails.append(f"{base}{birthday_info['year']}@{domain}")
            emails.append(f"{base}{birthday_info['yy']}@{domain}")
            emails.append(f"{base}{birthday_info['day']}{birthday_info['month']}@{domain}")
            emails.append(f"{base}{birthday_info['month']}{birthday_info['day']}@{domain}")
        if phone:
            emails.append(f"{base}{phone}@{domain}")
            emails.append(f"{base}{phone[-4:]}@{domain}")
            emails.append(f"{base}{phone[-6:]}@{domain}")
            emails.append(f"{base}{phone[:4]}@{domain}")
            emails.append(f"{base}{phone[:6]}@{domain}")
    bases = [
        f"{first}{last}",
        f"{first}.{last}",
        f"{first}_{last}",
        f"{first[0]}{last}",
        f"{first}{last[0]}",
        f"{last}{first}",
        f"{last}.{first}",
        f"{first}",
        f"{last}",
        f"{first[0]}.{last}",
        f"{first}.{last[0]}"
    ]
    # Add phone number as its own base
    if phone:
        bases.append(phone)
        bases.append(phone[-4:])
        bases.append(phone[-6:])
    for base in bases:
        add_permutations(base)
    emails = list(set(emails))
    print(f"\n[*] {len(emails)} email guesses generated.")
    print("[*] Verifying emails...\n")
    valid_count = 0
    invalid_count = 0
    unknown_count = 0
    for email in emails:
        status = verify_email(email, api_choice, api_key)
        if status == "valid":
            print(f"[+] {email} is VALID ✅")
            valid_count += 1
        elif status == "invalid":
            print(f"[-] {email} is INVALID ❌")
            invalid_count += 1
        else:
            print(f"[?] {email} is UNKNOWN ⚠")
            unknown_count += 1
    print("\n=== Scan Summary ===")
    print(f"Total scanned: {len(emails)}")
    print(f"Valid:   {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Unknown: {unknown_count}")

def option_email_mode(api_choice, api_key):
    email = input("Enter the email address to verify: ").strip()
    print(f"\n[*] Checking {email} ...")
    status = verify_email(email, api_choice, api_key)
    valid_count = 0
    invalid_count = 0
    unknown_count = 0
    if status == "valid":
        print(f"[+] {email} is VALID ✅")
        valid_count += 1
    elif status == "invalid":
        print(f"[-] {email} is INVALID ❌")
        invalid_count += 1
    else:
        print(f"[?] {email} is UNKNOWN ⚠")
        unknown_count += 1
    print("\n=== Scan Summary ===")
    print(f"Total scanned: 1")
    print(f"Valid:   {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Unknown: {unknown_count}")

def option_random_mode(api_choice, api_key):
    count = int(input("How many random Gmail addresses to generate? "))
    # Example wordlist, you can expand this
    words = ["john", "jane", "alex", "beksloy", "eleven", "user", "test"]
    emails = []
    for _ in range(count):
        word = random.choice(words)
        # Randomly choose to add a number (could be a birthday, year, etc.)
        if random.random() < 0.7:
            number = str(random.randint(0, 99)).zfill(2)
            email = f"{word}{number}@gmail.com"
        else:
            email = f"{word}@gmail.com"
        emails.append(email)
    emails = list(set(emails))
    print(f"\n[*] {len(emails)} random emails generated.")
    print("[*] Verifying emails...\n")
    valid_count = 0
    invalid_count = 0
    unknown_count = 0
    for email in emails:
        status = verify_email(email, api_choice, api_key)
        if status == "valid":
            print(f"[+] {email} is VALID ✅")
            valid_count += 1
        elif status == "invalid":
            print(f"[-] {email} is INVALID ❌")
            invalid_count += 1
        else:
            print(f"[?] {email} is UNKNOWN ⚠")
            unknown_count += 1
    print("\n=== Scan Summary ===")
    print(f"Total scanned: {len(emails)}")
    print(f"Valid:   {valid_count}")
    print(f"Invalid: {invalid_count}")
    print(f"Unknown: {unknown_count}")

def menu():
    print(BANNER)
    print("=== Verified Gmail Guessing Tool ===")
    print("Choose an option:")
    print("1. Name-based guessing & verify")
    print("2. Verify a single email")
    print("3. Random/guessing mode")
    print("4. Exit")

def main():
    while True:
        menu()
        choice = input("\nYour choice (1/2/3/4): ").strip()
        if choice in ("1", "2", "3"):
            api_choice = get_api_choice()
            if api_choice == "4":
                api_key = None
            else:
                api_key = get_api_key(api_choice)
                if not api_key:
                    print("API key required.")
                    continue
            if choice == "1":
                option_name_mode(api_choice, api_key)
            elif choice == "2":
                option_email_mode(api_choice, api_key)
            elif choice == "3":
                option_random_mode(api_choice, api_key)
        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.\n")

if __name__ == "__main__":
    main()