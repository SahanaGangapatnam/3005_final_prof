/*
This triggers the check_books function when a book is added or updated 
from the BOOKS table
*/

CREATE TRIGGER checkQuantityBooks BEFORE INSERT OR UPDATE ON BOOKS
	FOR EACH ROW EXECUTE FUNCTION check_books();