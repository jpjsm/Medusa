from pydantic import  PrivateAttr
from pydantic import BaseModel

class User(BaseModel):
    name: str
    _password: str = PrivateAttr()

    def set_password(self, password: str):
        self._password = password

    def check_password(self, password: str) -> bool:
        return self._password == password
    
    @property
    def Pwd(self) -> str:
        return self._password
    
    def __init__(self, name:str, pwd: str):
        super().__init__(
            name=name
        )
        self._password = pwd


user = User(name="Alice", pwd='secret')
#user.set_password("secret")
print(user)
print(user.check_password('qwerty'))
print(user.check_password('secret'))
print(user.Pwd)
