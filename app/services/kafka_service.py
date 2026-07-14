# app/services/kafka_service.py

import json
import asyncio
import os
from kafka import KafkaConsumer, KafkaProducer

# --- Singleton Pattern for Kafka Service ---
class KafkaService:
    _instance = None
    _consumer = None
    _producer = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(KafkaService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Prevent re-initialization
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")
        self.INPUT_TOPIC = os.getenv("KAFKA_INPUT_TOPIC", "wallet-transactions")
        self.SUCCESS_TOPIC = os.getenv("KAFKA_SUCCESS_TOPIC", "wallet-scores-success")
        self.FAILURE_TOPIC = os.getenv("KAFKA_FAILURE_TOPIC", "wallet-scores-failure")
        
        self._consumer_task = None

    def get_consumer(self):
        if not self._consumer:
            self._consumer = KafkaConsumer(
                self.INPUT_TOPIC,
                bootstrap_servers=self.KAFKA_BROKER,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                group_id="reputation-scorer-group"
            )
        return self._consumer

    def get_producer(self):
        if not self._producer:
            self._producer = KafkaProducer(
                bootstrap_servers=self.KAFKA_BROKER,
                value_serializer=lambda x: json.dumps(x).encode('utf-8')
            )
        return self._producer
    
    async def run_consumer(self):
        """
        Starts the Kafka consumer loop.
        """
        consumer = self.get_consumer()
        while True:
            for msg in consumer:
                # This will be handled by the main application logic
                yield msg
            await asyncio.sleep(1) # Sleep to prevent busy-looping
            
    async def stop_consumer(self):
        """
        Stops the Kafka consumer gracefully.
        """
        if self._consumer:
            self._consumer.close()
            
def get_kafka_service():
    """Dependency injection function for FastAPI."""
    return KafkaService()

