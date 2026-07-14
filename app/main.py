# app/main.py
import asyncio
import json
import os
import time
from datetime import datetime
from typing import Dict, Any, List

from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import ValidationError
import structlog

# Assuming these are the files with the models and services
from .ai_model import AIModel # Your AI model logic
from .services.kafka_service import KafkaService, get_kafka_service # Your Kafka consumer/producer
from .models import WalletTransactionMessage, WalletScoreSuccess, WalletScoreFailure # Pydantic models for validation
from .config import Settings # New configuration model

# --- Logging Setup ---
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory,
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger()

# --- App Initialization ---
settings = Settings()
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION
)
ai_model = AIModel()

# Global variables for statistics
stats = {
    "processed_count": 0,
    "success_count": 0,
    "failure_count": 0,
    "last_processed_timestamp": None
}

# --- Kafka Setup ---
kafka_service = get_kafka_service()

async def kafka_processor():
    """
    Background task to consume messages from Kafka, process them, and publish results.
    """
    global stats
    logger.info("Starting Kafka message processor...")
    while True:
        try:
            consumer = kafka_service.get_consumer()
            producer = kafka_service.get_producer()

            for msg in consumer:
                logger.info(
                    "Received message",
                    topic=msg.topic,
                    wallet_address=msg.value.get('wallet_address', 'N/A')
                )
                stats["processed_count"] += 1
                stats["last_processed_timestamp"] = int(msg.timestamp / 1000)

                try:
                    # 1. Validate the incoming message using Pydantic
                    message_data = WalletTransactionMessage.model_validate(msg.value)

                    # 2. Process the data using the AI model
                    final_score, features = ai_model.calculate_score(message_data.model_dump())
                    
                    # Create the success message
                    output_message = WalletScoreSuccess(
                        wallet_address=message_data.wallet_address,
                        zscore=f"{final_score:.18f}",  # 18 decimal places for blockchain compatibility
                        timestamp=int(datetime.now().timestamp()),
                        categories=[
                            {
                                "category": "dexes",
                                "score": final_score,
                                "transaction_count": features.get('total_transaction_count', 0),
                                "features": {k: v for k, v in features.items() if k != 'user_tags'}
                            }
                        ]
                    )
                    
                    # 3. Publish the successful result to the Kafka success topic
                    producer.send(kafka_service.SUCCESS_TOPIC, value=output_message.model_dump_json().encode('utf-8'))
                    logger.info("Published success", wallet_address=message_data.wallet_address)
                    stats["success_count"] += 1

                except (ValidationError, Exception) as e:
                    logger.error(
                        "Processing failed",
                        wallet_address=msg.value.get('wallet_address', 'N/A'),
                        error=str(e)
                    )
                    stats["failure_count"] += 1
                    # Create the failure message
                    failure_message = WalletScoreFailure(
                        wallet_address=msg.value.get('wallet_address', 'N/A'),
                        timestamp=int(datetime.now().timestamp()),
                        error=str(e)
                    )
                    # Publish the failure result to the Kafka failure topic
                    producer.send(kafka_service.FAILURE_TOPIC, value=failure_message.model_dump_json().encode('utf-8'))

            await asyncio.sleep(1) # Sleep to prevent busy-looping
        
        except Exception as e:
            logger.error("Fatal Kafka consumer error", error=str(e))
            await asyncio.sleep(5)  # Wait before retrying to reconnect

# --- FastAPI Endpoints ---
@app.on_event("startup")
async def startup_event():
    """
    Event handler for application startup.
    Starts the Kafka message processor as a background task.
    """
    asyncio.create_task(kafka_processor())

@app.on_event("shutdown")
async def shutdown_event():
    """
    Event handler for application shutdown.
    Shuts down the Kafka consumer gracefully.
    """
    await kafka_service.stop_consumer()
    logger.info("Application shutdown completed.")

@app.get("/")
def read_root():
    """Root endpoint providing service information."""
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running"
    }

@app.get("/api/v1/health")
def health_check():
    """
    Health check endpoint to ensure the service is running.
    """
    return {"status": "ok"}

@app.get("/api/v1/stats")
def get_stats():
    """
    Returns current processing statistics.
    """
    return stats
