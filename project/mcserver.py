import subprocess
import os
from .fabric import fabric_main
from .vanilla import vanilla_main
from .forge import forge_main

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
        print("1. Fabric")
        print("2. Forge")
        print("3. Vanilla")
        print("4. Back to main menu")
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
                    print("Note: To create the server, run 'start.bat' in the server directory.")
                    input("Press Enter to leave...")
                    exit()
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
                        f.write(f"java -Xmx{minRam}M -Xms{maxRam}M -jar fabric-server.jar nogui")
                    
                    print("Server configured to use Fabric server.")
                    print("Note: To create the server, run 'start.bat' in the server directory.")
                    input("Press Enter to leave...")
                    exit()

            case '2':
                if bool:
                    createMCDR(path)
                    forge_main(path + "/server")
                    print("Modifying MCDR config to use Forge server...")
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
                            nuevo_contenido = contenido.replace("start_command: echo Hello world from MCDReforged", f"start_command: run.bat")
                            f.write(nuevo_contenido)
                        with open(os.path.join(path + "/server", "user_jvm_args.txt"), "w") as f:
                            f.write(f"-Xms{minRam}M -Xmx{maxRam}M")
                    print("Server configured to use Forge server and MCDR.")
                    print("Note: To create the server, run 'start.bat' in the server directory.")
                    input("Press Enter to leave...")
                    exit()

                else:
                    forge_main(path)
                    print("Modifying start.bat to use Forge server...")
                    print("Note: 1GB of RAM is 1024MB.")
                    print("Default values will be used if left blank.")
                    minRam = input("Minimun ram in MB (Example: 1024): ")
                    maxRam = input("Maximum ram in MG (Example: 2048): ")
                    if minRam == "":
                        minRam = "1024"
                    if maxRam == "":
                        maxRam = "1024"
                    with open(os.path.join(path, "start.bat"), "w") as f:
                        f.write(f"run.bat")
                    with open(os.path.join(path, "user_jvm_args.txt"), "w") as f:
                            f.write(f"-Xms{minRam}M -Xmx{maxRam}M")
                    print("Server configured to use Forge server.")
                    print("Note: To create the server, run 'start.bat' in the server directory.")
                    input("Press Enter to leave...")
                    exit()

            case '3':
                if bool:
                    createMCDR(path)
                    vanilla_main(path + "/server")
                    print("Modifying MCDR config to use Vanilla server...")
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
                    print("Note: To create the server, run 'start.bat' in the server directory.")
                    input("Press Enter to leave...")
                    exit()

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
                        f.write(f"java -Xmx{minRam}M -Xms{maxRam}M -jar server.jar nogui")
                    print("Server configured to use Vanilla server.")
                    print("Note: To create the server, run 'start.bat' in the server directory.")
                    input("Press Enter to leave...")
                    exit()
            
            case '4':
                return
            
            case _:
                print("Invalid choice. Please select 1, 2, or 3.")
                input("Press Enter to continue...")