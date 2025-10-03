from ingestion.scrapers.air_canada_scraper import AirCanadaScraper
from ingestion.extractors.air_canada_extractor import AirCanadaExtractor

AIRLINES = {
    "AC": {
        "scraper": AirCanadaScraper,
        "extractor": AirCanadaExtractor,
    },
}
