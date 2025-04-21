"""metaso-sdk package.

The official Python SDK for https://metaso.cn
"""

from __future__ import annotations

from .model import File, Book, Query, Status, Topic
from .search import search
from .subject import create_topic, delete_file, delete_topic, update_progress, upload_directory, upload_file
from .bookshelf import upload_book

__all__: list[str] = [
    "Status",
    "Query",
    "Topic",
    "File",
    "Book",
    "search",
    "create_topic",
    "delete_topic",
    "upload_file",
    "upload_book",
    "update_progress",
    "delete_file",
    "upload_directory",
]
