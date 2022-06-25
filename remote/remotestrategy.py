from abc import ABC, abstractmethod
from pathlib import Path
import os


class RemoteStrategy(ABC):
    def __init__(self, conn):
        self._conn = conn
        self.basedir = Path(os.getcwd())

    @abstractmethod
    def enum(self, username: str):
        pass

    @abstractmethod
    def get(self, arg: Path):
        pass

    @abstractmethod
    def put(self, arg: Path):
        pass
