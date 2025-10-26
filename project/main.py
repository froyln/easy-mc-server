import os
import subprocess
from .mcserver import mcdr

def check_dependencies():
    clear_screen()
    try:
        subprocess.run("java --version", check=True)
    except subprocess.CalledProcessError:
        print("Java is not installed. Please install Java to continue.")
        print("You can download it from https://www.java.com/en/download/")
        print("After installing Java, please restart this program.")
        input("Press Enter to exit...")
        exit("Java is not installed. Please install Java to continue.")

    clear_screen()
    try:
        subprocess.run("python --version", check=True)
    except subprocess.CalledProcessError:
        print("Python is not installed. Please install Python to continue.")
        print("You can download it from https://www.python.org/downloads/")
        print("After installing Python, please restart this program.")
        input("Press Enter to exit...")
        exit("Python is not installed. Please install Python to continue.")

    clear_screen()
    try:
        subprocess.run("pip --version", check=True)
    except subprocess.CalledProcessError:
        print("Pip is not installed. Please install Pip to continue.")
        print("You can find instructions at https://pip.pypa.io/en/stable/installation/")
        print("After installing Pip, please restart this program.")
        input("Press Enter to exit...")
        exit("Pip is not installed. Please install Pip to continue.")

    clear_screen()
    try: 
        java_version_output = subprocess.check_output("java --version", shell=True, text=True)
        java_version = java_version_output.splitlines()[0]
        java_version = java_version.split()
        java_version = java_version[1]
        java_version = int(java_version.split(".")[0])
        if java_version < 21:
            print("Java version 21 or higher is required. Please update your Java installation.")
            print("You can download the latest version from https://www.java.com/en/download/")
            print("After updating Java, please restart this program.")
            input("Press Enter to exit...")
            exit("Java version 21 or higher is required. Please update your Java installation.")
    except:
        print("Failed to determine Java version. Please ensure Java is installed correctly.")
        input("Press Enter to exit...")
        clear_screen()
        exit("Failed to determine Java version. Please ensure Java is installed correctly.")


def clear_screen():
    # Check the operating system
    if os.name == 'nt':  # For Windows
        _ = os.system('cls')
    else:  # For macOS and Linux
        sys.exit("Unsupported OS for this script.")

def main():
    check_dependencies()
    
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