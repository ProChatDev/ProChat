import os
import os.path
import sys
import subprocess
import asyncio
from shutil import copyfile
import pip

_requirement_files = ["gateway\\requirements.txt", "backend\\requirements.txt", "database\\requirements.txt"]
requirement_files = []
for file in _requirement_files:
	requirement_files.append(os.getcwd() + "\\" + file)

_copyfiles = {
	"gateway\\config.json.example": "gateway\\config.json",
	"frontend\\config.json.example": "frontend\\config.json",
	"backend\\config.json.example": "backend\\config.json",
	"database\\config.json.example": "database\\config.json"
}
copyfiles = {}
for key, val in _copyfiles.items():
	key = os.getcwd() + "\\" + key
	val = os.getcwd() + "\\" + val
	copyfiles[key] = val

requirements = []

for file in requirement_files:
	with open(file) as f:
		lines = f.read().splitlines()
		requirements.extend(lines)

async def install_pip_requirements(requirements):
	installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]
	for requirement in requirements:
		if requirement in installed_pkgs:
			print("Requirement \"{}\" is already satisfied, not installing!".format(requirement))
		else:
			print("Installing \"{}\"".format(requirement))
			result = await pip_install(requirement)
			if not result:
				print("Failed to install {}: {}".format(requirement, result))
			else:
				print("Successfully installed {}: {}".format(requirement, result))

async def pip_install(name, *, timeout=None):
	# https://github.com/Cog-Creators/Red-DiscordBot/blob/develop/red.py#L186 thanks red, I modified it a little bit
    args = [
        "pip", "install",
        "--upgrade",
        name
    ]
    def install():
        code = subprocess.call(args)
        sys.path_importer_cache = {}
        return not bool(code)
    response = asyncio.get_event_loop().run_in_executor(None, install)
    return await asyncio.wait_for(response, timeout=timeout)

def copyFiles(files):
	for key, val in files.items():
		if os.path.isfile(val):
			print("File \"{}\" already exists, not copying".format(val))
		else:
			print("Copying \"{}\" to \"{}\"".format(key, val))
			copyfile(key, val)

copyFiles(copyfiles)

loop = asyncio.get_event_loop()  
loop.run_until_complete(install_pip_requirements(requirements))  
loop.close()  