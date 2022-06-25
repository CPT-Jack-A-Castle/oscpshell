from remote.remotestrategy import RemoteStrategy
from pathlib import Path


class WindowsRemote(RemoteStrategy):
    def enum(self, username: str):
        raise NotImplementedError()

    def get(self, arg: Path):
        raise NotImplementedError()

    def put(self, arg: Path):
        raise NotImplementedError()
