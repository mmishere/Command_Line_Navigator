from plumbum import cli
from pyfiglet import Figlet
from plumbum.cmd import ls, git
from questionary import prompt

def print_banner(text):
    print(Figlet(font='mini').renderText(text))

def get_files():
    ls_output = ls().strip()
    files = ls_output.split("\n")
    return files

def filter_underscore(name) -> bool:
    if (name[0] == '_'):
        return False
    return True

def generate_question(files):
    filtered_files = filter(filter_underscore, files)
    print(filtered_files)

    return [{
        'type': 'checkbox',
        'name': 'files',
        'message': 'Select files to add!',
        'choices': [{'name': file.strip()} for file in filtered_files],
    }]
class FancyGitAdd(cli.Application):
    VERSION = "1.0"
    commit = cli.Flag(['c', 'commit'], help = 'Commits the added files.')
    push = cli.Flag(['p', 'push'], help = 'Pushes files.')

    def main(self):
        print_banner("Fancy Git Add!")
        files = get_files()

        question = generate_question(files)
        answers = prompt(question)
        print(answers['files'])
        git('add', answers['files'])

        if self.commit:
            commit_text = input("Add commit text! ")
            git('commit', '-m', commit_text)

        if self.push:
            git('push')


if __name__ == "__main__":
    FancyGitAdd()


## TESTS


def test_get_files():
    files = get_files()
    assert len(files) == 7, "Should be 7 files"

def test_generate_question():
    files = ["best.rb", "good.kt", "small.py"]
    question = generate_question(files)
    assert len(question) == 1, "One question"
    assert question[0]['type'] == 'checkbox', "Should be checkbox"
    assert len(question[0]['choices']) == len(files), "choices = files length"