import pickle

def save (obj, file_name):
    with open (file_name, "wb") as file:
        pickle.dump (obj, file)

def load (file_name):
    with open (file_name, "rb") as file:
        return pickle.load(file)

