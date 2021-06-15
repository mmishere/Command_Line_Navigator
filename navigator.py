from plumbum import cli, local
from plumbum.cmd import ls, mkdir, touch
from pyfiglet import Figlet
from questionary import prompt
import questionary 

import os


# it can navigate through, but it seems it doesn't save that to the command line

def print_banner(text):
    print(Figlet(font='mini').renderText(text))


def get_files():
    ls_output = ls()
    files = [".."]
    files += ls_output.split("\n")
    return files

def get_files_all():
    ls_output = ls('-a')
    files = ls_output.split("\n")
    return files


def generate_question(filtered_folders):
    return questionary.rawselect(
        "Select the desired next location. Press ctrl+c to exit.",
        choices = [{'name': folder} for folder in filtered_folders]
    )

def filter_folders(unknown_file) -> bool:
    if os.path.isdir(unknown_file):
        return True
    return False

def filter_files(unknown_file) -> bool:
    if os.path.isfile(unknown_file):
        return True
    return False

class Navigator(cli.Application):
    VERSION = "1.0"
    all_flag = cli.Flag(['a', 'all'], help = 'List all files during navigation, including hidden ones')

    def main(self):
        print_banner("Navigator")
        sh = local.session()

        while True:
            extra_options = ["QUIT", "NEW FILE", "NEW FOLDER"]
            all_files = ""
            if self.all_flag:
                all_files = get_files_all()
            else:
                all_files = get_files()
            filtered_folders = filter(filter_folders, all_files)
            options = extra_options
            for folder in filtered_folders:
                options.append(folder)
            

            filtered_files = filter(filter_files, all_files)
            print("FILES:")
            for file in filtered_files:
                print(file)
            print("-----------")
            
            question = generate_question(options)
            answer = question.ask()

            if (answer == "NEW FILE"):
                file_name = input("Input file name: ")
                sh.run("touch " + file_name)

            elif (answer == "NEW FOLDER"):
                folder_name = input("Input folder name: ")
                sh.run("mkdir " + folder_name)

            elif (answer == "QUIT"):
                break

            else:
                try:
                    # local.cwd.chdir(answer)
                    # sh.run("cd " + answer)
                    os.chdir(answer)
                except:
                    print("FAILED TO CHANGE DIRECTORY\n----------------")


if __name__ == "__main__":
    Navigator()
