import datetime
import sqlite3
"""
Create a db_operations.py module with a DBOperations class inside.
"""
# Code successfully uses the Python sqlite3 module
# to store and retrieve weather data.


class DBOperations:
    # Use the Python sqlite3 module to store the weather data in an SQLite
    # database in the specified format. SQL queries to create and query the DB
    # can be provided if required.
    #
    # A class named DBOperations has been created inside a db_operations module.
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
        # Code successfully initializes the database and creates
        # the necessary tables/fields if they don't already exist.
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
            cursor.execute("""CREATE UNIQUE INDEX IF NOT EXISTS index_weather ON Weather (sample_date);""")
            connector.commit()
            print("create_database - Successfully created INDEX index_weather.")
        except Exception as e:
            print("Index index_weather already exists: ", e)
        connector.close()

    def create_table(self, my_dict):
        """
        Create table Weather with received dictionary values.
        Code receives & processes a data structure containing weather data (date, mean temperature)
        as input, checks for duplicates, and successfully stores it in the database.
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
                        if len(my_dict[sample_date]["max"]) == 1:
                            pass
                        else:
                            max_temp = float(my_dict[sample_date]["max"])
                except Exception as e:
                    print("Error in reciving max value: ", e, len(my_dict[sample_date]["max"]))
                """
                Receive min value.
                """
                try:
                    if my_dict[sample_date]["min"] != 'M' and my_dict[sample_date]["min"] != 'E':
                        if len(my_dict[sample_date]["min"]) == 1:
                            min_temp = 0.00
                        else:
                            min_temp = float(my_dict[sample_date]["min"])
                except Exception as e:
                    print("Error in reciving min value: ", e)
                """
                Receive max value.
                """
                try:
                    if my_dict[sample_date]["mean"] != 'M' and my_dict[sample_date]["mean"] != 'E':
                        if len(my_dict[sample_date]["mean"]) == 1:
                            avg_temp = 0.00
                        else:
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
                cursor.execute("""REPLACE INTO Weather
                                (sample_date, location, min_temp, max_temp, avg_temp)
                                VALUES (?,?,?,?,?)""",
                               (sample_date, location, min_temp, max_temp, avg_temp))
                connector.commit()
                connector.close()
            except Exception as e:
                print("Error in replacing data", e)

    def query_infos(self, from_year, to_year):
        # In addition to the above box plot, display a line plot of a particular months mean
        # temperature data, based on user input. For example, display all the mean
        # temperatures from January, with the x axis being the day, and the y axis being
        # temperature.
        # ------------
        # Code outputs the data required to accomplish the tasks in Part 3 of the project.
        connector = sqlite3.connect("weather.sqlite")
        cursor = connector.cursor()
        to_year = int(to_year) + 1
        mydict_output = {}
        for row in cursor.execute("SELECT * FROM Weather WHERE \
                                sample_date BETWEEN ? AND ?",
                                  (str(from_year) + '%', str(to_year) + '%')):
            # print(f"row {row}")
            my_month = datetime.datetime.strptime(row[1], '%Y/%m/%d').month
            mydict_output.setdefault(my_month, []).append(row[5])
        # print(mydict_output)
        return mydict_output
        connector.commit()
        connector.close()
