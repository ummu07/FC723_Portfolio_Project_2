#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  9 23:09:01 2025

@author: ummusalmahumarrani
"""
# === FC723 BANKING APPLICATION===
# Developed for Portfolio Project 2
# Object-Oriented Pyhton Application with 2's Complement Balance Handling 


# === ACCOUNT CLASS ===
class Account:
    def __init__(self, username, password, balance, contact_info):
        """
        Constructor for the Account class.
        Initializes the account with a username, password, and starting balance.
        Balance is stored internally in 2's complement binary format.
        """
        self.username = username
        self.password = password
        self.failed_attempts = 0  # Track login attempts for security 
        self.contact_info = contact_info # Email or phone number 
        self.transaction_history = [] # List to store recent activity 
        self.balance = self.to_twos_complement(balance) 

    def to_twos_complement(self, value):
        """
        Converts a signed integer to a 16-bit 2's complement binary value.
        - Handles both positive and negative numbers. 
        """
        if value < 0:
            value = (1 << 16) + value
        return value

    def from_twos_complement(self):
        """
        Converts the stored 16-bit 2's complement binary balance back to a signed integer.
        - This is what gets displayed to the user.
        """
        if self.balance & (1 << 15):
            return self.balance - (1 << 16)
        else:
            return self.balance

    def check_password(self, input_password):
        """
        Compares the input password with the stored password. 
        - If matched, resests failed attempts and returns True. 
        - Otherwise, increments the failedd attempt count and return False.
        """
        if input_password == self.password:
            self.failed_attempts = 0
            return True
        else:
            self.failed_attempts += 1
            return False

    def deposit(self, amount):
        """
        Adds money to the account balance.
        - Converts current balance to decimal. 
        - Adds the amount and converts it back to 2's complement.'
        """
        current = self.from_twos_complement()
        current += amount
        self.balance = self.to_twos_complement(current) 
        self.transaction_history.append(f"Deposited £{amount}")
        print(f"📩 ALERT: £{amount} credited. New balance: £{current} sent to {self.contact_info}") 

    def withdraw(self, amount):
        """
        Attempts to withdraw money from the account.
        - Only allows withdrawal if it won't exceed a £1500 overdraft limit.
        - Returns True if successful, False otherwise. 
        """
        current = self.from_twos_complement()
        if current - amount >= -1500:
            current -= amount
            self.balance = self.to_twos_complement(current) 
            self.transaction_history.append(f"Withdraw £{amount}") 
            print(f"📩 ALERT: £{amount} debited. New balance: £{current} sent to {self.contact_info}") 
            return True
        else:
            return False

    def transfer(self, amount, other_account):
        """
        Transfers money from this account to another account.
        - Calls withdraw() on this account. 
        - If successful, calls deposit() on the other account.
        """
        if self.withdraw(amount):
            other_account.deposit(amount)
            self.transaction_history.append(f"Transferred £{amount} to {other_account.username}")
            print(f"📩 ALERT: £{amount} transferred to {other_account.username}") 
            return True
        else:
            return False 

    def get_balance(self):
        """
        Returns the current account balance in decimal format.
        - Converts the stored binary balance back to human-readable format. 
        """
        return self.from_twos_complement() 
    
    def show_mini_statement(self):
        """
        Displays the 5 most recent transactions.
        """
        print("===== MINI STATEMENT =====") 
        for transaction in self.transaction_history[-5:]:
            print(transaction) 


# === TESTING BLOCK ===
if __name__ == "__main__":
    # Create two account objects for testing
    acc1 = Account("user1", "securePass", 500, "user1@example.com")
    acc2 = Account("user2", "anotherPass", 1000, "user2@example.com") 

    # Perform operations
    acc1.deposit(100)
    acc1.withdraw(700)
    acc1.transfer(200, acc2)

    # Display results
    print("User1 Balance:", acc1.get_balance())
    print("User2 Balance:", acc2.get_balance()) 


# === BANKSYSTEM CLASS ===     
class BankSystem:
    def __init__(self):
        """
        Constructor for BankSystem.
        Initializes a dictionary to store all accounts by username. 
        Keys are usernames, values are Account objects. 
        """
        self.accounts = {} # Dictionary to store user accounts 
     
    def create_account(self): 
     
        """
        Prompts the user to create a new account.
        - Checks for unique username. 
        - Validates password length (8-16 characters) 
        - Prompts for initial deposit and creates Account object.
        """
        username = input("Choose a username: ")
        
        # Check if username is already taken
        if username in self.accounts:
            print("Error: username already exists.")
            return 
        
        # Prompt for password and validate length 
        password = input ("Choose a password (8-16 characters): ")
        if len(password) < 8 or len(password) > 16:
            print("Error: Password must be between 8 and 16 characters.") 
            return 
        
        # Prompt for initial deposit and validate input
        try:
            deposit = int(input("Enter your initial deposit amount: "))
        except ValueError:
            print("Error: Deposit must be a number.")
            return 
        
        # Create the new Account and add it to the dictionary 
        contact_info = input("Enter your email or phone number for alerts: ")
        new_account = Account(username, password, deposit, contact_info) 
        self.accounts[username] = new_account
        print(f"Account for '{username}' created successfully!") 
        
    def login(self):
        """
        Handles login for exiting users. 
        - Prompts for username and password.
        - Allows up to attempts before lockout.
        - Calls main menu if login is successful. 
        """
        username = input("Enter your username:") 

        
        # Check if the accounts exists
        if username not in self.accounts:
            print("Error: Account not found.")
            return 
        
        account = self.accounts[username]
        
        # Allow up to 3 login attempts 
        for attempt in range(3):
            password = input("Enter your password:")
            
            if account.check_password(password):
                print(f"Login successful. Welcome, {username}!\n")
                self.main_menu(account)
                return 
            else: 
                remaining = 2 - attempt
                print(f"Incorrect password. Attempts remaining: {remaining}")
                
        print("Too many failed attempts. You are now locked out.\n")
        
        
    def main_menu(self, account):
        """
        Display the main menu for a logged-in user.
        Allows actions: ckeck balance, deposit, wihtdraw, transfer, exit.
        Runs in a loop until the user chooses to exit. 
        """ 
        while True:
            print("\n===== Banking Menu =====")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. View Mini Statement")
            print("6. Exit") 
            
            choice = input("Enter your choice (1-6): ")
            
            if choice == "1":
                # Display account balance
                print(f"Your balance is: £{account.get_balance()}")
                
            elif choice == "2":
                # Handle deposit
                try: 
                    amount = int(input("Enter amount to deposit: ")) 
                    if amount > 0:
                        account.deposit(amount)
                        print(f"£{amount} deposited successfully.")
                    else:
                        print("Amount must be greater than 0.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
            elif choice == "3":
                # Handle withdrwal
                try:
                    amount = int(input("Enter amount to withdraw: ")) 
                    if account.withdraw(amount):
                        print(f"£{amount} withdrawn successfully. ")
                    else:
                        print("Insufficient funds or overdraft limit reached.")
                except ValueError:
                    print("Invalid input. Please enter a number. ")
                    
            elif choice =="4":
                # Handle transfer 
                target_username = input("Enter the recipient's username: ")
                
                if target_username not in self.accounts:
                    print("Recipient's account does not exist.")
                    continue 
                
                try:
                    amount = int(input("Enter amount to transfer: "))
                    if account.transfer(amount, self.accounts[target_username]): 
                        print(f"Transfered £{amount} to {target_username}.")
                    else: 
                        print("Transfer failed. Check your balance.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
            elif choice == "5":
                account.show_mini_statement() 
                
            elif choice == "6":
                print("Logging out. Thank you for banking with us.")
                break 
            
            else: 
                print("Invalid selection. Please try again.")
                
      
# === PROGRAM ENTRY POINT ===                
if __name__ == "__main__":
    """ 
    Entry point of the banking application. 
    Shows a welcome menu that lets users create an account, log in, or exit.
    """ 
    system = BankSystem() # Create an instance of BankSystem

    while True:
        print("==== Welcome to FC723 Bank ====")
        print("1. Open New Account") 
        print("2. Log In to Existing Account")
        print("3. Exist")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            system.create_account() # Call method to create a new user 
        elif choice == "2":
             system.login() # Call login method
        elif choice == "3":
            print("Thank you for using FC723 Bank. Goodbye!")
            break 
        else:
            print("Invalid choice. Please try again.\n") 