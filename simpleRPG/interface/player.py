
class IPlayer:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_parameters(self):
        print(self.name)

    def set_parameters(self, name, params):
        pass