/* Retrieves all the books with the provided isbn */
cur.execute(f"SELECT * FROM books WHERE %s = isbn", (isbn_input,))

/* Retrieves all the books with the provided book name */
cur.execute(f"SELECT * FROM books WHERE %s = bookname", (name_input,))

/* Retrieves all the books with the provided author name */
cur.execute(f"SELECT * FROM books WHERE %s = authorname", (author_input,))

/* Retrieves all the books with the provided genre */
cur.execute(f"SELECT * FROM books WHERE %s = genre", (genre_input,))

/* Retrieves all the books with the provided price */
cur.execute(f"SELECT * FROM books WHERE %s = price", (price_input,))

/* 
Checks if the credentials provided are located in the owner or user table
whichever table_name is provided
 */
query = "SELECT * FROM %s WHERE username = %%s AND userpass = %%s" % table_name
cur.execute(query, (user_input, pass_input))

/* Inserts the provided username and password in owners or users table */
query = "INSERT INTO %s (userName, userPass) VALUES (%%s, %%s)" % table_name
cur.execute(query, (user_input, pass_input))

/* Inserts the provided order details into the orders table */
cur.execute(f"INSERT INTO ORDERS (ordernum, status, billingaddress, shippingaddress, username) VALUES (nextval('order_num_seq'), %s, %s, %s, %s)", (status_list[0], billing_address_input, shipping_address_input, user_name))

/* Gets the quantity and price of book with provided isbn*/
cur.execute(f"SELECT quantity, price FROM BOOKS WHERE isbn = %s", (isbn,))

/* 
Inserts the details into the have table. This table exists because the 
relationship between ORDERS and BOOKS is many to many. This relationship
also keeps track of the number of books ordered and the susbtotal
(price * number of books ordered) 
*/
cur.execute(f"INSERT INTO HAVE (ordernumber, bookisbn, numbooksordered, subtotal) VALUES (currval('order_num_seq'), %s, %s, (%s * %s))", (isbn, num_input, match[1], num_input))

/* Updates the quantity of the book, that was ordered, remaining in the store */
cur.execute(f"UPDATE BOOKS SET quantity = (%s - %s) WHERE isbn = %s", (match[0], num_input, isbn))

/* Updates the royalties the publisher earns from their book being purchased */
cur.execute(f"UPDATE PUBLISH SET royalty = (royalty + ((%s * 0.15) * %s) ) WHERE bookisbn = %s", (match[1], num_input, isbn))

/* 
Retrieves the most current order number, so we can provide the user 
their order number for tracking purposes
*/
cur.execute(f"SELECT last_value FROM order_num_seq")

/* 
Retrieves the status of an Order for tracking purposes, so we can use
the last known status to update it when the user inquires about it 
*/
cur.execute(f"SELECT status FROM ORDERS WHERE %s = ordernum AND %s = username", (order_input, user_name))

/* 
Updates the status to the next possible status when the user tracks
their order. For example, if the current status is 'Not Packaged', then 
when the user tracks it it will change to 'Packaged'
*/
cur.execute(f"UPDATE orders SET status = %s WHERE %s = ordernum AND %s = username", (next_status, order_input, user_name))

/* Insert a publisher with all the provided info */
cur.execute(f"INSERT INTO PUBLISHERS (publishername, address, emailadd, phonenum, bankingacc) VALUES (%s, %s, %s, %s, %s)", (name_input, address_input, email_input, phone_input, banking_input))

/* 
Checks if a publisher with the provided bank acc num exists. This is to ensure
that the publisher exists, when the owner adds a book by that publisher
 */
cur.execute(f"SELECT * FROM PUBLISHERS WHERE bankingacc = %s", (publisher_input,))

/* Inserts book with all the provided info */
cur.execute(f"INSERT INTO BOOKS (isbn, bookname, authorname, genre, numofpages, price, quantity, username) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (isbn_input, book_input, author_input, genre_input, num_input, price_input, quantity_input, user_name))

/* 
This represents the relationship between PUBLISHERS and BOOKS. When a book is 
added, this table will also share some of that information to tie in 
a publisher with their book
*/
cur.execute(f"INSERT INTO PUBLISH (pubbankingacc, bookisbn) VALUES (%s, %s)", (publisher_input, isbn_input))

/* 
Deletes book with the provided isbn in the publish relation. When we remove
a book from the store, we delete it from this relation too bc it references 
a books' isbn (publisher publishes non-exisitent book? no, so we delete it)
 */
cur.execute(f"DELETE FROM PUBLISH WHERE bookisbn = %s", (delete_isbn_input,))

/* 
Deletes book with the provided isbn in the have relation. When we remove
a book from the store, we delete it from this relation too bc it references 
a books' isbn (order has non-existent book? no, so we delete it)
 */
cur.execute(f"DELETE FROM HAVE WHERE bookisbn = %s", (delete_isbn_input,))

/* Deletes book with the provided isbn from the store */
cur.execute(f"DELETE FROM BOOKS WHERE isbn = %s", (delete_isbn_input,))

/* 
Joins BOOKS (has the genres of each book) and HAVE (has the total sales for 
each book) to be all to group books by genre and get their sales 
*/
cur.execute(f"SELECT genre, sum(subtotal) AS sales FROM BOOKS JOIN HAVE ON BOOKS.isbn = HAVE.bookisbn GROUP BY genre")

/* Joins BOOKS (has the author of each book) and HAVE (has the total sales for 
each book) to be all to group books by author name and get their sales 
*/
cur.execute(f"SELECT authorname, sum(subtotal) AS sales FROM BOOKS JOIN HAVE ON BOOKS.isbn = HAVE.bookisbn GROUP BY authorname")

/* Joins BOOKS (has each book and its quantity = total amt store spent
and HAVE (has the total sales for all books = total sales) */
cur.execute(f"SELECT sum(subtotal) AS sales, sum(quantity * price) AS expenditures FROM BOOKS JOIN HAVE ON BOOKS.isbn = HAVE.bookisbn")
