from typing import Optional

from .client import client
from .model import Status, Book


def upload_book(fileobj_or_url) -> Optional[Book]:
    """上传文件或 URL 到书架。

    :param fileobj_or_url: 待上传的文件对象或则 URL。
    :return: 如果文件上传成功，返回 Book 对象；否则返回 None。
    """
    if isinstance(fileobj_or_url, str):
        params = {"data": {"url": fileobj_or_url}}
    else:
        params = {"files": {"file": fileobj_or_url}}
    resp = client.put("/book", **params)
    json = resp.json()
    status = Status.model_validate(json)
    if status.errCode == 0:
        book = Book.model_validate(json["data"])
        return book
