import tempfile
from behave import given, when, then
from git_repo import TempGitRepo
from command_runner import CommandRunner



@given(u'a series of commits is made with messages')
def step_impl(context):
    context.repo = TempGitRepo(dirpath=tempfile.mkdtemp())
    context.command_runner = CommandRunner(context.repo.dirpath)
    context.repo.init_with_commits(['great', 'is', 'git', 'think', 'I'])


@when(u'I checkout the commit with the message \'git\' using its SHA')
def step_impl(context):
    context.sha = context.command_runner.capture_output_from_commands(['git', 'rev-parse', 'HEAD^^'])
    context.repo.checkout_quiet(context.sha)


@then(u'git is in a detached HEAD state')
def step_impl(context):
    head_content = context.repo.get_head()
    assert head_content == context.sha
    assert not head_content.startswith('ref: ')
