import re
import datetime

class Date:
    def __init__(self, month, day, year):
        self.month = int(month)
        self.day = int(day)
        self.year = int(year)
    
    def date2String(self):
        if self.day < 10:
            day = '0{}'.format(self.day)
        else:
            day = '{}'.format(self.day)
        if self.month < 10:
            month = '0{}'.format(self.month)
        else:
            month = '{}'.format(self.month)
        if self.year < 10:
            year = '0{}'.format(self.year)
        else:
            year = '{}'.format(self.year)
        date = '{}/{}/{}'.format(month, day, year)
        return date

class Date_finder:
    def __init__(self):
        #Expresiones regulares para búsqueda de fechas#
        self.DATE_RE_1 = re.compile('\d{1,2}[/-]\d{1,2}[/-]\d{2,4}')
        self.DATE_RE_2 = re.compile('\d{1,2} (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[,.]{0,1} \d{2,4}')
        self.DATE_RE_3 = re.compile('\d{1,2} (?:january|february|march|april|may|june|july|august|september|october|november|december)[,.]{0,1} \d{2,4}')
        self.DATE_RE_4 = re.compile('(?:january|february|march|april|may|june|july|august|september|october|november|december) \d{1,2}[,.]{0,1} \d{2,4}')
        self.DATE_RE_5 = re.compile('(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec) \d{1,2}[,.]{0,1} \d{2,4}')
        self.DATE_RE_6 = re.compile('(?:january|february|march|april|may|june|july|august|september|october|november|december) \d{2,4}')
        self.DATE_RE_7 = re.compile('\d{1,2}[/-]\d{4}')
        self.DATE_RE_8 = re.compile('\d{4}')

        # Diccionarios #
        self.MONTH_DIC = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6,
                          'jul':7, 'aug':8, 'sep':9, 'oct':10, 'nov':11, 'dec':12,
                          'january':1, 'february':2, 'march':3, 'april':4, 'may':5, 'june':6,
                          'july':7, 'august':8, 'september':9, 'october':10, 'november':11, 'december':12}

    
    def normalize_year(self, year):
        if len(year) == 4:
            year = year[2:]
        return int(year)
    
    def normalize_month(self, month):
        m = self.MONTH_DIC[month]
        return int(m)
    
    def normalize_day(self, day):
        index = len(day) - 1
        if day[index] == ',' or day[index] == '.':
            day = day[:index]
        return int(day)

    def normalize_date(self, date, regex):
        if regex == 1:
            d = date[0].split('/')
            if len(d)==1:
                d = date[0].split('-')
            year = self.normalize_year(d[2])
            normalized_date = Date(d[0],d[1],year)
        
        if regex == 2:
            d = date[0].split(' ')
            month = self.normalize_month(d[1])
            year = self.normalize_year(d[2])
            normalized_date = Date(month, d[0], year)
        
        if regex == 3:
            d = date[0].split(' ')
            month = self.normalize_month(d[1])
            year = self.normalize_year(d[2])
            normalized_date = Date(month, d[0], year)
        
        if regex == 4:
            d = date[0].split(' ')
            month = self.normalize_month(d[0])
            day = self.normalize_day(d[1])
            year = self.normalize_year(d[2])
            normalized_date = Date(month, day, year)
        
        if regex == 5:
            d = date[0].split(' ')
            month = self.normalize_month(d[0])
            day = self.normalize_day(d[1])
            year = self.normalize_year(d[2])
            normalized_date = Date(month, day, year)
        
        if regex == 6:
            d = date[0].split(' ')
            month = self.normalize_month(d[0])
            year = self.normalize_year(d[1])
            day = 1
            normalized_date = Date(month,day,year)
        
        if regex == 7:
            d = date[0].split('/')
            if len(d) == 1:
                d = date[0].split('-')
            day = 1
            year = self.normalize_year(d[1])
            normalized_date = Date(d[0],1, year)
        
        if regex == 8:
            year = self.normalize_year(date[0])
            normalized_date = Date(1,1,year)
        
        return normalized_date
            
            
    
    def find_date(self, text):
        text = text.lower()
        date = self.DATE_RE_1.findall(text)
        regex = 1
        if len(date) == 0:
            date = self.DATE_RE_2.findall(text)
            regex = 2
            if len(date)==0:
                date = self.DATE_RE_3.findall(text)
                regex = 3
                if len(date) == 0:
                    date = self.DATE_RE_4.findall(text)
                    regex = 4
                    if len(date) == 0:
                        date = self.DATE_RE_5.findall(text)
                        regex = 5
                        if len(date) == 0:
                            date = self.DATE_RE_6.findall(text)
                            regex = 6
                            if len(date) == 0:
                                date = self.DATE_RE_7.findall(text)
                                regex = 7
                                if len(date) == 0:
                                    date = self.DATE_RE_8.findall(text)
                                    regex = 8
        
        d = self.normalize_date(date,regex)                 
        return d



dates_file = open('dates.txt', 'r').read().split('\n')

finder = Date_finder()

dates = []
for line in dates_file:
    date = finder.find_date(line)
    dates.append(date)

# Converir fechas normalizadas a texto #
text_dates = []
for date in dates:
    text_dates.append(date.date2String())

for d in text_dates:
    print(d)

# Ordenamiento de las fechas #
dates = [datetime.datetime.strptime(d, "%m/%d/%y") for d in text_dates]
dates.sort()
sorted_dates = [datetime.datetime.strftime(d,  "%m/%d/%y") for d in dates]
print(sorted_dates)


