from sql import db
import sys
import os

def remove_comments(statement): # Remove comments that start with '--' (single-line comments).
    lines = statement.splitlines() # Split the statement into lines
    lines_without_comments = []
    
    for line in lines:
        # Check if the line contains a comment (anything after '--')
        comment_start = line.find("--")
        if comment_start != -1:
            line = line[:comment_start].strip() # Remove the comment part
        lines_without_comments.append(line)

    return " ".join(lines_without_comments).strip() # Rebuild the statement and remove extra whitespace

def setup_database():
    print("Executing Database Setup (dbsetup.sql). This will parse the file and execute any command seperated by a ; one by one")
    try:
        # Read the SQL file
        with open("./dbsetup.sql", mode='r', encoding='utf-8') as file:
            sql_file = file.read()

        # Split the SQL file into individual statements
        sql_statements = sql_file.split(";")

        # Execute each SQL statement
        for statement in sql_statements:
            statement = remove_comments(statement) # Remove comments starting with --
            statement = statement.strip() # Clean up whitespace
            if statement: # Ignore empty statements
                db.execute(statement, verbose=True)

    except Exception as err:
        print(f"Setup failed! {err}")
        sys.exit("Exiting the program due to setup failure.") # Exit on setup failure
    else:
        print("Database Setup Success")

setup_database()