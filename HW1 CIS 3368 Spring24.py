import mysql.connector
from mysql.connector import Error
# starting off by importing mysql connector and Error
def create_con(hostname, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            password = userpw,
            database = dbname
        )
        print("CON SUCCESS")
    except Error as e:
        print(f'The error {e} occurred')
    return connection
# then came time to define the connection and labeling each parameter when setting up the connection
# making sure that if the connection was successful, a message would appear confirming so
class Drink_Menu:
    def __init__(self, name, price, description, color):
        self.name = name
        self.price = price
        self.description = description
        self.color = color 
# next came the task of  labeling the parameters for the drink menu structure 

class Dive_bar:
    def __init(self, connection):
        self.connection = connection
        self.drinks = self.load_drinks_from_db()
        self.order = []
# above is the defined class of Dive_bar where a connection is made
    def generate_drinks_from_db(self):
        drinks = []
        cursor = conn.cursor(dictionary = True)
        sql = 'SELECT * FROM drinks'
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            drinks.append(Drink(row['name'], row['price'], row['description'], row['color']))
        cursor.close()
        return drinks
# this section would also be where the cursor is created and where the database would be called upon to output the drinks from MySQL

def main():
    conn = create_con('cis3368spring.crmi0e6cq704.us-east-1.rds.amazonaws.com', 'admin', 'cis3368spring24', 'cis3368springdb')
    if conn is not None:
        bar = Dive_bar(conn)
        while True:
            print("\nAvailable drinks:")
            bar.display_drinks()
            choice = input("Do you want to start an order (type 'order') or get information about a drink (type 'info')? (q to quit): ").strip().lower()
            if choice == 'q':
                break
            elif choice == 'info':
                try:
                    drink_number = int(input("Enter the number of the drink you want more info on: "))
                    bar.get_drink_info(drink_number)
                except ValueError:
                    print("Please enter a valid number.")
            elif choice == 'order':
                while True:
                    try:
                        drink_number = input("Enter the number of the drink to add to your order (q to finish): ")
                        if drink_number.lower() == 'q':
                            break
                        drink_number = int(drink_number)
                        bar.add_to_order(drink_number)
                    except ValueError:
                        print("Please enter a valid number.")
                    more = input("Would you like to add another drink? (y/n): ").strip().lower()
                    if more != 'y':
                        break
                bar.calculate_total()

        conn.close()
    else:
        print("Failed to connect to the database.")
# the bulk of this section is where the main code comes from, as it pertains to the program asking the user about the available drinks and takes the orders
# placed; making the calculation of the total that the drinks amount to 
if __name__ == "__main__":
    main()