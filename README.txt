Please execute the code in the following order:
Python Scripts Cleanup
	Types of XML Tags.py
	Types of 'Tags'.py
	Number of Unique Users.py
	Editing Street Names.py
	Full ETL to JSON.py

The code will run through: 
	Number of nodes and ways.
	Number of different 'tags' (different from XML tags) and separable categories.
	Number of unique users.
	Different street names and edits to those names for standardization / uniformity.

Python Scripts Queries
	Total Entries.py
	Total Unique Users.py
	Total Nodes.py
	Total Ways.py
	Total Amenities.py
	Top 4 Parking Structures.py
	Top 5 School Types.py
	Top 5 Restaurants.py

The code will pull the queries in the PDF in order.

Be sure to run Mongod in Windows to grab the correct database and use the shell command - mongoimport 
--host=127.0.0.1 --db mongData --collection OSMLagny --drop --file LocationOfJSONFile

See pdf and comments for more in depth description of what code does.