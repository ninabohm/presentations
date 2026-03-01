from domain.directory.directory import Directory
from test_helpers.command_runner import CommandRunner

class GitRepoRepository:
    def __init__(self):
        pass

    def is_initialized(self, directory: Directory) -> bool:
        cmd = CommandRunner()
        result = cmd.run(directory.path, 'ls', '.git')
        return result.exitcode == 0
