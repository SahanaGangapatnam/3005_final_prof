/* Create statements for all the tables */

CREATE TABLE USERS (
	userName VARCHAR(10) PRIMARY KEY,
	userPass VARCHAR(10) NOT NULL
);

CREATE TABLE OWNERS (
	userName VARCHAR(10) PRIMARY KEY,
	userPass VARCHAR(10) NOT NULL
);

CREATE TABLE PUBLISHERS (
	publisherName VARCHAR(15) NOT NULL,
	address VARCHAR(40) NOT NULL,
	emailAdd VARCHAR(20) NOT NULL,
	phoneNum CHAR(10) NOT NULL,
	bankingAcc CHAR(15) PRIMARY KEY
);

CREATE TABLE BOOKS (
	ISBN VARCHAR(15) PRIMARY KEY,
	bookName VARCHAR(15) NOT NULL,
	authorName VARCHAR(15) NOT NULL,
	genre VARCHAR(20) NOT NULL, 
	numOfPages SMALLINT NOT NULL, 
	price NUMERIC (5,2) NOT NULL,
	quantity SMALLINT NOT NULL,
	username VARCHAR(10) NOT NULL,
	FOREIGN KEY (username)
		REFERENCES OWNERS (userName)
);

CREATE TABLE PUBLISH (
	pubBankingAcc CHAR(15), 
	bookISBN VARCHAR(15),
	royalty NUMERIC (5,2),
	FOREIGN KEY (pubBankingAcc)
		REFERENCES PUBLISHERS (bankingAcc),
	FOREIGN KEY (bookISBN)
		REFERENCES BOOKS (ISBN),
	PRIMARY KEY (pubBankingAcc, bookISBN)
);

CREATE TABLE ORDERS (
	orderNum INT PRIMARY KEY,
	status VARCHAR(15) NOT NULL,
	billingAddress VARCHAR(40) NOT NULL,
	shippingAddress VARCHAR(40) NOT NULL,
	username VARCHAR(10),
	FOREIGN KEY (username)
		REFERENCES USERS (userName)
);

CREATE TABLE HAVE (
	orderNumber INT,
	bookISBN VARCHAR(15),
	numBooksOrdered INT NOT NULL,
	subtotal NUMERIC(7,2) NOT NULL,
	FOREIGN KEY (orderNumber)
		REFERENCES ORDERS (orderNum),
	FOREIGN KEY (bookISBN)
		REFERENCES BOOKS (ISBN),
	PRIMARY KEY (orderNumber, bookISBN)
);

CREATE SEQUENCE orderNumberSequence;

CREATE FUNCTION check_books() RETURNS trigger AS $checkQuantityBooks$
	BEGIN
		IF NEW.quantity < 5 THEN
			NEW.quantity := 20;
		END IF;
		RETURN NEW;
	END;
$checkQuantityBooks$ LANGUAGE plpgsql;

CREATE TRIGGER checkQuantityBooks BEFORE INSERT OR UPDATE ON BOOKS
	FOR EACH ROW EXECUTE FUNCTION check_books();


