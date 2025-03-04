import logging


def setup_logging(logger, loglevel):
    logger.setLevel(loglevel)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(loglevel)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)