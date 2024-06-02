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
    def __init__(self, connection):
        """
        Initialize a new instance of the divebar class here
        """
        self.connection = connection
        self.drinks = self.load_drinks_from_db()
        self.order = []
# above is the defined class of Dive_bar where a connection is made
    def load_drinks_from_db(self):
        """
        Load the drinks from the DB, return them as a list of Drink_Menu objects
        """
        drinks = []
        cursor = self.cursor(dictionary = True)
        sql = 'SELECT * FROM drinks'
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            drinks.append(Drink_Menu(row['name'], row['price'], row['description'], row['color']))
        cursor.close()
        return drinks
# this section would also be where the cursor is created and where the database would be called upon to output the drinks from MySQL

    def display_drinks(self):
        """
        Display the list of available drinks with their corresponding numbers and prices
        """
        for i, drink in enumerate(self.drinks, start=1):
            print(f"{i} - {drink.name}: ${drink.price:.2f}")
    
    def get_drink_info(self, drink_number):
        """
        Retrieve and display the description and color of the specified drink
        """
        if 1 <= drink_number <= len(self.drinks):
            drink = self.drinks[drink_number - 1]
            print(f"Name: {drink.name}")
            print(f"Description: {drink.description}")
            print(f"Color: {drink.color}")
        else:
            print("Invalid drink number.")

    def add_to_order(self, drink_number):
        """
        Add the specified drink to the order based on the drink number
        """
        if 1 <= drink_number <= len(self.drinks):
            drink = self.drinks[drink_number - 1]
            self.order.append(drink)
            print(f"{drink.name} added to order")
        else:
            print("Invalid drink number")

    def calculate_total(self):
        """
        Calculate the total
        """
        total = sum(drink.price for drink in self.order)
        print("\nReceipt:")
        for drink in self.order:
            print(f"{drink.name}: ${drink.price:.2f}")
        print(f"\nTotal: ${total:.2f}")

    

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

            try: 
                if choice == 'info':
                    drink_number = int(input("Enter the number of the drink you want more info on: "))
                    bar.get_drink_info(drink_number)
                elif choice == 'order':
                    while True:
                        drink_number = input("Enter the number of the drink to add to your order (q to finish): ")
                        if drink_number.lower() == 'q':
                            break
                        drink_number = int(drink_number)
                        bar.add_to_order(drink_number)
                        more = input("Would you like to add another drink? (y/n): ").strip().lower()
                        if more != 'y':
                            break
                    bar.calculate_total()
                else:
                    print("Invalid choice. Please enter 'order', 'info', or 'q' to quit")
            except ValueError:
                print("Please enter a valid number")
        conn.close()
    else:
        print("Failed to connect to the database.")
# the bulk of this section is where the main code comes from, as it pertains to the program asking the user about the available drinks and takes the orders
# placed; making the calculation of the total that the drinks amount to 
if __name__ == "__main__":
    main()