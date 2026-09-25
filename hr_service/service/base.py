from utils.db_manager import DBManager


class BaseService:

    def __init__(self, db: DBManager | None = None):
        self.db = db