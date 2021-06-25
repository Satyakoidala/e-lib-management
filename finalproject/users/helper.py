from datetime import datetime, timedelta
from datetime import date

def duedate(current_date):
    due_date = current_date + timedelta(15)
    return due_date
    
def fine(due_date,current_date):
    delta = current_date - due_date
    if delta.days <= 0:
        return 0
    return delta.days*(1.5)

def diff(date1, date2):
    delta = date2 - date1
    return delta.days
    
# if __name__=="__main__":
#     current_date = date.today()
#     due_date=duedate(current_date)
#     print(due_date)
#     print(fine(due_date,current_date))
    