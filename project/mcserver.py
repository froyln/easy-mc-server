import subprocess
import os
from .fabric import fabric_main
from .vanilla import vanilla_main

def createMCDR(path):
    _ = os.system('cls')
    try:
        print("Checking for mcdreforged installation...")
        subprocess.run("mcdreforged --version", check=True)
    except:
        try:
            print("mcdreforged not found. Installing mcdreforged...")
            subprocess.run("pip install mcdreforged", check=True)
            print("mcdreforged installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install mcdreforged. Please install it manually.")
            exit(1)
    try: 
        os.chdir(path)
        subprocess.run("mcdreforged init", check=True)
        print("mcdreforged initialized successfully in " + path)

        #Crear el start.bat
        with open(os.path.join(path, "start.bat"), "w") as f:
            f.write("python -m mcdreforged\n")

        path = path + "/server"
    except:
        print("Failed to initialize mcdreforged in " + path)
        exit(1)

def mcdr(path, bool):
    while True:
        _ = os.system('cls')
        print("Select Minecraft server type.")
        print("1. fabric")
        print("2. vanilla")
        print("3. back to main menu")
        choice = input("Enter your choice: ")

        match (choice):
            case '1':
                if bool:
                    createMCDR(path)
                    fabric_main(path + "/server")
                    print("Modifying MCDR config to use Fabric server...")
                    print("Note: 1GB of RAM is 1024MB.")
                    print("Default values will be used if left blank.")
                    minRam = input("Minimun ram in MB (Example: 1024): ")
                    maxRam = input("Maximum ram in MG (Example: 2048): ")
                    if minRam == "":
                        minRam = "1024"
                    if maxRam == "":
                        maxRam = "1024"
                    with open(os.path.join(path, "config.yml"), "r") as f:
                        contenido = f.read()
                    if ("start_command: echo Hello world from MCDReforged" in contenido):
                        with open(os.path.join(path, "config.yml"), "w") as f:
                            nuevo_contenido = contenido.replace("start_command: echo Hello world from MCDReforged", f"start_command: java -Xmx{minRam}M -Xms{maxRam}M -jar fabric-server.jar nogui")
                            f.write(nuevo_contenido)
                    print("Server configured to use Fabric server and MCDR.")
                    input("Press Enter to leave...")
                    exit("Server configured to use Fabric server and MCDR.")
                else:
                    fabric_main(path)
                    print("Modifying start.bat to use Fabric server...")
                    print("Note: 1GB of RAM is 1024MB.")
                    print("Default values will be used if left blank.")
                    minRam = input("Minimun ram in MB (Example: 1024): ")
                    maxRam = input("Maximum ram in MG (Example: 2048): ")
                    if minRam == "":
                        minRam = "1024"
                    if maxRam == "":
                        maxRam = "1024"
                    with open(os.path.join(path, "start.bat"), "w") as f:
                        f.write("start_command: echo Hello world from MCDReforged", f"start_command: java -Xmx{minRam}M -Xms{maxRam}M -jar fabric-server.jar nogui")
                    
                    print("Server configured to use Fabric server.")
                    input("Press Enter to leave...")
                    exit("Server configured to use Fabric server.")
                    
            case '2':
                if bool:
                    createMCDR(path)
                    vanilla_main(path + "/server")
                    print("Modifying MCDR config to use Fabric server...")
                    print("Note: 1GB of RAM is 1024MB.")
                    print("Default values will be used if left blank.")
                    minRam = input("Minimun ram in MB (Example: 1024): ")
                    maxRam = input("Maximum ram in MG (Example: 2048): ")
                    if minRam == "":
                        minRam = "1024"
                    if maxRam == "":
                        maxRam = "1024"
                    with open(os.path.join(path, "config.yml"), "r") as f:
                        contenido = f.read()
                    if ("start_command: echo Hello world from MCDReforged" in contenido):
                        with open(os.path.join(path, "config.yml"), "w") as f:
                            nuevo_contenido = contenido.replace("start_command: echo Hello world from MCDReforged", f"start_command: java -Xmx{minRam}M -Xms{maxRam}M -jar server.jar nogui")
                            f.write(nuevo_contenido)
                    print("Server configured to use Vanilla server and MCDR.")
                    input("Press Enter to leave...")
                    exit("Server configured to use Vanilla server and MCDR.")

                else:
                    vanilla_main(path)
                    print("Modifying start.bat to use Vanilla server...")
                    print("Note: 1GB of RAM is 1024MB.")
                    print("Default values will be used if left blank.")
                    minRam = input("Minimun ram in MB (Example: 1024): ")
                    maxRam = input("Maximum ram in MG (Example: 2048): ")
                    if minRam == "":
                        minRam = "1024"
                    if maxRam == "":
                        maxRam = "1024"
                    with open(os.path.join(path, "start.bat"), "w") as f:
                        f.write("start_command: echo Hello world from MCDReforged", f"start_command: java -Xmx{minRam}M -Xms{maxRam}M -jar server.jar nogui")
                    print("Server configured to use Vanilla server.")
                    input("Press Enter to leave...")
                    exit("Server configured to use Vanilla server.")

            case '3':
                return
            
            case _:
                print("Invalid choice. Please select 1, 2, or 3.")
                input("Press Enter to continue...")