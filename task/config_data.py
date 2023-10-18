class ConfigData:
    def __init__(self):
        self.server = "178.63.101.40"
        self.port = 8087
        self.username = "operator"
        self.password = "test_elecard"
        self.token = None
        self.auth_payload = {
            "username": self.username,
            "password": self.password
        }
        self.group_payload = {
            "name": "GroupX",
            "description": "some text"
        }
        self.player_payload = {
            "name": "Player",
            "description": "some text",
            "mac": "00:00:00:00:00:03",
            "mediaGroup": 1
        }

    @property
    def url(self):
        return f"http://{self.server}:{self.port}/"


config = ConfigData()
