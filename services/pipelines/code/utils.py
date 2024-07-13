from datetime import datetime, timedelta


def date_list(start_date: datetime = datetime(2024, 1, 1), end_date: datetime = datetime.today() - timedelta(days=1)) -> list[str]:
    """
    Generate a list of dates between the start and end dates.
    """
    # Calculate the number of days between start and end dates
    delta = end_date - start_date

    # Initialize an empty list to store dates
    date_list = []

    # Loop through each day between start and end dates
    for i in range(delta.days + 1):
        # Calculate the current date
        current_date = start_date + timedelta(days=i)
        # Format the current date as YYYY-MM-DD and add it to the list
        date_list.append(current_date.strftime('%Y-%m-%d'))

    return date_list
