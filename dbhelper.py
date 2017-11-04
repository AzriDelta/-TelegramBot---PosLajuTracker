import sqlite3


class DBHelper:
	#to add the owner column when a new database is set up
	def setup(self):
		tblstmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text)"
		itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description ASC)" 
		ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner ASC)"
		self.conn.execute(tblstmt)
		self.conn.execute(itemidx)
		self.conn.execute(ownidx)
		self.conn.commit()

	#accept the chat_id (which we're using to identify owners) as an additional argument, and to add this to the database along with the item
	def add_item(self, item_text, owner):
		stmt = "INSERT INTO items (description, owner) VALUES (?, ?)"
		args = (item_text, owner)
		self.conn.execute(stmt, args)
		self.conn.commit()
	
	#only deletes items that match and that belong to the indicated owner
	def delete_item(self, item_text, owner):
		stmt = "DELETE FROM items WHERE description = (?) AND owner = (?)"
		args = (item_text, owner )
		self.conn.execute(stmt, args)
		self.conn.commit()
	
	#nly return the items that belong to the specified owner
	def get_items(self, owner):
		stmt = "SELECT description FROM items WHERE owner = (?)"
		args = (owner, )
		return [x[0] for x in self.conn.execute(stmt, args)]