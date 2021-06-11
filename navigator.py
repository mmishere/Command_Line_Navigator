from plumbum import cli
from pyfiglet import Figlet
# from plumbum.cmd import ls, cd
from questionary import prompt
import questionary

from plumbum.cmd import ls, mkdir, touch
from plumbum import local
# cd = local["cd"]


# possibly also include mkdir and touch, to create new files while on here

def print_banner(text):
    print(Figlet(font='mini').renderText(text))

def get_files():
    files = ["New file", "New folder", ".."]
    ls_output = ls() # how to include hidden files?
    files += ls_output.split("\n")
    return files

def generate_question(files):
    return questionary.rawselect(
        "Select the desired next location",
        choices = [{'name': file.strip()} for file in files]
    )
    # return [{
    #     'type': 'rawselect',
    #     'name': 'file',
    #     'message': 'Select the desired next location',
    #     'choices': [{'name': file.strip()} for file in files]
    # }]

class Navigator(cli.Application):
    VERSION = "1.0"
    all_flag = cli.Flag(['a', 'all'], help = 'List all files during navigation, including hidden ones')

    def main(self):
        print_banner("Navigator")
        sh = local.session()

        while True:
            # add mkdir and touch here (new folder, new file)
            files = get_files()
            question = generate_question(files)
            answer = question.ask()
            print(answer)
            if (answer == "New file"):
                file_name = input("Input file name: ")
                sh.run("touch " + file_name)
            elif (answer == "New folder"):
                folder_name = input("Input folder name: ")
                sh.run("mkdir " + folder_name)
            else:
                sh.run("cd " + answer)

if __name__ == "__main__":
    Navigator()
