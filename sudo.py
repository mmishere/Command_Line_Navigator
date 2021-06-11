from plumbum import cli
from pyfiglet import Figlet
from plumbum.cmd import sudo

def print_banner(text):
    print(Figlet(font='mini').renderText(text))



class SudoAllCommands(cli.Application):

    def main(self):
        print_banner("Sudo All Commands")

        while True:
            command = input("Input command: ")
            if (command == "quit"):
                break
            
            
            #  if input == quit, then close the application
            # elif input == valid command, do that

if __name__ == "__main__":
    SudoAllCommands()
