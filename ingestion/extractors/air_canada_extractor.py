from models.scrape_task import ScrapeRequest
from ingestion.extractors.base_extractor import BaseExtractor
from models.flight import *
from models.scrape_task import ScrapeRequest
from typing import List
from bs4 import BeautifulSoup
from datetime import datetime
from ingestion.constants.air_canada import *

class AirCanadaExtractor(BaseExtractor):

    def extract_flight_price(self, request: ScrapeRequest, html_content: str) -> List[FlightPrice]:
        return self.extract_flight_price_one_way(request, html_content)

    def extract_flight_price_one_way(self, request: ScrapeRequest, html_content: str) -> List[FlightPrice]:
        soup = BeautifulSoup(html_content, 'lxml')

        flight_rows = soup.find_all(id=FLIGHT_ROW_ID_REGEX)
        prices: List[FlightPrice] = []

        for flight_row in flight_rows:
            depart_time = flight_row.select(DEPART_TIME_SELECTOR)[0].get_text(strip=True)
            arrive_time = flight_row.select(ARRIVAL_TIME_SELECTOR)[0].get_text(strip=True)
            price = flight_row.select(PRICE_SELECTOR)[0].get_text(strip=True)
            stripped_price = int("".join(c for c in price if c.isdigit()))

            parsed_depart = datetime.strptime(depart_time, "%H:%M").time()
            parsed_arrive = datetime.strptime(arrive_time, "%H:%M").time()
            prices.append(
                FlightPrice(
                    flight=Flight(
                        route=request.route,
                        date_range=DateRange(
                            start=datetime(
                                request.outbound.year,
                                request.outbound.month,
                                request.outbound.day,
                                parsed_depart.hour,
                                parsed_depart.minute,
                            ),
                            end=datetime(
                                request.outbound.year,
                                request.outbound.month,
                                request.outbound.day,
                                parsed_arrive.hour,
                                parsed_arrive.minute,
                            ),
                        ),
                    ),
                    price=stripped_price,
                )
            )

        return prices