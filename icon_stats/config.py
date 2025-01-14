import os

from dotenv import dotenv_values
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from icon_stats.clients.configs import CmcClientConfig
from icon_stats.db_config import DbConfigs


class Settings(BaseSettings):
    # General
    NAME: str = "stats"
    VERSION: str = "v0.3.0"  # x-release-please-version
    NETWORK_NAME: str = "mainnet"

    # Exchanges
    cmc: CmcClientConfig = Field(default_factory=CmcClientConfig)

    # Enablers - Allows you to disable part of the service
    ENABLE_API: bool = True
    ENABLE_CRON: bool = True
    ENABLE_STREAMING: bool = True

    # API
    API_PORT: int = 8000
    API_REST_PREFIX: str = "/api/v1"
    API_DOCS_PREFIX: str = "/api/v1/statistics/docs"
    API_MAX_PAGE_SIZE: int = 100

    CORS_ALLOW_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False
    CORS_ALLOW_METHODS: str = "GET,POST,HEAD,OPTIONS"
    CORS_ALLOW_HEADERS: str = ""
    CORS_EXPOSE_HEADERS: str = "x-total-count"

    # Cron
    CRON_SLEEP_SEC: int = 600

    # Monitoring
    METRICS_PORT: int = 9400
    METRICS_ADDRESS: str = "localhost"
    METRICS_PREFIX: str = "/metrics"

    # Health
    HEALTH_PORT: int = 8180
    HEALTH_PREFIX: str = "/heath"
    HEALTH_POLLING_INTERVAL: int = 60

    # Endpoints
    ICON_NODE_URL: str = "https://api.icon.community/api/v3"
    COMMUNITY_API_ENDPOINT: str = "https://tracker.icon.community"
    LISBON_COMMUNITY_API_ENDPOINT: str = "https://lisbon.tracker.icon.community"
    BERLIN_COMMUNITY_API_ENDPOINT: str = "https://berlin.tracker.icon.community"

    # DB
    db: DbConfigs = Field(default_factory=DbConfigs)

    # Kafka
    KAFKA_BROKER_URL: str = "localhost:29092"
    CONSUMER_IS_TAIL: bool = False
    CONSUMER_GROUP: str = "stats"
    CONSUMER_TOPIC_BLOCKS: str = "blocks"
    CONSUMER_AUTO_OFFSET_RESET: str = "earliest"
    JOB_ID: str | None = None

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = False
    LOG_FILE_NAME: str = "stats.log"
    LOG_FORMAT: str = "string"  # or "json"
    LOG_INDENT: int = 4
    LOG_INCLUDE_FIELDS: list[str] = ["timestamp", "message"]
    LOG_EXCLUDE_FIELDS: list[str] = []

    # OpenAPI Merger
    OPENAPI_CACHE_DURATION: int = 30 * 60  # In seconds
    OPENAPI_MAIN_ENDPOINT: str = "https://tracker.icon.community/api/v1/docs/doc.json"
    OPENAPI_CONTRACTS_ENDPOINT: str = "https://tracker.icon.community/api/v1/contracts/docs/openapi.json"
    OPENAPI_GOVERNANCE_ENDPOINT: str = "https://tracker.icon.community/api/v1/governance/docs/openapi.json"
    OPENAPI_STATS_ENDPOINT: str = "https://tracker.icon.community/api/v1/statistics/docs/openapi.json"

    model_config = SettingsConfigDict(
        case_sensitive=False,
    )


def load_env_to_variables(env_file_path):
    """
    Load environment variables from a .env file and export them to the actual environment variables.

    Args:
    - env_file_path (str): Path to the .env file

    Returns:
    - None
    """
    # Load environment variables from the .env file
    env_vars = dotenv_values(env_file_path)

    # Export variables to the actual environment
    for key, value in env_vars.items():
        os.environ[key] = value


# Ignored by default
test_env = os.path.join(os.path.dirname(__file__), "..", ".env.test")
if os.environ.get("ENV_FILE", False):
    load_env_to_variables(os.environ.get("ENV_FILE"))
elif os.path.isfile(test_env):
    load_env_to_variables(test_env)

config = Settings()
