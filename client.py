class User:
    def __init__ (self, username, displayName, password, rank):
        self.username = username
        self.displayName = displayName
        self.password = password
        self.rank = rank

class Mission ():
    def __init__ (self, _id, name, description, rank, reward):
        self._id = _id
        self.name = name
        self.description = description
        self.rank = rank
        self.reward = reward

class Post ():
    def __init__ (self, _id, title, text, file, author, time):
        self._id = _id
        self.title = title
        self.text = text
        self.file = file
        self.author = author
        self.time = time