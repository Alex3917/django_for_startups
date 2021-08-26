import re
import subprocess  # nosec

RSTRIP_ROOT_DEPENDENCIES = re.compile(r"(#.*|=.*)")
RSTRIP_OUTDATED_PACKAGES = re.compile(r"\s.*")

with open("requirements.in") as f:
    possible_root_dependencies_list = f.read().splitlines()

root_dependencies_set = set()
for possible_root_dependency in possible_root_dependencies_list:
    stripped_line = RSTRIP_ROOT_DEPENDENCIES.sub("", possible_root_dependency)
    if stripped_line:
        root_dependency = stripped_line
        root_dependencies_set.add(root_dependency.casefold())

completed_process = subprocess.run(["pip", "list", "-o"], stdout=subprocess.PIPE)  # nosec
outdated_packages_str = completed_process.stdout.decode("utf-8")
outdated_packages_list = outdated_packages_str.splitlines()

for i, outdated_package in enumerate(outdated_packages_list, start=0):
    outdated_package_name = RSTRIP_OUTDATED_PACKAGES.sub("", outdated_package)
    if i <= 1:
        header_line = outdated_package_name
        print(header_line)
    elif outdated_package_name.casefold() in root_dependencies_set:
        outdated_root_package = outdated_package
        print(outdated_root_package)
