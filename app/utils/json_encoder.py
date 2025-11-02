import json
from datetime import datetime


def serialize_data(obj: object) -> object:
    """
    A generic function to convert complex objects into a JSON-serializable format.
    This is passed to the 'default' argument of json.dumps().
    """
    # 1. Handle Datetime Objects (A common serialization failure)
    if isinstance(obj, datetime):
        return obj.isoformat()

    # 2. Handle SQLAlchemy/Pydantic Models
    # Look for common methods used by frameworks to convert to a dictionary:

    # Check for Pydantic V2 method
    if hasattr(obj, 'model_dump'):
        return obj.model_dump()

    # Check for Pydantic V1 method
    if hasattr(obj, 'dict'):
        return obj.dict()

    # Check for SQLAlchemy conversion (using __dict__ and cleaning up)
    if hasattr(obj, '__dict__'):
        # For SQLAlchemy, we often need to clean up internal state attributes
        data = dict(obj.__dict__)
        # Remove SQLAlchemy internal state
        data.pop('_sa_instance_state', None)
        return data

    # 3. Raise TypeError for truly unknown objects
    raise TypeError(
        f"Object of type {obj.__class__.__name__} is not JSON serializable")
