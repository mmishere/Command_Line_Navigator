from plumbum import cli, local
from plumbum.cmd import ls, mkdir, touch
from pyfiglet import Figlet
from questionary import prompt
import questionary 

import os

def print_banner(text):
    print(Figlet(font='mini').renderText(text))


def get_files():
    ls_output = ls() # how to include hidden folders?
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
            extra_options = ["Quit", "New file", "New folder", ".."]
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
