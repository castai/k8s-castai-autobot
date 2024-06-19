from models.bot import Bot

import logging
import os

log_level = os.environ.get("LOG_LEVEL", "critical").upper()
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(name)s - %(message)s', level=log_level)

TEST_RUN = False

if __name__ == "__main__":
    bot = Bot(test_run=TEST_RUN)
    bot.execute_function()
