import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# ------------------------------------------------

"""
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename="error_log.log",
                    filemode="w",
                    format=LOG_FORMAT,
                    level=logging.ERROR)
"""

# ------------------------------------------------

# """
sql_logger = logging.getLogger('peewee')
sql_logger.addHandler(logging.StreamHandler())
sql_logger.setLevel(logging.DEBUG)
# """