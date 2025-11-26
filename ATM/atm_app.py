import json
import os
from pathlib import Path

def get_path(filename):
    try:
       base_dir = Path(__file__).resolve().parent
    except NameError:
        base_dir = Path(os.getcwd())
        
    file_path = base_dir / filename
    return file_path

def file_maker(dictionary, filepath):
    try:
        with open(filepath, "w", encoding='utf-8') as file:
            json.dump(dictionary, file, indent=4)
    except  Exception as e:
        print("Error: ",e)
    

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

def loggin_func(accounts):
    input_username = input("Username: ").strip()
    input_pin = input("PIN code: ").strip()
    if input_username in accounts:
        if input_pin == accounts[input_username]["pin"]:
            print(f"{' '*6} Welcome ")
            return input_username
        else:
            print("Invalid PIN code. Try again")
            return None
    else:
        print("Card number not found.")
        return None

     
def deposite(accounts, logged_in_pin):
    try:
        deposit_amount = float(input("Enter amount to deposit: ").strip())
        if deposit_amount <= 0:
            print("Amount must be positive.")
            return
        accounts[logged_in_pin]["balance"] += deposit_amount
        print(f"Deposited ${deposit_amount:.2f}. New balance: ${accounts[logged_in_pin]['balance']:.2f}")
    except ValueError:
        print("Invalid amount format.")
    except Exception as e:
        print("Error: ", e)

def withdraw(accounts, logged_in_pin):
    try:
        wid_amount = float(input("Enter amount to withdraw: ").strip())
        current_balance = accounts[logged_in_pin]["balance"]
            
        if wid_amount <= 0:
            print("Amount must be positive.")
            return
                
        if wid_amount >= current_balance:
            print("Insufficient balance.")
            return
                
        accounts[logged_in_pin]["balance"] -= wid_amount
        print(f"Withdrew ${wid_amount:.2f}. New balance: ${accounts[logged_in_pin]['balance']:.2f}")
        
    except ValueError:
        print("Invalid amount format.")
    except Exception as e:
        print("Error: ", e)


def balance_check(accounts, logged_in_pin):
    current_balance = accounts[logged_in_pin]["balance"]
    print(f"Your balance is ${current_balance:.2f}")


def main():
    FILEPATH = get_path("accounts.json") 
    all_accounts = load_accounts(FILEPATH)
    logged_in_pin = None

    print(f"{' '*5} Welcome!   \n1. Registration  \n2. Log_in  \n3. Exit")
    option = input("Please chose option ")
    if option == "1":
        new_account = account_maker(all_accounts)
    
    elif option == "2":
        loggin_func(all_accounts)
        #................................
        #...............................
        # მომხმარებლის შენახვა, 
        #ბალანსების განახლება-შეამოწმე!!!

        print("1. deposite \n2. withdraw   \n3. Balance  ")
        question = input("type your option ")
        if question == "1":
            result = deposite(all_accounts)
        elif question == "2":
            resunt = withdraw(all_accounts)
        else:
            result = balance_check(all_accounts)
    else:
        exit
    
main()

