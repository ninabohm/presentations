import re

from behave import given, then, when
from test_helpers.command_runner import CommandRunner
from test_helpers.temp_git_repo import TempGitRepo
from domain.directory.directory_service import DirectoryService
from domain.directory.directory_repository import DirectoryRepository
from domain.git_repo.git_repo_service import GitRepoService
from domain.git_repo.git_repo_repository import GitRepoRepository


@given(u'I have a directory that is not a git repository')
def step_impl(context):
    directory_repository = DirectoryRepository()
    directory_service = DirectoryService(directory_repository)
    context.directory = directory_service.create_temp_directory()
    context.git_repo_repository = GitRepoRepository()
    context.git_repo_service = GitRepoService(context.git_repo_repository)
    assert not context.git_repo_service.is_initialized(context.directory)


@when(u'I run git init in the directory')
def step_impl(context):
    # temp initializing the git repo in this step to apply DDD one by one
    context.repo = TempGitRepo()
    context.repo.init()


@then(u'a .git directory exists')
def step_impl(context):
    cmd = CommandRunner()
    result = cmd.run(context.repo.dirpath, 'ls', '.git')
    assert result.exitcode == 0


@then(u'.git/HEAD contains the text "ref: refs/heads/main"')
def step_impl(context):
    head_content = context.repo.read_head()
    errmsg = f"Expected 'ref: refs/heads/main', but got '{head_content}'"
    assert head_content == "ref: refs/heads/main", errmsg


@then(u'.git/refs/heads/main doesn\'t exist')
def step_impl(context):
    cmd = CommandRunner()
    result = cmd.run(context.repo.dirpath, 'ls', '.git/refs/heads/main')
    assert result.exitcode != 0


@given(u'I have an empty repository')
def step_impl(context):
    context.execute_steps(u'''
        Given I have a directory that is not a git repository
        When I run git init in the directory
    ''')


@when(u'a series of commits is made with messages: {messages}')
def step_impl(context, messages):
    message_list = [msg. strip() for msg in messages.split(',')]
    for message in message_list:
        context.repo.add_test_commit_with_message(message)


@then(u'running "git log --oneline" prints out')
def step_impl(context):
    cmd = CommandRunner()
    log_output = cmd.run(context.repo.dirpath,
                         'git', 'log', '--oneline').output
    commit_messages = log_output.split('\n')
    sha_pattern = r'[0-9a-f]{7}'

    for i, row in enumerate(context.table):
        message = f"{sha_pattern} {row['message']}"
        errmsg = f'''
            Expected commit message: {message}
            But got: {commit_messages[i]}'''
        assert re.match(message, commit_messages[i]), errmsg


@then(u'the contents of .git/refs/heads/main contains a SHA')
def step_impl(context):
    cmd = CommandRunner()
    result = cmd.run(context.repo.dirpath, 'cat', ".git/refs/heads/main")
    debugging = cmd.run(context.repo.dirpath, 'ls', "-laR")
    assert result.output != '', debugging.output


@then(u'the parent commit of HEAD does not exist')
def step_impl(context):
    cmd = CommandRunner()
    result = cmd.run(context.repo.dirpath, 'git', 'cat-file', 'commit', 'HEAD')
    contains_parent = 'parent' in result.output
    errmsg = f"Expected no parent in the following output: {result.output}"
    assert contains_parent is False, errmsg
