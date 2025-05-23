from collections.abc import Generator

from _typeshed import Incomplete
from behave._types import Unknown as Unknown

def parse_bool(text): ...
def parse_user_define(text): ...
def unqote(text): ...

class UserData(dict):
    def getas(
        self,
        convert,
        name,
        default: Incomplete | None = None,
        valuetype: Incomplete | None = None,
    ): ...
    def getint(self, name, default: int = 0): ...
    def getfloat(self, name, default: float = 0.0): ...
    def getbool(self, name, default: bool = False): ...
    @classmethod
    def make(cls, data): ...

class UserDataNamespace:
    namespace: Incomplete
    data: Incomplete
    def __init__(self, namespace, data: Incomplete | None = None) -> None: ...
    @staticmethod
    def make_scoped(namespace, name): ...
    def get(self, name, default: Incomplete | None = None): ...
    def getas(
        self,
        convert,
        name,
        default: Incomplete | None = None,
        valuetype: Incomplete | None = None,
    ): ...
    def getint(self, name, default: int = 0): ...
    def getfloat(self, name, default: float = 0.0): ...
    def getbool(self, name, default: bool = False): ...
    def __contains__(self, name) -> bool: ...
    def __getitem__(self, name): ...
    def __setitem__(self, name, value) -> None: ...
    def __len__(self) -> int: ...
    def scoped_keys(self): ...
    def keys(self) -> Generator[Incomplete, None, None]: ...
    def values(self) -> Generator[Incomplete, None, None]: ...
    def items(self) -> Generator[Incomplete, None, None]: ...
