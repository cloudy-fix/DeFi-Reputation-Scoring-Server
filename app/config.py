# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Model_config is used to configure Pydantic settings
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Kafka configuration
    KAFKA_BROKER: str = "localhost:9092"
    KAFKA_INPUT_TOPIC: str = "wallet-transactions"
    KAFKA_SUCCESS_TOPIC: str = "wallet-scores-success"
    KAFKA_FAILURE_TOPIC: str = "wallet-scores-failure"

    # API configuration
    API_TITLE: str = "DeFi Reputation Scoring Server"
    API_DESCRIPTION: str = "A microservice to calculate wallet reputation scores using AI."
    API_VERSION: str = "1.0.0"