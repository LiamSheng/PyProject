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
            dict_month = {'January': '01', 'February': '02', 'March': '03',
                          'April': '04', 'May': '05', 'June': '06',
                          'July': '07', 'August': '08', 'September': '09',
                          'October': '10', 'November': '11', 'December': '12'}
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

# w = WeatherScraper()
