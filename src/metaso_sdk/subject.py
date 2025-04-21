from pathlib import Path
from typing import List, Optional, Union

from streamable import Stream

from .client import client
from .model import File, Book, Status, Topic


def create_topic(topic: Topic) -> Optional[Topic]:
    """创建一个新专题。

    :param topic (Topic): 要创建的专题对象。
    :return: 专题对象。
    """
    resp = client.put("/topic", json=topic.model_dump())
    resp.raise_for_status()
    json = resp.json()
    status = Status.model_validate(json)
    if status.errCode == 0:
        topic = Topic.model_validate(json["data"])
        return topic


def delete_topic(topic: Topic) -> bool:
    """删除指定的专题。

    :param topic (Topic): 要删除的Topic对象。
    :return: 如果成功删除Topic返回True，否则返回False。
    """
    resp = client.post("/topic/trash", json={"ids": [topic.id]})
    resp.raise_for_status()
    status = Status.model_validate(resp.json())
    return status.errCode == 0


def upload_file(topic: Topic, file) -> Optional[File]:
    """上传文件到指定专题。

    :param topic (Topic): 文件所属的专题。
    :param file: 待上传的文件对象。
    :return: 如果文件上传成功，返回文件对象；否则返回None。
    """
    resp = client.put(f"/file/{topic.dirRootId}", files={"file": file})
    resp.raise_for_status()
    json = resp.json()
    status = Status.model_validate(json)
    if status.errCode == 0:
        file = File.model_validate(json["data"][0])
        return file


def update_progress(file_or_book: Union[File, Book]) -> Union[File, Book]:
    """更新处理进度。

    :param file_or_book: 待更新进度的 File 或者 Book 对象。
    :return: 更新 progress 后的对象。
    """
    file_id = file_or_book.id if isinstance(file_or_book, File) else file_or_book.fileId
    resp = client.get(f"/file/{file_id}/progress")
    resp.raise_for_status()
    json = resp.json()
    status = Status.model_validate(json)
    if status.errCode == 0:
        file_or_book.progress = json["data"]
    return file_or_book


def delete_file(file_or_book: Union[File, Book]) -> bool:
    """删除文件。

    :param file_or_book: 待删除的 File 或者 Book 对象。
    :return: 如果删除成功，返回True。否则返回False。
    """
    file_id = file_or_book.id if isinstance(file_or_book, File) else file_or_book.fileId
    resp = client.post("/file/trash", json={"ids": [file_id]})
    resp.raise_for_status()
    status = Status.model_validate(resp.json())
    return status.errCode == 0


def upload_directory(topic: Topic, path: Path, pattern="**/*", *, concurrency=10) -> List[File]:
    """递归上传指定目录下的文件到指定专题。

    参数:
    - topic: 目标专题。
    - path: 需要上传的本地目录路径。
    - pattern: 文件匹配模式，默认为"**/*"，表示匹配所有文件。
    - concurrency: 并发上传的数量，默认为10。

    返回:
    - List[File]: 成功上传的文件列表。
    """

    def _upload_file(file) -> File:
        with file.open("rb") as f:
            return upload_file(topic, f)

    files = list(
        Stream(Path(path).glob(pattern))
        .filter(Path.is_file)
        .map(_upload_file, concurrency=concurrency)
        .filter(lambda file: file is not None)
        .observe("files")
        .catch(),
    )

    return files
