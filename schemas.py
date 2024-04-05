from pydantic import BaseModel
from typing import Union,Optional

# class Student(BaseModel):
#     name: str
#     age: int
#     city:str
 
class URLShortener(BaseModel):
    # uni_code: str
    og_url: str
    # short_url: str
    alias: Optional[str] = None