/* insert into statements for all the tables */

INSERT INTO USERS(userName, userPass)
VALUES
	('user1', 'abc'),
	('user2', '123');
	
INSERT INTO OWNERS(userName, userPass)
VALUES
	('owner1', 'abc'),
	('owner2', '123');

INSERT INTO BOOKS(isbn, bookname, authorname, genre, numofpages, price, quantity, username)
VALUES
	('123', 'Book3', 'Author1', 'Romance', 40, 21.99, 20, 'owner1'),
	('184692740193719', 'Book1', 'Author1', 'Mystery', 20, 19.99, 5, 'owner1');

INSERT INTO PUBLISHERS(publishername, address, emailadd, phonenum, bankingacc)
VALUES
	('publisher1', '34 Harlem St. L3K2J3', 'pub1@gmail.com', '1234567891', '777777777777777'),
	('publisher2', '31 Holiday St. L3M2A1', 'pub2@gmail.com', '1112223333', '666666666666666');

INSERT INTO ORDERS(ordernum, status, billingaddress, shippingaddress, username)
VALUES 
	(4, 'Not Delivered', '23 Yale Lane L6B1H2', '30 Yale Lane L6B1H9', 'user1'),
	(5, 'Not Delivered', '23 Yale Lane L6B1H2', '30 Yale Lane L6B1H9', 'user1'),
	(11, 'Not Delivered', '2 Abc Rd L6J1H2', '2 Abc Rd L6J1H2', 'user1');

INSERT INTO HAVE (ordernumber, bookisbn, numbooksordered, subtotal) 
VALUES 
	(4, '123', 3, 65.97), 
	(5, '184692740193719', 2, 39.98), 
	(11, '123', 2, 43.98);

INSERT INTO PUBLISH (pubBankingAcc, bookisbn, royalty)
VALUES
	('666666666666666', '123', 23.09),
	('777777777777777', '184692740193719', 14.99);