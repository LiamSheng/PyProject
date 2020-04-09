"""
Create a scrape_weather.py module with a
WeatherScraper class inside.
"""
import datetime
from html.parser import HTMLParser


class WeatherScraper(HTMLParser):
    """
    Use the Python HTMLParser class to scrape Winnipeg weather data
    (mean temperatures) from the Environment Canada website,
    from the current date, as far back in time as is available.

    WeatherScraper class has been created inside a scrape_weather module.
    Code uses the Python HTMLParser class to parse the website html.
    """

    def __init__(self):
        """
        initialze an instance of WeatherScraper class.
        """
        HTMLParser.__init__(self)
        self.is_in_Tr = self.is_in_Th = self.is_in_Abbr = self.is_in_A = self.is_in_Td = False
        self.is_date = self.is_in_caption = self.is_in_Tbody = False
        self.is_in_mean = self.is_in_min = self.is_in_max = self.is_in_avg = self.is_in_date = False
        self.is_equal = True
        self.i = self.j = 0
        self.keys = ["max", "min", "mean"]
        self.dict_Inner = {}
        self.dict_outer = {}
        self.date = ''
        self.caption_year = ''
        self.caption = []
        self.url_year = self.url_month = None

    def handle_starttag(self, tag, attrs):
        """
        Handle starttags.
        """
        # Set boolean flags when handling each starting tags.
        if tag == 'caption':
            # Only one caption in html
            try:
                self.is_in_caption = True
            except Exception as e:
                print("Error in handling caption tag ", e)
        if tag == 'tbody':
            # Only one <tbody> in html
            try:
                self.is_in_Tbody = True
            except Exception as e:
                print("Error in handling tbody tag ", e)
        if tag == 'tr':
            try:
                self.is_in_Tr = True
            except Exception as e:
                print("Error in handling tr tag ", e)
        if tag == 'td':
            try:
                # column MAX TEMP(#1)
                # column MIN TEMP(#2)
                # column MEAN TEMP(#3)
                self.i += 1
                self.is_in_Td = True
            except Exception as e:
                print("Error in handling td tag ", e)
        if tag == 'th':
            try:
                self.is_in_Th = True
            except Exception as e:
                print("Error in handling th tag ", e)
        if tag == 'abbr':
            # attr[1] holds date information.
            try:
                self.is_in_Abbr = True
            except Exception as e:
                print("Error in handling abbr ", e)
        if tag == 'a':
            try:
                self.is_in_A = True
            except Exception as e:
                print("Error in handling a tag :", e)

        for attr in attrs:
            self.is_in_mean = True
            if self.is_in_Tbody and self.is_in_Tr and self.is_in_Th and self.is_in_Abbr and \
                    attr[0] == 'title' and not attr[0] == 'href' \
                    and not attr[1] == 'Average' and not attr[1] == 'Extreme':
                self.is_in_date = True
                try:
                    self.date = datetime.datetime.strptime(attr[1], '%B %d, %Y').date().strftime('%Y/%m/%d')
                    print(f"Parsing weather data for {self.date}")
                    self.is_date = True
                except Exception as e:
                    print(f"Error in handling date : {attr[1]}", e)

    def handle_endtag(self, tag):
        """
        Handle the endtags.
        """
        # Re-set boolean flags when handling each ending tags.
        if tag == 'caption':
            try:
                self.is_in_caption = False
            except Exception as e:
                print("Error in handling end caption tag :", e)
        if tag == 'tbody':
            try:
                self.is_in_Tbody = False
            except Exception as e:
                print("Error in handling end tbody tag :", e)
        if tag == 'tr':
            try:
                self.i = 0
                self.is_in_Tr = False
            except Exception as e:
                print("Error in handling end tr tag :", e)
        if tag == 'td':
            try:
                self.is_in_Td = False
            except Exception as e:
                print("Error in handling end td tag :", e)
        if tag == 'th':
            try:
                self.is_in_Th = False
            except Exception as e:
                print("Error in handling end th tag :", e)
        if tag == 'abbr':
            try:
                self.is_in_mean = False
                self.is_in_Abbr = False
            except Exception as e:
                print("Error in handling end abbr :", e)
        if tag == 'a':
            # Set all a tag
            try:
                self.is_in_A = False
            except Exception as e:
                print("Error in handling end a tag :", e)

    def handle_data(self, data):
        """
        Handld the data and return dictionary.

        Code successfully scrapes the mean temperature and date,
        and stores them in a data structure.
        One way could be a dictionary of dictionaries. For example:
            • daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}
            • weather = {“2018-06-01”: daily_temps, “2018-06-02”: daily_temps}
        """
        if data == 'Sum':
            self.is_in_date = False
        # Receive "max", "min" and "mean", store these data into dictionary
        if self.is_in_date and self.is_in_Td and self.i == 1:
            try:
                self.dict_Inner[self.keys[0]] = data
            except Exception as e:
                self.dict_Inner[self.keys[0]] = 0
                print("Error in getting Max - Inner:: ", e)
        if self.is_in_date and self.is_in_Td and self.i == 2:
            try:
                self.dict_Inner[self.keys[1]] = data
            except Exception as e:
                self.dict_Inner[self.keys[1]] = 0
                print("Error in getting Min - Inner: ", e)
        if self.is_in_date and self.is_in_Td and self.i == 3:
            try:
                self.dict_Inner[self.keys[2]] = data
            except Exception as e:
                self.dict_Inner[self.keys[2]] = 0
                print("Error in getting Mean - Inner: ", e)
        if self.is_in_date:
            self.dict_outer[self.date] = dict(self.dict_Inner)

        if self.is_in_caption:
            self.caption = data.split()
            self.caption_year = self.caption[5]
            # self.myCaptionMonth = self.caption[4]
            month_dict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                          'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                          'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
            my_month = self.caption[4].strip()[:3].lower()
            if str(self.url_month).zfill(2) == month_dict[my_month] and str(self.url_year) \
                    in self.caption_year:
                self.is_equal = True
            else:
                self.is_equal = False

# Code successfully scrapes weather data from
# the current date, as far back in time as is available.

# Code receives a url to scrape as input,
# and outputs a data structure containing the scraped data.
# try:
#     wather_scraper = WeatherScraper()
#     now = datetime.datetime.now()
#     break_loop = False
#     for i in reversed(range(now.year)):
#         wather_scraper.url_year = i
#         if break_loop:
#             break
#         for j in range(0, 13):
#             wather_scraper.url_month = j
#             with urllib.request.urlopen(passedUrl) as response:
#                 html = str(response.read())
#             wather_scraper.feed(html)
#             if wather_scraper.EqualData is False:
#                 x_loop_must_break = True
#                 break
#     print(f"inner{wather_scraper.dictInner}")
#     print(f"outer{wather_scraper.dictOuter}")
#     myOperations = DBOperations()
#     myOperations.process(wather_scraper.dictOuter)
# except Exception as e:
#     print("Error:", e)
