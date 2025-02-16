from typing import Optional

from pydantic import BaseModel


class Status(BaseModel):
    errCode: int
    errMsg: str


class Query(BaseModel):
    question: str
    lang: str = "zh"
    sessionId: Optional[str] = None
    stream: bool = False
    topicId: Optional[str] = None
    searchTopicId: Optional[str] = None
    enableMix: bool = False
    newEngine: bool = False
    mode: str = None
    enableImage: bool = False


class Topic(BaseModel):
    id: Optional[str] = None
    name: str
    dirRootId: Optional[str] = None
    description: Optional[str] = None


class File(BaseModel):
    id: Optional[str]
    fileName: str
    parentId: str
    contentType: str
    size: int
    previewUrl: Optional[str] = None
    originalUrl: Optional[str] = None
    progress: int
