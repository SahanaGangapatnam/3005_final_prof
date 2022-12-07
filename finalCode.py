import psycopg2
import psycopg2.extras

hostname = 'localhost'
database = 'bookStore'
username = 'postgres'
pwd = 'password@123'
port_id = 5432

# prints user's options
def userOptions():
    print("-------------------OPTIONS-------------------")
    print("1) Search the Bookstore")
    print("2) Make an Account/Sign in")
    print("3) Make a Purchase")
    print("4) Track an Order")
    print("5) View Cart")
    print("6) Quit Program")
    print("---------------------------------------------")
    option_input = input("Select a Number from the List of Options: ")
    return option_input

# prints user's search options
def searchOptionsDisplay():
    print("-------------------OPTIONS-------------------")
    print("1) Search By ISBN")
    print("2) Search By Book Name")
    print("3) Search By Author Name")
    print("4) Search By Genre")
    print("5) Search By Price")
    print("---------------------------------------------")
    option_input = input("Select a Number from the List of Options: ")
    return option_input

# prints owner's options
def ownerOptions():
    print("-------------------OPTIONS-------------------")
    print("1) Add a Publisher")
    print("2) Add a New Book to Inventory")
    print("3) Remove a Book")
    print("4) View Statistics")
    print("5) Quit Program")
    print("---------------------------------------------")
    option_input = input("Select a Number from the List of Options: ")
    return option_input

# prints owner's stats options
def statsOptionsDisplay():
    print("-------------------OPTIONS-------------------")
    print("1) Sales per Genre")
    print("2) Sales per Author")
    print("3) Sales v. Expenditures")
    print("---------------------------------------------")
    option_input = input("Select a Number from the List of Options: ")
    return option_input

# asks for user input to add a publisher
def addPublisherToStore():
    name_input = input("Enter the Publisher's Name: ")
    address_input = input("Enter the Publisher's Address (Up to 40 Letters Including Spaces): ")
    email_input = input("Enter the Publisher's Email Address (Up to 20 Letters Including Spaces): ")
    phone_input = input("Enter the Publisher's Phone Number: ")
    banking_input = input("Enter the Publisher's Bank Acc Number (Atleast 15 Digits): ")
    return (name_input, address_input, email_input, phone_input, banking_input)

# asks for user input to add a book
def addBookToStore():
    isbn_input = input("Enter the ISBN number (Up to 15 Digits): ")
    book_input = input("Enter the Book Name (Up to 15 Letters Including Spaces): ")
    author_input = input("Enter the Author's Name (Up to 15 Letters Including Spaces): ")
    genre_input = input("Enter the Genre (Up to 20 Letters Including Spaces): ")
    num_input = input("Enter the Number of Pages: ")
    price_input = input("Enter the Price: ")
    quantity_input = input("Enter the Quantity: ")
    publisher_input = input("Enter the Publisher's Bank Acc Number (Atleast 15 Digits): ")
    return (isbn_input, book_input, author_input, genre_input, num_input, price_input, quantity_input, publisher_input)

# checks and prints out books that match a query
def checkQueryListResult(l, cart):
    if len(l) == 0:
        print("There are no Books Matching Your Query!")
    else:
        print("Here are the Books Matching Your Query: ")
        for row in l:
            final_string = ""
            for col in row:
                print(col, end=' ')
                # gets a string of the book to see if it should be added to cart
                final_string = final_string + str(col) + " "
            print()
            add_input = input("Would you Like to add the Book to Your Cart? (y/n): ")
            # adds book to cart if it does not already exist in cart
            if (add_input == 'y' and final_string not in cart):
                cart.append(final_string)
            print()
    return cart

def searchQueries(search_input, cart):
    # SEARCH BY ISBN
    if (search_input == "1"):
        isbn_input = input("Enter the ISBN number (Up to 15 Digits): ")
        cur.execute(f"SELECT * FROM books WHERE %s = isbn", (isbn_input,))

    # SEARCH BY BOOKNAME 
    elif (search_input == "2"):
        name_input = input("Enter the Book Name: ")
        cur.execute(f"SELECT * FROM books WHERE %s = bookname", (name_input,))
    
    # SEARCH BY AUTHORNAME
    elif (search_input == "3"):
        author_input = input("Enter the Author Name: ")
        cur.execute(f"SELECT * FROM books WHERE %s = authorname", (author_input,))

    # SEARCH BY GENRE
    elif (search_input == "4"):
        genre_input = input("Enter the Genre: ")
        cur.execute(f"SELECT * FROM books WHERE %s = genre", (genre_input,))

    # SEARCH BY PRICE
    elif (search_input == "5"):
        price_input = input("Enter the Price: ")
        cur.execute(f"SELECT * FROM books WHERE %s = price", (price_input,))
    
    else:
        print("ERROR: Input is Invalid!")
    
    # sends query matches to the other function
    if (int(search_input) > 0 and int(search_input) <= 5):
        match = cur.fetchall()
        return checkQueryListResult(match, cart)

# sign in for users and owner
def authenticatePerson(table_name):
    user_input = input('Enter your Username: ')
    pass_input = input('Enter your Password: ')
    query = "SELECT * FROM %s WHERE username = %%s AND userpass = %%s" % table_name
    cur.execute(query, (user_input, pass_input))
    match = cur.fetchall()
    if len(match) == 0:
        print("ERROR: Login Failed!")
    else:
        print(f"Login Succeeded {user_input}!")
        return (user_input, True, True)
    return("", False, False)

# if user isnt already logged in, creates an acc if they dont have one
# then sends to another function so they can log in
def checkOrCreateUserAccount(table_name):
    if (login == True):
        print("You're Already Logged in!")
    else:
        registered_input = input("Do you Have an Account with us? (y/n): ")
        
        if (registered_input == 'y'):
            return authenticatePerson(table_name)
        else:
            user_input = input('Please create a Username of Length 10 or Less: ')
            pass_input = input('Please create a Password of Length 10 or Less: ')
            query = "INSERT INTO %s (userName, userPass) VALUES (%%s, %%s)" % table_name
            cur.execute(query, (user_input, pass_input))
            print(f"Your Account has Been Added!")
            return authenticatePerson(table_name)

with psycopg2.connect(
    host = hostname, 
    dbname = database,
    user = username,
    password = pwd,
    port = port_id) as conn:

    with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        print("Welcome to Look Inna Book!")
        type_input = input("Are you a User (1) or an Owner (2): ")
        print(f"Welcome!")
        login = False
        user = False
        owner = False
        user_name = ""
        cart = []
        status_list = ['Not Packaged', 'Packaged', 'Not Delivered', 'Delivered', 'In Transit', 'Reached']

        # USER PORTION
        if (type_input == '1'):
            while True:
                option_input = userOptions()
                                
                # SEARCH BOOKSTORE
                if (option_input == "1"):
                    search_input = searchOptionsDisplay()
                    cart = searchQueries(search_input, cart)
                    print(cart)

                # MAKE AN ACC/SIGN IN
                elif (option_input == "2"): 
                    (user_name, login, user) = checkOrCreateUserAccount("USERS")

                # MAKE A PURCHASE
                elif (option_input == "3"):
                    if (login == True and user == True and len(cart) > 0):
                        billing_address_input = input("Please Enter Your Billing Address: ")
                        shipping_address_input = input("Please Enter Your Shipping Address: ")

                        cur.execute(f"INSERT INTO ORDERS (ordernum, status, billingaddress, shippingaddress, username) VALUES (nextval('order_num_seq'), %s, %s, %s, %s)", (status_list[0], billing_address_input, shipping_address_input, user_name))
                        
                        for order in cart:
                            print(order)
                            isbn = order.split(" ")[0]
                            cur.execute(f"SELECT quantity, price FROM BOOKS WHERE isbn = %s", (isbn,))

                            match = cur.fetchone()

                            num_input = input(f"How Many of This Book do you Wish to Purchase? There are only {match[0]} in Stock!: ")
                            
                            # please refer to 'queries.sql' to get an explanation for the queries below
                            cur.execute(f"INSERT INTO HAVE (ordernumber, bookisbn, numbooksordered, subtotal) VALUES (currval('order_num_seq'), %s, %s, (%s * %s))", (isbn, num_input, match[1], num_input))

                            cur.execute(f"UPDATE BOOKS SET quantity = (%s - %s) WHERE isbn = %s", (match[0], num_input, isbn))

                            cur.execute(f"UPDATE PUBLISH SET royalty = (royalty + ((%s * 0.15) * %s) ) WHERE bookisbn = %s", (match[1], num_input, isbn))

                            cur.execute(f"SELECT last_value FROM order_num_seq")

                        match = cur.fetchone()
                        print(f"Your Order has been Confirmed! Your Order Number is {match[0]}. Thank you for Shopping with us!")
                        cart = []

                    elif (login == True and user == True and len(cart) == 0):
                        print("Your cart is Empty!")
                    else:
                        print("ERROR: You must be Logged in to make a Purchase!")
                
                # TRACK AN ORDER
                elif (option_input == "4"):
                    if (login == True and user == True):
                        order_input = input("Enter your Order Number: ")

                        cur.execute(f"SELECT status FROM ORDERS WHERE %s = ordernum AND %s = username", (order_input, user_name))

                        match = cur.fetchone()

                        if (match == None):
                            print("ERROR: Order with the Order Number provided does not Exist for Your Account!")
                        elif (match[0] != status_list[-1]):
                            # gets the next status from the status list
                            next_status = status_list[status_list.index(match[0]) + 1]
                            
                            cur.execute(f"UPDATE orders SET status = %s WHERE %s = ordernum AND %s = username", (next_status, order_input, user_name))
                            print(next_status)
                        else:
                            print(status_list[-1])
                    else:
                        print("ERROR: You must be Logged in to Track your Order!")

                # VIEW CART
                elif (option_input == "5"):
                    print("Here's Your Cart: ")
                    print(cart)

                # QUIT PROGRAM
                elif (option_input == "6"):
                    print("Quitting Program.")
                    break

                else:
                    print("ERROR: Input is Invalid!")

                   
        # OWNER PORTION
        if (type_input == '2'):
            (user_name, login, owner) = checkOrCreateUserAccount("OWNERS")

        if (login == True and owner == True):
            while True:
                option_input = ownerOptions()

                # ADDING PUBLISHER
                if (option_input == "1"):
                    (name_input, address_input, email_input, phone_input, banking_input) = addPublisherToStore()
                    cur.execute(f"INSERT INTO PUBLISHERS (publishername, address, emailadd, phonenum, bankingacc) VALUES (%s, %s, %s, %s, %s)", (name_input, address_input, email_input, phone_input, banking_input))
                    print("Publisher has Been Added!")

                # ADDING BOOKS
                elif (option_input == "2"):
                    (isbn_input, book_input, author_input, genre_input, num_input, price_input, quantity_input, publisher_input) = addBookToStore()
                    
                    # check if publisher exists
                    cur.execute(f"SELECT * FROM PUBLISHERS WHERE bankingacc = %s", (publisher_input,))
                    match = cur.fetchall()
                    if len(match) == 0:
                        print("ERROR: The Publisher you Provided Doesn't Exist in the Bookstore Database! Please add Them Before Re-attempting.")
                    else:
                        cur.execute(f"INSERT INTO BOOKS (isbn, bookname, authorname, genre, numofpages, price, quantity, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (isbn_input, book_input, author_input, genre_input, num_input, price_input, quantity_input, user_name))
                        print(f"Book has been Added By {user_name}!")

                        cur.execute(f"INSERT INTO PUBLISH (pubbankingacc, bookisbn) VALUES (%s, %s)", (publisher_input, isbn_input))

                # REMOVING BOOKS
                elif (option_input == "3"):
                    delete_isbn_input = input("Enter the ISBN number (Up to 15 Digits): ")
                    
                    # check if book actually exists
                    cur.execute(f"SELECT * FROM BOOKS WHERE isbn = %s", (delete_isbn_input,))
                    match = cur.fetchall()

                    if len(match) == 0:
                        print("ERROR: Book with the ISBN provided does not Exist!")
                    else:
                        cur.execute(f"DELETE FROM PUBLISH WHERE bookisbn = %s", (delete_isbn_input,))

                        cur.execute(f"DELETE FROM HAVE WHERE bookisbn = %s", (delete_isbn_input,))

                        cur.execute(f"DELETE FROM BOOKS WHERE isbn = %s", (delete_isbn_input,))
                        print("Book has been Deleted!")
                
                # ADD STATS
                elif (option_input == "4"):
                    match = []
                    stats_input = statsOptionsDisplay()

                    if (stats_input == "1"):
                        cur.execute(f"SELECT genre, sum(subtotal) AS sales FROM BOOKS JOIN HAVE ON BOOKS.isbn = HAVE.bookisbn GROUP BY genre")
                        match = cur.fetchall()

                    elif (stats_input == "2"):
                        cur.execute(f"SELECT authorname, sum(subtotal) AS sales FROM BOOKS JOIN HAVE ON BOOKS.isbn = HAVE.bookisbn GROUP BY authorname")
                        match = cur.fetchall()

                    elif (stats_input == "3"):
                        cur.execute(f"SELECT sum(subtotal) AS sales, sum(quantity * price) AS expenditures FROM BOOKS JOIN HAVE ON BOOKS.isbn = HAVE.bookisbn")
                        match = cur.fetchall()
                    
                    else:
                        print("ERROR: Input is Invalid!")


                    if (len(match) == 0):
                        print("ERROR: No Stats Available!")
                    else:
                        for row in match:
                            for col in row:
                                print(col, end=' ')
                            print()

                # QUITTING
                elif (option_input == "5"):
                    print("Quitting Program.")
                    break

                else:
                    print("ERROR: Input is Invalid!")

conn.close()