# spl
"""
Database interface
"""

import mariadb
import sys
import os
from config import SQL_USER_ID, SQL_USER_PASSWORD, SQL_HOST, DB_NAME

class DB:
    """
    A Databse Object to handle database connections and query execution.
    ensure config.py has the proper connection info!
    """
    __fileName = os.path.basename(__file__)

    def __init__(self):
        """
        Connects to database on object creation
        """
        self.__connect()


    def __connect(self):
        """
        Initiate a connection to the database
        Should only need to be used internally
        """
        try:
            self.__connection = mariadb.connect(
                user=SQL_USER_ID,
                passwd=SQL_USER_PASSWORD,
                host=SQL_HOST, port=3306,
                db=DB_NAME
            )
            print(f"({self.__fileName}) Database connection established successfully.")
        except mariadb.Error as e:
            print(f"({self.__fileName}) Error (re)connecting to database: {e}")
            exit(f"({self.__fileName}) Exiting the program due to database connection failure. Precaution for more errors later!") # Exit on connection failure


    def __resetConnection(self):
        """
        Closes the current connection and reopens it
        """
        print(f"({self.__fileName}) Attempting to close and reset current connection")
        try:
            self.__connection.close()
            self.__connection = None
            print("(sql.py) Closed current connection")
        except:
            pass # ignore any errors while closing
        self.__connect()


    def execute(self, sql, args=None, verbose=True, tries = 0): # tries should not be used externally
        """
        Executes a SQL query with optional arguments and retry logic.

        Args:
            sql (str): The SQL query to execute.
            args (tuple, optional): The arguments to format the query with. Defaults to None.
            verbose (bool, optional): Whether to print the query being executed. Defaults to False.

        Returns:
            The cursor after executing the query.

        Raises:
            If the query fails after retries.
        """

        if not isinstance(args, tuple):
            args = (args,)

        if self.__connection is None:
            print(f"({self.__fileName}) Error executing current statement, attempting to reset current connection and retry")
            self.__resetConnection();
            return self.execute(sql, args, tries=(tries + 1)) # None is passed as sql has already been formated

        try:
            if verbose:
                print(f"({self.__fileName}) Statement: " + sql)
            cursor = self.__connection.cursor()
            cursor.execute(sql, args)
            self.__connection.commit()
            return cursor

        except:
            if tries == 0:
                print(f"({self.__fileName}) Error executing current statement, attempting to reset current connection and retry")
                self.__resetConnection();
                return self.execute(sql, args, tries=(tries + 1)) # None is passed as sql has already been formated
            else:
                raise

        return cursor


db = DB()