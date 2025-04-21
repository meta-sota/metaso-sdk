import json

from httpx_sse import EventSource, connect_sse

from .client import client
from .model import Query, Topic

EventSource._check_content_type = lambda self: True


def search(query: Query, *, stream: bool = False, topic: Topic = None):
    """搜索功能的函数注释。

    :param query: 查询对象，用于指定搜索内容。
    :param stream: 布尔值，表示是否以流的形式返回结果，默认为False。
    :param topic: 专题对象，用于指定搜索的专题，默认为None。
    :return: 根据查询条件返回搜索结果。
    """
    if topic is not None:
        query.searchTopicId = topic.id

    if stream:
        query.stream = True

    def _gen():
        with connect_sse(client, "POST", "/search/v2", json=query.model_dump()) as event_source:
            for sse in event_source.iter_sse():
                if (data := sse.data) != "[DONE]":
                    yield json.loads(data)

    if query.stream:
        return _gen()

    resp = client.post("/search/v2", json=query.model_dump())
    resp.raise_for_status()
    return resp.json()["data"]
