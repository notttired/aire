import logging

logging.basicConfig(
    filename="../logs/app.log",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.DEBUG
)