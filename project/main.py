import os
from .mcserver import mcdr

def clear_screen():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        sys.exit("Unsupported OS for this script.")

def main():
    while True:
        clear_screen()
        print("Easy Minecraft server.")
        print("Select an option:")
        print("1. Use mcdr")
        print("2. Without mcdr")
        print("3. Exit")
        choice = input("Enter your choice: ")
        print()

        match (choice):
            case '1':
                clear_screen()
                print("Set path to mcdr:")
                print("Default is current directory.")
                path = input("Enter path (or press Enter for default): ")
                if path == "":
                    path = os.getcwd()
                mcdr(path, True)
            case '2':
                clear_screen()
                print("Set path to mcdr:")
                print("Default is current directory.")
                path = input("Enter path (or press Enter for default): ")
                if path == "":
                    path = os.getcwd()
                mcdr(path, False)
            case '3':
                exit("goodbye")
            case _:
                print("Invalid choice. Please select 1, 2, or 3.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    main()