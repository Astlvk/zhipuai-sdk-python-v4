from __future__ import annotations

from typing import TYPE_CHECKING

import httpx

from ..core._base_api import BaseAPI
from ..core._base_type import NOT_GIVEN, Body, Query, Headers, NotGiven, FileTypes
from ..core._files import is_file_content
from ..core._http_client import (
    make_user_request_input,
)
from ..types.file_object import FileObject

if TYPE_CHECKING:
    from .._client import ZhipuAI

__all__ = ["Files"]


class Files(BaseAPI):

    def __init__(self, client: "ZhipuAI") -> None:
        super().__init__(client)

    def create(
            self,
            *,
            file: FileTypes,
            purpose: str,
            extra_headers: Headers | None = None,
            extra_query: Query | None = None,
            extra_body: Body | None = None,
            timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> FileObject:

        if not is_file_content(file):
            prefix = f"Expected file input `{file!r}`"
            raise RuntimeError(
                f"{prefix} to be bytes, an io.IOBase instance, PathLike or a tuple but received {type(file)} instead."
            ) from None
        files = [("file", file)]

        extra_headers = {"Content-Type": "multipart/form-data", **(extra_headers or {})}

        return self._post(
            "/files",
            body={
                "purpose": purpose,
            },
            files=files,
            options=make_user_request_input(
                extra_headers=extra_headers, timeout=timeout
            ),
            cast_type=FileObject,
        )

