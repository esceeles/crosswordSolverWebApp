from Model import Model

class model(Model):
    """initializes null list"""
    def __init__(self):
        self.entries = []
    """return current list"""
    def select(self):
        return self.entries
    """Append list containing puzzle, type, and puzString to list"""
    def insert(self, puzzle, type, puzString):
        params = [puzzle, type, puzString]
        self.entries.append(params)
        return True