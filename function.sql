/* 
This function automatically updates a book's quantity when it's inserted 
or being updated (bought). If the quantity is less than 5, it will change
the value to 20
*/

CREATE FUNCTION check_books() RETURNS trigger AS $checkQuantityBooks$
	BEGIN
		IF NEW.quantity < 5 THEN
			NEW.quantity := 20;
		END IF;
		RETURN NEW;
	END;
$checkQuantityBooks$ LANGUAGE plpgsql;
