"""
Module: Creates a WeatherProcessor class to prompt user interaction.
"""
import urllib.request
import datetime
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations


class WeatherProcessor:
    """This class is for user interaction."""

    def main(self):
        """
        When the program starts, prompt the user to download a full set of
        weather data, or to update it (optional).
        • Then prompt the user for a year range of interest (from year, to year).
        • Use this class to launch and manage all the other tasks.
        """
        user_selection = ''
        while user_selection != '4':
            try:
                print("1. Update a set of weather data up to today")
                print("2. Download a full set of weather data")
                print("3. A year range of interest (from year, to year)")
                print("4. Exit")
                user_selection = input("Please make your choice...")
                if user_selection == '1':
                    try:
                        my_scraper = WeatherScraper()
                        now_date = datetime.datetime.now()
                        is_loop = False
                        for i in range(now_date.year, now_date.year-1, -1):
                            my_scraper.url_year = i
                            if is_loop:
                                break
                            for j in range(now_date.month - 2, now_date.month + 1):
                                my_scraper.url_month = j
                                my_url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={my_scraper.url_year}&Month={my_scraper.url_month}#"
                                with urllib.request.urlopen(my_url) as response:
                                    html = str(response.read())
                                my_scraper.feed(html)
                                if my_scraper.is_equal is False:
                                    is_loop = True
                                    break
                        # print(f"inner{my_scraper.dict_Inner}")
                        # print(f"outer{my_scraper.dict_outer}")
                        my_database = DBOperations()
                        my_database.create_table(my_scraper.dict_outer)
                    except Exception as e:
                        print("Error in Updating a set of weather data up to today: ", e)
                elif user_selection == '2':
                    try:
                        my_scraper = WeatherScraper()
                        now_date = datetime.datetime.now()
                        is_loop = False
                        for i in reversed(range(now_date.year)):
                            my_scraper.url_year = i
                            if is_loop:
                                break
                            for j in range(0, 13):
                                my_scraper.url_month = j
                                my_url = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={my_scraper.url_year}&Month={my_scraper.url_month}#"
                                with urllib.request.urlopen(my_url) as response:
                                    html = str(response.read())
                                my_scraper.feed(html)
                                if my_scraper.is_equal is False:
                                    is_loop = True
                                    break
                        # print(f"inner{my_scraper.dict_Inner}")
                        # print(f"outer{my_scraper.dict_outer}")
                        my_database = DBOperations()
                        my_database.create_table(my_scraper.dict_outer)
                    except Exception as e:
                        print("Error in downloading a full set of weather data: ", e)
                elif user_selection == '3':
                    try:
                        range_value = input("Please select a RANGE of your interest(e.g 2017 2019): ")
                        range_value = range_value.split()
                        my_database = DBOperations()
                        dict_value = my_database.query_infos(range_value[0], range_value[1])
                        my_plot_operation = PlotOperations()
                        my_plot_operation.diplay_box_plot(dict_value, range_value[0], range_value[1])
                    except Exception as e:
                        print("Error in A year range of interest (from year, to year): ", e)
                elif user_selection == '4':
                    break
                else:
                    print("Invalid choice")
            except Exception as e:
                print("Error plot_operations.py: ", e)


def weather_app():
    """
    Create instance of WeatherProcessor
    """
    my_weather_processor = WeatherProcessor()
    my_weather_processor.main()


if __name__ == '__main__':
    weather_app()
