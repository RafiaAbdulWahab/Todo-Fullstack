import json
import logging
from typing import Any, Dict

try:
    from dapr.clients import DaprClient
    from dapr.clients.grpc._client import DaprClient as DaprGrpcClient
except ImportError:
    logging.warning("Dapr client not found, running in development mode without Dapr.")

    class DaprClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass

        async def publish_event(
            self, pubsub_name: str, topic_name: str, data: str, data_content_type: str
        ):
            logging.info(
                f"Mock DaprClient: Publishing event to pubsub={pubsub_name}, topic={topic_name}, data={data}"
            )



DAPR_PUB_SUB_NAME = "todo-pubsub"  # This should match the Dapr component name for pubsub
TODO_EVENTS_TOPIC = "todo-events"  # This should match the Kafka topic name


async def publish_event(event_type: str, data: Dict[str, Any]):
    """
    Publishes an event to the todo-events Kafka topic via Dapr Pub/Sub asynchronously.

    Args:
        event_type (str): The type of event (e.g., "todo_created", "todo_updated").
        data (Dict[str, Any]): The data associated with the event.
    """
    event_payload = {"eventType": event_type, "data": data}
    async with DaprClient() as client:
        await client.publish_event(
            pubsub_name=DAPR_PUB_SUB_NAME,
            topic_name=TODO_EVENTS_TOPIC,
            data=json.dumps(event_payload),
            data_content_type="application/json",
        )
    print(f"Published event to Dapr Pub/Sub: {event_payload}")


# Example usage (for testing purposes)
if __name__ == "__main__":
    import asyncio

    async def main():
        test_data: Dict[str, Any] = {"id": "123", "title": "Test Todo", "status": "new"}
        await publish_event("todo_created", test_data)

    asyncio.run(main())