from pydantic import (Field, PrivateAttr)
from pydantic import (BaseModel, AfterValidator)
from typing import Annotated

from PIL import Image

class Picture(BaseModel):
    OriginalPath: Annotated[str, AfterValidator(lambda x: x.strip())] = Field(min_length=1)
    _original: Image = PrivateAttr()

    @property
    def Original(self) -> Image:
        return self._original
    
    
    
    def __init__(self, path:str):
        super().__init__(
            OriginalPath=path
        )

        #
        # Note:
        # Private attributes are defined at the end of the creation of the instance
        # ==> Update them after !!
        #
        self._original = Image.open(path)
        print(self._original.size)

pic = Picture(path='/shared/FotosVarias/medusa-test-images/2014/12/20141226_024252260_iOS.jpg')

print(pic)

pic.Original.show()