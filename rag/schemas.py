from pydantic import BaseModel

class Prompt(BaseModel):
    question: str
    name: str
    description: str
    rag_hints: str
    authorized_functions: str
    body: str
    prototype: str
    program: bool
    previous_attempts: list[str]