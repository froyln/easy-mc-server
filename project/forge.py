import os
import requests
import subprocess

FORGE_API_URL = "https://files.minecraftforge.net/net/minecraftforge/forge/promotions_slim.json"

def forge_main(path):
    print("Forge server selected.")

    #Extract available versions
    response = requests.get(FORGE_API_URL)
    data = response.json()
    versions = data['promos']
    forge_versions = [key for key in versions.keys() if key.endswith("-recommended")]

    #Version selection
    _ = os.system('cls')
    print("Select Minecraft version.")
    version = input("Enter your version (Default is lasted): ")
    if version == "":
        version = sorted(forge_versions)[-1].replace("-recommended", "")
    elif not any(version in v for v in forge_versions):
        print("Invalid version selected.")
        input("Press Enter to continue...")
        return
    
    if version + "-recommended" in versions:
        forge_version = versions[version + "-recommended"]
    
    print(f"Downloading Forge Minecraft server version {version}-{forge_version}...")
    download_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{forge_version}/forge-{version}-{forge_version}-installer.jar"
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        server_jar_path = os.path.join(path, "forge-installer.jar")
        with open(server_jar_path, 'wb') as f:
            f.write(response.content)
        print(f"Forge Minecraft server version {version}-{forge_version} downloaded successfully.")
    except:
        print(f"Failed to download Forge Minecraft server version {version}-{forge_version}.")
        input("Press Enter to continue...")
        exit(1)

    #Run installer
    try:
        os.chdir(path)
        subprocess.run(f'java -jar forge-installer.jar --installServer', check=True)
        print("Forge server installed successfully.")
        input("Press Enter to continue...")
    except:
        print("Failed to run Forge installer. Please ensure Java is installed correctly.")
        input("Press Enter to continue...")
        exit(1)
    
    #Aceptar el eula automáticamente, reescribiendo el archivo
    with open(os.path.join(path, "eula.txt"), "w") as f:
        f.write("eula=true\n")
        print("EULA accepted.")
        
    #clear screen
    _ = os.system('cls')