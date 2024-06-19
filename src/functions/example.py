from constants import API_SERVER, CLUSTERS_PREFIX, WORKLOAD_POSTFIX, WORKLOAD_AS_PREFIX
from models.bot_execution_config import BotExecutionConfig
from services.api_requests_svc import cast_api_get, cast_api_put


def example_function(bot_config: BotExecutionConfig) -> None:
    print(f"inputs={bot_config.inputs}")
    print(f"param2={bot_config.env_variables}")


def disable_workload_autoscaler(bot_config: BotExecutionConfig) -> None:
    get_workloads_url = f"{API_SERVER}{WORKLOAD_AS_PREFIX}{bot_config.cluster_id}{WORKLOAD_POSTFIX}"
    get_workloads_result = cast_api_get(get_workloads_url, bot_config.api_key)
    for workload in get_workloads_result["workloads"]:
        if workload["managementOption"] == "MANAGED":
            off_conf = {"managementOption": "READ_ONLY", "recommendationConfig": workload["recommendationConfig"]}
            set_workload_url = \
                f'{API_SERVER}{CLUSTERS_PREFIX}{bot_config.cluster_id}{WORKLOAD_POSTFIX}/{workload["id"]}'
            cast_api_put(set_workload_url, bot_config.api_key, off_conf)
