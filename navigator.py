from plumbum import cli, local
from plumbum.cmd import ls, mkdir, touch
from pyfiglet import Figlet
from questionary import prompt
import questionary 

def print_banner(text):
    print(Figlet(font='mini').renderText(text))


def get_files():
    files = ["New file", "New folder", "Quit", ".."]
    ls_output = ls() # how to include hidden files?
    files += ls_output.split("\n")
    return files


def generate_question(files):
    return questionary.rawselect(
        "Select the desired next location. Press ctrl+c to exit.",
        choices = [{'name': file} for file in files]
    )


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
            elif (answer == "Quit"):
                break
            else:
                try:
                    local.cwd.chdir(answer)
                except:
                    print("Failed to change directory!")


if __name__ == "__main__":
    Navigator()
