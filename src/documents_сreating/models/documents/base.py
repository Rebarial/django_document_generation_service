from ..base import BaseModel

class BaseDocument(BaseModel):

    class Meta:
        abstract = True