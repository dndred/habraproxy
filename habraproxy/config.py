import os


class Config:
    def __init__(self):
        env = os.environ
        self.front_host = env.get('FRONT_HOST', '127.0.0.1')
        self.bind_host = env.get('BIND_HOST', '0.0.0.0')
        self.port = env.get('PORT', 8080)
        self.remote_url = env.get('REMOTE_URL', 'https://habr.com/')

    @property
    def local_url(self):
        return f'http://{self.front_host}:{self.port}/'

    __inst = None

    @classmethod
    def get_instance(cls) -> 'Config':
        if not cls.__inst:
            cls.__inst = Config()
        return cls.__inst
