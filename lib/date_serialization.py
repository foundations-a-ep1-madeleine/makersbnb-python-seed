from datetime import date

def string_to_date(date_string):
    split = date_string.split("-")
    return date(int(split[0]), int(split[1]), int(split[2]))