import tempfile

from domain.directory.directory import Directory


class DirectoryRepository:
    def create_temp_directory(self) -> Directory:
        return Directory(tempfile.mkdtemp())
