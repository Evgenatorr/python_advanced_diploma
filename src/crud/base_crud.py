from abc import ABC, abstractmethod


class BaseCrud(ABC):

    @abstractmethod
    def __init__(self, model):
        self.model = model

    @abstractmethod
    def get(self, session, obj_id):
        pass

    @abstractmethod
    def get_list(self, session):
        pass

    @abstractmethod
    def post(self, session, data):
        pass

    @abstractmethod
    def delete(self, session, obj_id):
        pass

    @abstractmethod
    def update(self, session, current_data, new_data):
        pass

    @abstractmethod
    def patch(self, session, obj_id, new_data):
        pass
