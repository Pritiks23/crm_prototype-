from typing import Callable, Dict, List

subscribers: Dict[str, List[Callable]] = {}

def subscribe(event_type: str, handler: Callable):
    if event_type not in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append(handler)

def publish(event_type: str, payload: dict):
    if event_type in subscribers:
        for handler in subscribers[event_type]:
            handler(payload)
