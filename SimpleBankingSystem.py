import random
import _sqlite3
conn = _sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card")
create_table = 'create table if not exists card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);'
insert_data1 = "insert into card(number, pin) values (?, ?);"
insert_id = "insert into card(id) values (?);"
get_number1 = "select * from card where number = ?;"
all_data = "select * from card;"
update = "update card set balance=? where number=?;"
delete = "delete from card where number = ?;"
cur.execute(create_table)

def lhn_algorithm(card_number):
    number = list(card_number)
    for i in range(15):
        if (i + 1) % 2 != 0:
            number2 = int(number[i]) * 2
            number[i] = str(number2)

    for i in number:
        if int(i) > 9:
            number2 = number.index(i)
            number[number2] = str(int(i) - 9)
    sum1 = 0
    for i in range(len(number)):
        sum1 += int(number[i])
    count = 0
    if sum1 % 10 != 0:
        while True:
            sum1 += 1
            count += 1
            if sum1 % 10 == 0:
                break
    else:
        count = 0
    number = str(card_number)
    number = list(number)
    number.append(str(count))
    card_number_new = "".join(number)
    return card_number_new
def lhn_algorithm2(card_number):
    number = list(card_number)
    for i in range(15):
        if (i + 1) % 2 != 0:
            number2 = int(number[i]) * 2
            number[i] = str(number2)

    for i in number:
        if int(i) > 9:
            number2 = number.index(i)
            number[number2] = str(int(i) - 9)
    sum1 = 0
    for i in range(len(number)):
        sum1 += int(number[i])
    return sum1 % 10 != 0
def create_account():
    cards_query = conn.execute("SELECT number FROM card").fetchall()
    account_list = []
    for i in range(len(cards_query)):
        account_list.append(cards_query[i][0][6:-1])
    account_identifier = ''.join(str(random.randint(0, 9)) for _ in range(9))
    while account_identifier in account_list:
        account_identifier = ''.join(str(random.randint(0, 9)) for _ in range(9))
    else:
        account_list.append(account_identifier)
        BIN_account = "400000" + account_identifier
        list_BIN_account = list(BIN_account)

        # Convert to integer
        for i in range(len(list_BIN_account)):
            list_BIN_account[i] = int(list_BIN_account[i])

        # Multiply odd positions by 2
        for i in range(len(list_BIN_account)):
            if i % 2 == 0 or i == 0:
                list_BIN_account[i] *= 2

        # Subtract 9
        for i in range(len(list_BIN_account)):
            if list_BIN_account[i] > 9:
                list_BIN_account[i] -= 9

        # Sum all numbers
        checksum = sum(list_BIN_account)

        # Checksum + last digit
        if checksum % 10 == 0:
            account_number = BIN_account + "0"
        else:
            last_digit = str(10 - (checksum % 10))
            account_number = BIN_account + last_digit

    PIN = ''.join(str(random.randint(0, 9)) for _ in range(4))
    conn.execute("INSERT INTO card (number, pin) VALUES (?, ?)", (account_number, PIN))
    conn.commit()
    print("\nYour card has been created\nYour card number:\n{}\nYour card PIN:\n{}\n".format(account_number, PIN))

data = {}
id = 0
while True:
    print("""
1. Create an account
2. Log into account
0. Exit""")
    take_input = int(input())
    if take_input == 1:
        print("")
        create_account()
        print("")


    elif take_input == 2:
        print("")


        enter_acc = input("Enter your card number:\n")
        passwor = input("Enter your PIN:\n")

        data11 = cur.execute(("select number, pin from card where number=?"), (enter_acc,)).fetchall()
        print()
        try:

            if passwor == data11[0][1]:
                print("")
                print("You have successfully logged in!")
                while True:
                    print("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
                    input2 = int(input())
                    if input2 == 1:
                        print("")
                        data12 = cur.execute(("select number, balance from card where number=?"),(enter_acc,)).fetchall()
                        print(f'Balance: {data12[0][1]}')
                    elif input2 == 2:
                        print("")
                        income = int(input("Enter income:\n"))
                        data15 = cur.execute(("select number, balance from card where number=?"),(enter_acc,)).fetchall()
                        income1 = data15[0][1] + income
                        cur.execute(("Update card set balance = ? where number = ?"), (income1, enter_acc))
                        conn.commit()
                        print("Income was added!")
                    elif input2 == 3:
                        print("")
                        print("Transfer")

                        card_info = input("Enter card number:\n")
                        get_clr = lhn_algorithm2(card_info)
                        if get_clr != 0:
                            print("Probably you made a mistake in the card number. Please try again!")
                        elif get_clr == 0:
                            if enter_acc != card_info:
                                details = cur.execute(("select number from card where number=?"), (card_info,)).fetchall()
                                if details == []:
                                    print("Such a card does not exist.")
                                else:
                                    add = int(input("Enter how much money you want to transfer:\n"))
                                    data13 = cur.execute(("select number, balance from card where number=?"), (enter_acc,)).fetchall()

                                    if data13[0][1] < add:
                                        print("not enough money")
                                    else:
                                        modify = data13[0][1] - add
                                        cur.execute(("Update card set balance = ? where number = ?"),
                                                    (modify, enter_acc))
                                        conn.commit()
                                        data14 = cur.execute(("select number, balance from card where number=?"), (card_info,)).fetchall()
                                        modify1 = data14[0][1] + add
                                        cur.execute(("Update card set balance = ? where number = ?"),
                                                    (modify1, card_info))
                                        conn.commit()
                                        print("Success!")
                            else:
                                print("You can't transfer money to the same account!")

                    elif input2 == 4:
                        print("")
                        cur.execute(("delete from card where number=?"), (enter_acc,))
                        conn.commit()
                        print("The account has been closed!")
                    elif input2 == 5:
                        print("")
                        print("You have successfully logged out!")
                        break

                    elif input2 == 0:
                        exit()
            else:
                print("")
                print("Wrong card number or PIN!")
        except KeyError:
            print("")
            print("Wrong card number or PIN!")
        except IndexError:
            print("")
            print("Wrong card number or PIN!")
        except TypeError:
            print("")
            print("Wrong card number or PIN!")
    elif take_input == 0:
        print("Bye!")
        break



