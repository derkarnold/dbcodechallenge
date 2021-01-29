# March 13th 1**4, on a leap year is "The third youngest".
# Hint is "the youngest"...
# https://challenge.dreambroker.jobs/af776836-ae78-45b6-be76-079b557460ed
import datetime as dt

_IDX_OF_TUESDAY = 1
_TODAY = dt.date.today()

startingYear = 2000
for year in range(1004, 2004, 10):
    if year % 4 != 0:
        continue
    birthDate = dt.date(year, 3, 13)
    if birthDate.weekday() != _IDX_OF_TUESDAY:
        continue
    print(year)
    