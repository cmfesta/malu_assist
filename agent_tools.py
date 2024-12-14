from pydantic.v1 import BaseModel, Field, validator
from langchain_core.tools import ToolException
import re
from langchain_experimental.utilities import PythonREPL


class SearchInput(BaseModel):
    summary: str = Field(description="Description of the meeting")
    start_datetime: str = Field(
        description="The time the meeting will start, the data should be in yyyy-mm-dd HH:mm:ss"
    )
    end_datetime: str = Field(
        description="The time the meeting will end, the data should be yyyy-mm-dd HH:mm:ss"
    )

    @validator("summary")
    def validate_summary(cls, v):
        if not type(v) == str:
            raise ToolException("Tipo errado")
        return v

    @validator("start_datetime")
    def validate_start_datetime(cls, v):
        regex_exp = "^(\d{4})\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01]) ([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$"
        if not re.match(regex_exp, v):
            raise ToolException("Incorrect data format, should be yyyy-mm-dd HH:mm:ss")
        return v

    @validator("end_datetime")
    def validate_end_datetime(cls, v):
        regex_exp = "^(\d{4})\-(0?[1-9]|1[012])\-(0?[1-9]|[12][0-9]|3[01]) ([0-1][0-9]|[2][0-3]):([0-5][0-9]):([0-5][0-9])$"
        if not re.match(regex_exp, v):
            raise ToolException("Incorrect data format, should be yyyy-mm-dd HH:mm:ss")
        return v


class ValidInput(BaseModel):
    input: str = Field(description="Python code ready to be executed")

    @validator("input")
    def validate_input(cls, v):
        if not type(v) == str:
            raise ToolException("Tipo errado")
        return v


def pythonInterpreter(input: str) -> str:
    """Function that recieves a python code and prints the answer with print() function

    Args:
    input: Python code ready to be executed. It MUST print the final result of the code using print() function.

    Return:
    String with the answer
    """
    input = input.replace("```python", "").replace("```", "").strip()
    return PythonREPL().run(input)