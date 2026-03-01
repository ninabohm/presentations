from domain.directory.directory import Directory
from domain.git_repo.git_repo_repository import GitRepoRepository


class GitRepoService:
    def __init__(self, repository: GitRepoRepository):
        self.repository = repository

    def is_initialized(self, directory: Directory) -> bool:
        return self.repository.is_initialized(directory)
