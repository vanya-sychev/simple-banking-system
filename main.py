import random
import sqlite3


class BankingSystem:
    card_number = int
    pin = str
    card_balance = int

    def create_an_account(self):
        self.pin = str(random.randint(1000, 9999))
        self.card_balance = 0

        print("\nYour card has been created")
        print(f"Your card number:\n{self.card_number}")
        print(f"Your card PIN:\n{self.pin}\n")

    def luna_algorithm(self):
        a = 1000000000
        b = 9999999999

        while True:
            self.card_number = "400000" + str(random.randint(a, b))

            # Step 1: Original number
            step_1 = self.card_number

            # Step 2: Drop the last digit
            step_2 = step_1[:-1]

            # Step 3: Multiply odd digits by 2
            step_3 = [int(step_2[i]) * 2
                      if i % 2 == 0 else int(step_2[i]) for i in range(0, 15)]

            # Step 4: Subtract 9 from numbers over 9
            step_4 = [i - 9 if i > 9 else i for i in step_3]

            # Step 5: Add all numbers
            step_5 = sum(step_4) + int(step_1[-1])

            if step_5 % 10 == 0:
                self.card_number = int(step_1)
                break

    def log_into_account(self):
        user_card = int(input("\nEnter your card number:\n"))
        user_pin = int(input("Enter your PIN:\n"))

        self.card_number = user_card
        self.pin = user_pin

        info = cur.execute(f"SELECT 1 AS 'Answer' "
                           f"FROM  card "
                           f"WHERE number = {user_card} AND pin = {user_pin};")

        if info.fetchone() is None:
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            return "Successfully"

    def account(self):
        while True:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")

            user_input = int(input())

            if user_input == 1:
                info = cur.execute(f"SELECT balance "
                                   f"FROM   card "
                                   f"WHERE  number = {self.card_number};")
                print(f"\nBalance: {info.fetchone()[0]}\n")
            elif user_input == 2:
                print("\nEnter income:")
                income = int(input())

                cur.execute(f"UPDATE card "
                            f"SET    balance = balance + {income} "
                            f"WHERE  number = {self.card_number}")
                conn.commit()

                print("Income was added!\n")
            elif user_input == 3:
                print("\nTransfer")
                print("Enter card number:")
                card_number = input()

                info = cur.execute(f"SELECT 1 AS 'Answer' "
                                   f"FROM card "
                                   f"WHERE number = {card_number};")

                step_1 = card_number
                step_2 = step_1[:-1]
                step_3 = [int(step_2[i]) * 2
                          if i % 2 == 0 else int(step_2[i])
                          for i in range(0, 15)]
                step_4 = [i - 9 if i > 9 else i for i in step_3]
                step_5 = sum(step_4) + int(step_1[-1])
                card_number = int(card_number)

                if card_number == self.card_number:
                    print("You can't transfer money to the same account!\n")
                elif step_5 % 10 != 0:
                    print("Probably you made a mistake in the card number. "
                          "Please try again!\n")
                elif info.fetchone() is None:
                    print("Such a card does not exist.\n")
                else:
                    print("Enter how much money you want to transfer:")
                    how_much_money = int(input())

                    inquiry = cur.execute(f"SELECT balance "
                                          f"FROM  card "
                                          f"WHERE "
                                          f"number = {self.card_number};")

                    if how_much_money > inquiry.fetchone()[0]:
                        print("Not enough money!\n")
                    else:
                        cur.execute(f"UPDATE card "
                                    f"SET    balance = balance "
                                    f"       + {how_much_money} "
                                    f"WHERE  number = {card_number}")
                        cur.execute(f"UPDATE card "
                                    f"SET    balance = balance "
                                    f"       - {how_much_money} "
                                    f"WHERE  number = {self.card_number}")
                        conn.commit()

                        print("Success!\n")
            elif user_input == 4:
                cur.execute(f"DELETE FROM card "
                            f"WHERE number = {self.card_number}")
                conn.commit()

                print("\nThe account has been closed!\n")
                break
            elif user_input == 5:
                print(f"\nYou have successfully logged out!\n")
                break
            elif user_input == 0:
                return "Buy!"

    def main_menu(self):
        while True:
            print("1. Create an account")
            print("2. Log into account")
            print("0. Exit")

            user_input = int(input())

            if user_input == 1:
                self.luna_algorithm()
                self.create_an_account()
                cur.execute(f"INSERT INTO card (number, pin, balance) "
                            f"VALUES ({self.card_number}, {self.pin}, "
                            f"{self.card_balance});")
                conn.commit()
            elif user_input == 2:
                if self.log_into_account() == "Successfully":
                    if self.account() == "Buy!":
                        print("\nBuy!")
                        break
            elif user_input == 0:
                print("\nBuy!")
                break


if __name__ == '__main__':
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS card("
                "id      INTEGER PRIMARY KEY,"
                "number  TEXT,"
                "pin     TEXT,"
                "balance INTEGER DEFAULT 0);")

    person = BankingSystem()
    person.main_menu()
