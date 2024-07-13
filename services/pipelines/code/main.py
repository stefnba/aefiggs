from flows.rates import rates_by_dates
from prefect import serve
from utils import date_list
from datetime import date, timedelta, datetime

def main():

    rates_by_dates_deploy = rates_by_dates.to_deployment(name="Get rates by dates", description="Get historical rates by dates from EOD API and store them in the database.", 
                                                         
                                                         parameters={
            "dates": date_list(start_date=datetime(2024,6,1))
        },
                                                         )
    

    rates_last_day_deploy = rates_by_dates.to_deployment(
        "Rates Last Day",
        description="Scheduled pipeline to get the last day's rates",
        cron="0 5 * * *",
    )

    serve(rates_by_dates_deploy, rates_last_day_deploy)  # type: ignore


if __name__ == "__main__":
    main()
