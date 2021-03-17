from datetime import date, timedelta

class Month(date):
    def __new__(cls, year, month, day=None):
        self = date.__new__(cls, year, month, 1)
        return self

    @classmethod
    def this_month(cls):
        today = date.today()
        return cls(today.year, today.month)

    def next(self):
        year = self.year + 1 if self.month+1 > 12 else self.year
        month = self.month%12 + 1
        return Month(year, month)

    def previous(self):
        year = self.year - 1 if self.month-1 < 1 else self.year
        month = 12 - (1-self.month)%12
        return Month(year, month)

    @property
    def dates(self):
        return [
            date(self.year,self.month,i+1) for i in range(0, 31) 
            if (self+timedelta(days=i)).month == self.month
            ]
