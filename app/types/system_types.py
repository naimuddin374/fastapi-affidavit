from enum import Enum as PyEnum
# --- NEW ENUM DEFINITIONS ---


class DocumentStatus(PyEnum):
    """Defines the stages of document processing."""
    PENDING = "pending"
    UPLOADED = "uploaded"
    IN_PROGRESS = "in-progress"
    COMPLETE = "complete"
    CANCEL = "cancel"


class DocumentType(PyEnum):
    """Defines the type of data the document contains."""
    STATEMENT = "statement"
    OTHER = "other"
