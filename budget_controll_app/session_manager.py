from logger import logger


class SessionManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session = None

    def __enter__(self):
        """Creating session during context enter"""
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):

        try:
            if exc_type is not None:
                logger.error(f"Exception type: {exc_type}, value: {exc_val}")
                self.session.rollback()
            else:
                self.session.commit()
        finally:
            self.session.close()
