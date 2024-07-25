import subprocess

# Open and read the requirements.txt file
with open('requirements.txt', 'r') as file:
    packages = file.readlines()

# Remove newline characters from each package name
packages = [package.strip() for package in packages]

# Uninstall each package
for package in packages:
    subprocess.check_call(["pip", "uninstall", "-y", package])