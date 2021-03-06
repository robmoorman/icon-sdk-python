# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from os import path, walk
from io import BytesIO
from zipfile import ZipFile, ZIP_DEFLATED
from iconsdk.exception import ZipException


def gen_deploy_data_content(_path: str) -> bytes:
    """Generate zip data(hex string) of SCORE.

    :param _path: Path of the directory to be zipped.
    """
    if path.isdir(_path) is False:
        raise ValueError(f"Invalid path {_path}")
    try:
        memory_zip = InMemoryZip()
        memory_zip.zip_in_memory(_path)
    except ZipException:
        raise ZipException(f"Can't zip SCORE contents")
    else:
        return memory_zip.data


class InMemoryZip:
    """Class for making zip data in memory using BytesIO."""

    def __init__(self):
        self._in_memory = BytesIO()

    @property
    def data(self) -> bytes:
        """Returns zip data

        :return: zip data
        """
        self._in_memory.seek(0)
        return self._in_memory.read()

    def zip_in_memory(self, _path):
        """Makes zip data(bytes) in memory.

        :param _path: Path of the directory to be zipped.
        """
        try:
            with ZipFile(self._in_memory, 'a', ZIP_DEFLATED, False) as zf:
                if path.isfile(_path):
                    zf.write(_path)
                else:
                    for root, folders, files in walk(_path):
                        if root.find('__pycache__') != -1:
                            continue
                        if root.find('/.') != -1:
                            continue
                        for file in files:
                            if file.startswith('.'):
                                continue
                            full_path = path.join(root, file)
                            zf.write(full_path)
        except ZipException:
            raise ZipException

