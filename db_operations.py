"""
Create a db_operations.py module with a DBOperations class inside.
"""
import sqlite3


class DBOperations:
    """
    Use the Python sqlite3 module to store the weather data in an SQLite
    database in the specified format. SQL queries to create and query the DB
    can be provided if required.
    """

    def create_database(self):
        """
        Initialise the database and create tables.
        """
        try:
            connector = sqlite3.connect("weather.sqlite")
            cursor = connector.cursor()
            print("The database has been successfully initialised...")
        except Exception as e:
            print("Error initialising database: ", e)

        # The DB format for your reference:
        #     ◦ id -> integer, primary key, autoincrement
        #     ◦ sample_date -> text
        #     ◦ location -> text
        #     ◦ min_temp -> real
        #     ◦ max_temp -> real
        #     ◦ avg_temp -> real
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS Weather
                            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                             sample_date text NOT NULL,
                             location text NOT NULL,
                             min_temp REAL NOT NULL,
                             max_temp REAL NOT NULL,
                             avg_temp REAL NOT NULL);""")
            print("Table has been successfully created...")
        except Exception as e:
            print("Error in creating table: ", e)

        try:
            cursor.execute("""CREATE UNIQUE INDEX index_weather ON Weather (sample_date);""")
            connector.commit()
            print("create_database - Successfully created INDEX index_weather.")
        except Exception as e:
            print("Index index_weather already exists: ", e)
        connector.close()

    def create_table(self, my_dict):
        """
        Create table Weather with received dictionary values.
        """
        self.create_database()
        my_location = "Winnipeg"

        for dict_key in my_dict.keys():
            try:
                sample_date = dict_key
            except Exception as e:
                print("Error in reciving data from dictionary: ", e)
            for dict_value in my_dict.values():
                """
                Receive max value.
                """
                try:
                    if my_dict[sample_date]["max"] != 'M' and my_dict[sample_date]["max"] != 'E':
                        max_temp = float(my_dict[sample_date]["max"])
                except Exception as e:
                    print("Error in reciving max value: ", e)
                """
                Receive min value.
                """
                try:
                    if my_dict[sample_date]["min"] != 'M' and my_dict[sample_date]["min"] != 'E':
                        min_temp = float(my_dict[sample_date]["min"])
                except Exception as e:
                    print("Error in reciving min value: ", e)
                """
                Receive max value.
                """
                try:
                    if my_dict[sample_date]["mean"] != 'M' and my_dict[sample_date]["mean"] != 'E':
                        avg_temp = float(my_dict[sample_date]["mean"])
                except Exception as e:
                    print("Error in reciving mean value: ", e)
                """
                Receive location value.
                """
                try:
                    location = my_location
                except Exception as e:
                    print("Error in receiving location value: ", e)

            try:
                connector = sqlite3.connect("weather.sqlite")
                cursor = connector.cursor()
                cursor.execute("""REPLACE INTO weather
                                (sample_date, location, min_temp, max_temp, avg_temp)
                                VALUES (?,?,?,?,?)""",
                               (sample_date, location, min_temp, max_temp, avg_temp))
                connector.commit()
                connector.close()
            except Exception as e:
                print("Error:", e)


db = DBOperations()
db.create_database()
