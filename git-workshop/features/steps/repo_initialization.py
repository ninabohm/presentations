from behave import *
import tempfile
import subprocess
import os

@given(u'I have a directory that is not a git repository')
def step_impl(context):
    dirpath = tempfile.mkdtemp()
    result = subprocess.run(['ls', '.git'], cwd=dirpath)
    context.dirpath = dirpath
    assert result.returncode != 0


@when(u'I run git init in the directory')
def step_impl(context):
    # Figuring out how to prevent the line break after this would be useful
    result = subprocess.run(['git', 'init', '--initial-branch=main'],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL,
                   cwd=context.dirpath)
    assert result.returncode == 0


@then(u'a .git directory exists')
def step_impl(context):
    result = subprocess.run(['ls', '.git'], cwd=context.dirpath)
    assert result.returncode == 0


@then(u'.git/refs contains a directory named heads')
def step_impl(context):
    dir_path = os.path.join(context.dirpath, '.git', 'refs', 'heads')
    assert os.path.isdir(dir_path)
