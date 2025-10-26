def main():
    print("This is a test file.")
    java_version = "java 21.0.0"
    java_version = java_version.split()
    java_version = java_version[1]
    java_version = int(java_version.split(".")[0])
    print(f"Java major version: {java_version}")

main()