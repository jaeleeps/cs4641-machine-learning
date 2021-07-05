from pydantic.main import BaseModel

class NytArchiveTransform_V1(BaseModel):
    abstract: str
    snippet: str
    lead_paragraph: str
    source: str

    headline_main: str

    pub_date: str

