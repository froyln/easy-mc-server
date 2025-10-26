import requests
import os

MAIN_MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

def vanilla_main(path):
    #Version selection
    _ = os.system('cls')
    print("Vanilla server selected.")
    print("Select Minecraft version.")
    response = requests.get(MAIN_MANIFEST_URL)
    versions = response.json()['versions']
    version_list = [v['id'] for v in versions if v['type'] == 'release']
    choice = input(f"Enter your version (Default is the latest version: {version_list[0]}): ")
    if choice == "":
        choice = version_list[0]
    elif choice not in version_list:
        print("Invalid version selected.")
        input("Press Enter to continue...")
        return
    selected_version = choice
    print(f"Versión de MC seleccionada: {selected_version}")
    print()
    print(f"Downloading Vanilla Minecraft server version {selected_version}...")
    version_data = next(v for v in versions if v['id'] == selected_version)
    server_url = version_data['url']
    server_info = requests.get(server_url).json()
    download_url = server_info['downloads']['server']['url']
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        server_jar_path = os.path.join(path, "server.jar")
        with open(server_jar_path, 'wb') as f:
            f.write(response.content)
        print(f"Vanilla Minecraft server version {selected_version} downloaded successfully.")
    except Exception as e:
        print(f"Failed to download Vanilla Minecraft server: {e}")
        input("Press Enter to continue...")

    #Aceptar el EULA
    eula_path = os.path.join(path, "eula.txt")
    with open(eula_path, "w") as f:
        f.write("eula=true\n")
    print("EULA accepted.")
    input("Press Enter to continue...")
    _ = os.system('cls')