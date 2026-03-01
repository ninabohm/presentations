from domain.directory.directory import Directory
from domain.directory.directory_repository import DirectoryRepository


class DirectoryService:
    def __init__(self, repository: DirectoryRepository):
        self.repository = repository

    def create_temp_directory(self) -> Directory:
        return self.repository.create_temp_directory()
