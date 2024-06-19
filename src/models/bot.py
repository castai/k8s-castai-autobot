import logging
import os
import json

from dotenv import load_dotenv

from constants import FUNCTION_CONFIG_FILE_NAME, FUNCTION_CONFIG_FILE_PATH, TEST_CONFIG_FILE_NAME
from models.bot_execution_config import BotExecutionConfig

from functions.example import example_function
from functions.example import disable_workload_autoscaler


def _load_bot_config(test_run: bool = False):
    config_data = _get_config_data(test_run)
    return BotExecutionConfig(
        cluster_id=os.getenv("CLUSTER_ID"),
        api_key=os.getenv("API_KEY"),
        function_name=config_data['function']['function_name'],
        inputs=config_data['function']['inputs'],
        env_variables=config_data['function']['env_variables']
    )


def _get_config_data(test_run):
    config_file_path = FUNCTION_CONFIG_FILE_PATH
    if test_run:
        config_file_path = ""
        if os.path.exists(TEST_CONFIG_FILE_NAME):
            load_dotenv(dotenv_path=TEST_CONFIG_FILE_NAME)
    config_file_full_path = config_file_path + FUNCTION_CONFIG_FILE_NAME
    try:
        with open(config_file_full_path, 'r') as file:
            config_data = json.load(file)
    except FileNotFoundError as e:
        logging.error(f"Config file not found: {config_file_full_path}")
        raise e
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON in config file: {e}")
        raise e
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise e
    return config_data


class Bot:
    def __init__(self, test_run: bool = False):
        self._logger = logging.getLogger(__name__)
        self._bot_config = _load_bot_config(test_run=test_run)

    def execute_function(self):
        dynamic_function = globals().get(self._bot_config.function_name)
        if dynamic_function:
            dynamic_function(self._bot_config)
        else:
            self._logger.error(f"Error: Function '{self._bot_config.function_name}' not found.")

