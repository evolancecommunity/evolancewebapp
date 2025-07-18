from evolancewebapp.backend.models.data import PSYCHOLOGY_BOOKS, MEDITATION_BOOKS

class DataService:
    def get_psychology_books(self):
        """Get psychology books data"""
        return PSYCHOLOGY_BOOKS

    def get_meditation_books(self):
        """Get meditation books data"""
        return MEDITATION_BOOKS