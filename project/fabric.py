import os
import requests
import urllib.request
import subprocess

API_GAME = "https://meta.fabricmc.net/v2/versions/game"
API_LOADER = "https://meta.fabricmc.net/v2/versions/loader"
API_INSTALLER = "https://meta.fabricmc.net/v2/versions/installer"

def fabric_main(path):
    game_versions = [v['version'] for v in requests.get(API_GAME).json() if v['stable']]
    loader_versions = [v['version'] for v in requests.get(API_LOADER).json() if v['stable']]
    installer_versions = [v['version'] for v in requests.get(API_INSTALLER).json() if v['stable']]

    #Version selection
    _ = os.system('cls')
    print("Fabric server selected.")
    print("Select Minecraft version.")
    choice = input(f"Enter your version (Default is the latest version: {game_versions[0]}): ")
    if choice == "":
        choice = game_versions[0]
    elif choice not in game_versions:
        print("Invalid version selected.")
        input("Press Enter to continue...")
        return
    selected_game = choice
    print(f"Versión de MC seleccionada: {selected_game}")
    print()

    #Loader selection
    _ = os.system('cls')
    print("Select Fabric Loader version.")
    print("Available versions:")
    for v in loader_versions:
        print(f"- {v}")
    choice = input(f"Enter your version (Default is the latest version: {loader_versions[0]}): ")
    if choice == "":
        choice = loader_versions[0]
    elif choice not in loader_versions:
        print("Invalid version selected.")
        input("Press Enter to continue...")
        return
    selected_loader = choice
    print(f"Versión de Fabric Loader seleccionada: {selected_loader}")
    print()
    
    #Installer selection
    _ = os.system('cls')
    print("Select Fabric Installer version.")
    print("Available versions:")
    for v in installer_versions:
        print(f"- {v}")
    choice = input(f"Enter your version (Default is the latest version: {installer_versions[0]}): ")
    if choice == "":
        choice = installer_versions[0]
    elif choice not in installer_versions:
        print("Invalid version selected.")
        input("Press Enter to continue...")
        return
    selected_installer = choice
    print(f"Downloading Fabric Installer version {selected_installer}...")
    print()

    #Download installer
    try:
        #Descargar el instalador
        _ = os.system('cls')
        download_url = f"https://meta.fabricmc.net/v2/versions/loader/{selected_game}/{selected_loader}/{selected_installer}/server/jar"
        urllib.request.urlretrieve(download_url, os.path.join(path, "fabric-server.jar"))
        print("Download completed.")
        print(f"Fabric server setup completed in {path}.")

        #Iniciar el instalador
        os.chdir(path)
        subprocess.run(f'java -jar fabric-server.jar nogui', check=True)

        #Aceptar el eula automáticamente, reescribiendo el archivo
        with open(os.path.join(path, "eula.txt"), "w") as f:
            f.write("eula=true\n")
            print("EULA accepted.")
        
        #clear screen
        _ = os.system('cls')
    except:
        print("Failed to get Fabric URL.")
        input("Press Enter to continue...")
        exit(1)
    