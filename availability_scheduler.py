from datetime import datetime, timedelta
import calendar

TODAY = datetime.now()

def month_parser(input):
    """
    :param input: month as number, abbreviation, or full name. lowercase or capitalized
    :return: month as abbreviation
    """
    try:
        input = input.capitalize()
        if input == "Current":
            return TODAY.strftime("%b")
        elif input == "Next":
            next_month = TODAY + timedelta(calendar.monthrange(TODAY.year, TODAY.month)[1])
            return next_month.strftime("%b")
        elif input.isnumeric():
            return(calendar.month_abbr[int(input)])
        elif input in calendar.month_abbr:
            return input
        elif input in calendar.month_name:
            month_numeric = list(calendar.month_name).index(input)
            return calendar.month_abbr[month_numeric]
        else:
            raise Exception("Input does not belong to any defined input modes.")
    except:
        raise Exception("Error when parsing input.")

def availability_calculator(month):
    DAYS_IN_MONTH = {
        "Jan": 31,
        "Feb": 28,
        "Mar": 31,
        "Apr": 30,
        "May": 31,
        "Jun": 30,
        "Jul": 31,
        "Aug": 31,
        "Sep": 30,
        "Oct": 31,
        "Nov": 30,
        "Dec": 31
    }
    TODAY = datetime.now()
    if month == "Current":
        month = TODAY.strftime("%b")
    elif month == "Next":
        print("NEXT")


    output_list = []
    output_string = ""
    for day_index in range(DAYS_IN_MONTH[month]):
        day_number = day_index + 1
        day_output = (f"{month} {day_number} - Available all shifts")
        output_list.append(day_output)
        output_string += f"{day_output}\n"
    return output_list, output_string


def homeprint_adapted(month):
    DAYS_IN_MONTH = {
        "Jan": 31,
        "Feb": 28,
        "Mar": 31,
        "Apr": 30,
        "May": 31,
        "Jun": 30,
        "Jul": 31,
        "Aug": 31,
        "Sept": 30,
        "Oct": 31,
        "Nov": 30,
        "Dec": 31
    }
    TODAY = datetime.now()
    if month == "Current":
        month = TODAY.strftime("%b")
    elif month == "Next":
        print("NEXT")


    output = ""
    for day_index in range(DAYS_IN_MONTH[month]):
        day_number = day_index + 1
        day_output = (f"{month} {day_number} - Available all shifts")
        output += day_output + " \n"
    return output

# month_input = input("Which month would you like?\n").capitalize()
# print(homeprint_adapted(month_input))
