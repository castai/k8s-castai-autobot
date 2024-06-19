import os
import logging
from typing import List, Optional, Dict


class BotExecutionConfig:
    def __init__(self, cluster_id: str, api_key: str, function_name: str, inputs: List[Dict],
                 env_variables: List[Dict]):

        self._logger = logging.getLogger(__name__)

        self.cluster_id = cluster_id
        self.api_key = api_key
        self.function_name = function_name
        self.inputs = inputs
        self.env_variables = env_variables
        for env_var in env_variables:
            os.environ[env_var["name"]] = str(env_var["value"])

        self._logger.debug(str(self))

    def __str__(self):
        return (f"BotExecutionConfig("
                f"cluster_id={self.cluster_id}, "
                f"api_key={self.api_key}, "
                f"function_name={self.function_name}, "
                f"inputs={self.inputs}, "
                f"env_variables={self.env_variables})")
