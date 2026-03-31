import logging
from logging.handlers import RotatingFileHandler



def crea_log():


    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)


    rotating_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=5)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    rotating_handler.setFormatter(formatter)

    logger.addHandler(rotating_handler)

    return logger