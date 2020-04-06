"""
Create a scrape_weather.py module with a 
WeatherScraper class inside.
"""
import datetime
import urllib.request
from html.parser import HTMLParser
from db_operations import DBOperations


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
        self.keys = ["max", "min", "mean"]
        self.EqualData = True
        self.i = self.j = 0
        self.dictInner = self.dictOuter = {}
        self.myDate = self.myCaptionYear = self.myCaptionMonth = ''
        self.myCaption = []
        self.url_year = self.url_month = None
        self.isInTrTag = self.isInThTag = self.isInAbbr = self.isInATag = False
        self.inMean = self.inMin = self.inMax = self.inAvg = self.inMyDate = False
        self.isInTdTag = self.isDate = self.isInCaption = self.isInTbody = False

    def handle_starttag(self, tag, attrs):
        """
        Handle starttags.
        """
        for attr in attrs:
            self.inMean = True
            if self.isInTbody and self.isInTrTag and self.isInThTag and self.isInAbbr and \
                    attr[0] == 'title' and not attr[0] == 'href' \
                    and not attr[1] == 'Average' and not attr[1] == 'Extreme':
                self.inMyDate = True
                try:
                    self.myDate = datetime.datetime.strptime(attr[1], '%B %d, %Y').date().strftime('%Y/%m/%d')
                    print(f"self.myDate {self.myDate}")
                    self.isDate = True
                except Exception as e:
                    print(f"Error in handling date : {attr[1]}", e)

        """
        Set boolean flags when handling each starting tags.
        """
        if tag == 'caption':
            try:
                self.isInCaption = True
            except Exception as e:
                print("Error in handling caption tag ", e)

        if tag == 'tbody':
            try:
                self.isInTbody = True
            except Exception as e:
                print("Error in handling tbody tag ", e)

        if tag == 'tr':
            try:
                self.isInTrTag = True
            except Exception as e:
                print("Error in handling tr tag ", e)

        if tag == 'th':
            try:
                self.isInThTag = True
            except Exception as e:
                print("Error in handling th tag ", e)

        if tag == 'abbr':
            """
            attr[1] holds date information.
            """
            try:
                self.isInAbbr = True
            except Exception as e:
                print("Error in handling abbr ", e)

        if tag == 'a':
            try:
                self.isInATag = True
            except Exception as e:
                print("Error in handling a tag :", e)

        if tag == 'td':
            try:
                """
                column MAX TEMP(#1)
                column MIN TEMP(#2)
                column MEAN TEMP(#3)
                """
                self.i += 1
                self.isInTdTag = True
            except Exception as e:
                print("Error in handling td tag ", e)

    def handle_endtag(self, tag):
        """
        Handle the endtags.
        """
        """
        Re-set boolean flags when handling each ending tags. 
        """
        if tag == 'caption':
            try:
                self.isInCaption = False
            except Exception as e:
                print("Error in handling end caption tag :", e)

        if tag == 'tbody':
            try:
                self.isInTbody = False
            except Exception as e:
                print("Error in handling end tbody tag :", e)

        if tag == 'tr':
            try:
                self.i = 0
                self.isInTrTag = False
            except Exception as e:
                print("Error in handling end tr tag :", e)

        if tag == 'td':
            try:
                self.isInTdTag = False
            except Exception as e:
                print("Error in handling end td tag :", e)

        if tag == 'th':
            try:
                self.isInThTag = False
            except Exception as e:
                print("Error in handling end th tag :", e)

        if tag == 'abbr':
            try:
                self.inMean = False
                self.isInAbbr = False
            except Exception as e:
                print("Error in handling end abbr :", e)

        if tag == 'a':
            try:
                self.isInATag = False
            except Exception as e:
                print("Error in handling end a tag :", e)

    def handle_data(self, data):
        """
        Handld the data and return dictionary.

        Code successfully scrapes the mean temperature and date,
        and stores them in a data structure.
        """
        """
        One way could be a dictionary of dictionaries. For example:
            • daily_temps = {“Max”: 12.0, “Min”: 5.6, “Mean”: 7.1}
            • weather = {“2018-06-01”: daily_temps, “2018-06-02”: daily_temps}
        """
        if self.isInCaption:
            self.myCaption = data.split()
            self.myCaptionYear = self.myCaption[5]
            """Year"""
            self.myCaptionMonth = self.myCaption[4]
            """Month"""
            dict_month = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                          'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                          'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
            s = self.myCaption[4].strip()[:3].lower()
            if str(self.url_month).zfill(2) == dict_month[s] and str(self.url_year) \
                    in self.myCaptionYear:
                self.EqualData = True
            else:
                self.EqualData = False

        if data == 'Sum':
            self.inMyDate = False

        """
        Receive "max", "min" and "mean", store these data into dictionary
        """
        if self.inMyDate and self.isInTdTag and self.i == 1:
            try:
                self.dictInner[self.keys[0]] = data
            except Exception as e:
                self.dictInner[self.keys[0]] = 0
                print("Error in getting Max - Inner:: ", e)

        if self.inMyDate and self.isInTdTag and self.i == 2:
            try:
                self.dictInner[self.keys[1]] = data
            except Exception as e:
                self.dictInner[self.keys[1]] = 0
                print("Error in getting Min - Inner: ", e)

        if self.inMyDate and self.isInTdTag and self.i == 3:
            try:
                self.dictInner[self.keys[2]] = data
            except Exception as e:
                self.dictInner[self.keys[2]] = 0
                print("Error in getting Mean - Inner: ", e)

        if self.inMyDate:
            self.dictOuter[self.myDate] = dict(self.dictInner)


# Code successfully scrapes weather data from
# the current date, as far back in time as is available.

# Code receives a url to scrape as input,
# and outputs a data structure containing the scraped data.
try:
    wather_scraper = WeatherScraper()
    now = datetime.datetime.now()
    break_loop = False
    for i in reversed(range(now.year)):
        wather_scraper.url_year = i
        if break_loop:
            break
        for j in range(0, 13):
            wather_scraper.url_month = j
            passedUrl = f"https://climate.weather.gc.ca/climate_data/daily_data_e.html?%20StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=%201&Year={wather_scraper.url_year}&Month={wather_scraper.url_month}#"
            with urllib.request.urlopen(passedUrl) as response:
                html = str(response.read())
            wather_scraper.feed(html)
            if wather_scraper.EqualData is False:
                x_loop_must_break = True
                break
    print(f"inner{wather_scraper.dictInner}")
    print(f"outer{wather_scraper.dictOuter}")
    myOperations = DBOperations()
    myOperations.process(wather_scraper.dictOuter)
except Exception as e:
    print("Error:", e)
