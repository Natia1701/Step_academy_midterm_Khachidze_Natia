import json
import os
from pathlib import Path

#ფაილის მისამართის ზუსტად განსაზღვრა
def get_path(filename):
    try:
       base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path(os.getcwd())
        
    file_path = base_dir / filename
    return file_path

#ფაილში მონაცემების  ჩაწერა
def file_maker(dictionary, filepath):
    try:
        with open(filepath, "w", encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)
    except  Exception as e:
        print("Error: ",e)
    
#ფაილიდან მონაცემების წაკითხვა, თუ ფაილი არ არსებობს შექმნის ახალ ფაილს
def load_accounts(filepath):
    if not Path(filepath).exists():
        print("File Not Found")
        try:
            with open(filepath, 'w', encoding='utf-8') as file:
                json.dump({}, file, indent=4) 
        except Exception as e:
            print(f"Error: {e}")
            return {} 
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            accounts = json.load(file)
            for card_num, data in accounts.items():
                data["balance"] = float(data["balance"]) 
            return accounts
            
    except json.JSONDecodeError:
        print(f"File is dameged")
        return {}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

# ახალი მომხმარებლის რეგისტრაცია
# ამოწმებს უკვე არსებობს თუ არა ეს ექაუნთი
def account_maker(accounts):
    while True:
        card_number = input("PLease enter Your card number (use only numbers, card number is 16 digit number): - ").strip()
        if  not card_number.isdigit() or len(card_number) != 16:
            print("Invalid input. try again.")
            continue
        if card_number in accounts:
            print("This acount already axists.")
            return None
        break
    
    while True:
        pin = input("Please enter your pasword (use only numbers, pasword): ").strip()
        if not pin.isdigit() or len(pin) != 4:
            print("invalid input, please try again.")
            continue
        break

    while True:
        initial_amount = input("Please enter number of amount on your card")
        try:
            amount = float(initial_amount)
            if amount < 0:
                print("Initial amount cannot be negative.")
                continue
            
            break # გამოდის ციკლიდან წარმატების შემთხვევაში
            
        except ValueError:
            print("Invalid input. Amount must be a valid number.")
            continue
    print(f"Your Username is {card_number} and pin code is {pin}")
    return { card_number: {
            "pin number": pin,
            "balance": amount
        }
    }

# არსებული ექაუნთის გამოძახება
def loggin_func(accounts):
    input_username = input("Username: ").strip()
    input_pin = input("PIN code: ").strip()
    if input_username in accounts:
        if input_pin == accounts[input_username]["pin number"]:
            print(f"{' '*6} Welcome ")
            return input_username
        else:
            print("Invalid PIN code. Try again")
            return None
    else:
        print("Card number not found.")
        return None

 # არსებულ ექაუნთზე თანხის დამატება    
def deposite(accounts, logged_in_card_number):
    try:
        deposit_amount = float(input("Enter amount to deposit: ").strip())
        if deposit_amount <= 0:
            print("Amount must be positive.")
            return
        accounts[logged_in_card_number]["balance"] += deposit_amount
        print(f"Deposited ${deposit_amount:.2f}. New balance: ${accounts[logged_in_card_number]['balance']:.2f}")
    except ValueError:
        print("Invalid amount format.")
    except Exception as e:
        print("Error: ", e)

 # არსებულ ექაუნთიდან თანხის გამოტანა
def withdraw(accounts, logged_in_card_number):
    try:
        wid_amount = float(input("Enter amount to withdraw: ").strip())
        current_balance = accounts[logged_in_card_number]["balance"]
            
        if wid_amount <= 0:
            print("Amount must be positive.")
            return
                
        if wid_amount >= current_balance:
            print("Insufficient balance.")
            return
                
        accounts[logged_in_card_number]["balance"] -= wid_amount
        print(f"Withdrew ${wid_amount:.2f}. New balance: ${accounts[logged_in_card_number]['balance']:.2f}")
        
    except ValueError:
        print("Invalid amount format.")
    except Exception as e:
        print("Error: ", e)

# ბალანსის შემოწმება
def balance_check(accounts, logged_in_card_number):
    current_balance = accounts[logged_in_card_number]["balance"]
    print(f"Your balance is ${current_balance:.2f}")


# ATM აპლიკაციის მართვის ფუნქცია
def main():
    FILEPATH = get_path("accounts.json") 
    all_accounts = load_accounts(FILEPATH)
    logged_in_pin = None

    print(f"{' '*5} Welcome!   \n1. Registration  \n2. Log_in  \n3. Exit")
    option = input("Please chose option ").strip()
    if option == "1":
        new_account = account_maker(all_accounts)
        if new_account:
            all_accounts.update(new_account) 
            print("Account created successfully!")
            
            #ვინახავთ მონაცემებს json ფაილში
            file_maker(all_accounts, FILEPATH)
            print("Account data saved.")
    
    elif option == "2":
        logged_in_card_num = loggin_func(all_accounts)
        if logged_in_card_num:
            while True:
                print("     Menu:  ")
                print("1. deposite \n2. withdraw   \n3. Balance   \n4. Exit ")
                question = input("type your option ").strip()
                if question == "1":
                    deposite(all_accounts, logged_in_card_num)
                elif question == "2":
                    withdraw(all_accounts, logged_in_card_num)
                elif question == "3":
                    balance_check(all_accounts, logged_in_card_num)
                elif question == "4":
                    print("Logging out...")

                    file_maker(all_accounts, FILEPATH) 
                    print("Changes saved successfully!")
                    break
                else:
                    print("Invalid option. Please choose 1, 2, 3, or 4.")
        else:
            print("Login failed. Returning to main menu.")
    elif option == "3":
        print("Goodbye")
    else:
        print("Invalid option. Exiting.")
    
if __name__ == "__main__":
    main()

