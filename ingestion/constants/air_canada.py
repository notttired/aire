import re

# Scraper
DEFAULT_TIMEOUT_MS = 60000

BASE_URL = "https://www.aircanada.com/home/ca/en/aco/flights"

DEPARTURE_LOCATION_SELECTOR = "#flightsOriginLocationbkmgLocationContainer"
DEPARTURE_FORM_SELECTOR = "#flightsOriginLocation"
ARRIVAL_LOCATION_SELECTOR = "#flightsOriginDestinationbkmgLocationContainer"
ARRIVAL_FORM_SELECTOR = "#flightsOriginDestination"
SEARCH_RESULT_SELECTOR_0 = "#flightsOriginDestinationSearchResult0"

TRIP_TYPE_SELECTOR = "#bkmgFlights-trip-selector_tripTypeBtn"
ROUND_TRIP_SELECTOR = "#bkmgFlights-trip-selector_tripTypeSelector_R"
ONE_WAY_TRIP_SELECTOR = "#bkmgFlights-trip-selector_tripTypeSelector_O"

# One Way
DATE_SELECTOR = "#bkmg-desktop_travelDates"

# Round Trip
DEPARTURE_DATE_SELECTOR = "#bkmg-desktop_travelDates-formfield-1"
RETURN_DATE_SELECTOR = "#bkmg-desktop_travelDates-formfield-2"
NEXT_MONTH_SELECTOR = "#bkmg-desktop_travelDates_nextMonth"
PREVIOUS_MONTH_SELECTOR = "#bkmg-desktop_travelDates_previousMonth"
CONFIRM_DATES_SELECTOR = "#bkmg-desktop_travelDates_1_confirmDates"

SEARCH_BUTTON_SELECTOR = "#bkmg-desktop_findButton"

NOT_FOUND_URL = "https://www.aircanada.com/booking/ca/en/aco/no-flights-found"
FOUND_URL = "https://www.aircanada.com/booking/ca/en/aco/availability/rt/outbound"
ONE_WAY_FOUND_URL = "https://www.aircanada.com/booking/ca/en/aco/availability/ow/outbound"

# Extractor
DEPART_TIME_SELECTOR = 'div[bound-departure] div[bound-information] span[bound-location]'
ARRIVAL_TIME_SELECTOR = 'div[bound-arrival] div[bound-information] span[bound-location]'
PRICE_SELECTOR = 'span[cabin-price] span'
DEPART_TIME_SELECTOR = 'div.bound-departure div.bound-information span.bound-time'
ARRIVAL_TIME_SELECTOR = 'div.bound-arrival div.bound-information span.bound-time'
PRICE_SELECTOR = 'span.cabin-price span'


FLIGHT_ROW_SELECTOR = '[id^="flight-row"]'
FLIGHT_ROW_ID_REGEX = re.compile(r"^flight-row")