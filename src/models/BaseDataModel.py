from src.helpers.config import get_settings, Settings


class BaseDataModel:
    """
    Base class for all data models.
    Provides shared functionality like database client access and application settings.
    """
    def __init__(self, db_client: object):
        """
        Initialize the base data model.
        :param db_client: The database client (e.g., MongoDB client).
        """
        self.db_client = db_client
        self.app_settings = get_settings()