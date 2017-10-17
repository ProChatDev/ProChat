import os
import os.path
import sys
import subprocess
import asyncio
from shutil import copyfile
import pip
import json

_requirement_files = ["gateway\\requirements.txt", "backend\\requirements.txt"]
requirement_files = []
for file in _requirement_files:
	requirement_files.append(os.getcwd() + "\\" + file)

_copyfiles = {
	"gateway\\config.json.example": "gateway\\config.json",
	"frontend\\config.json.example": "frontend\\config.json",
	"backend\\config.json.example": "backend\\config.json"
}
copyfiles = {}
for key, val in _copyfiles.items():
	key = os.getcwd() + "\\" + key
	val = os.getcwd() + "\\" + val
	copyfiles[key] = val

requirements = []

configfiles = copyfiles.values()

def load_config():
	path = "install-config.json"
	if not os.path.isfile(path):
		print("Creating default installer config")
		if not os.path.isfile("install-config.json.example"):
			print("Example install config missing, exiting...")
			exit("Could not load configuration")
		copyfile("install-config.json.example", path)
	return json.loads(open(path).read())

config = load_config()

def save_config():
	with open("install-config.json", 'w') as outfile:
	    json.dump(config, outfile, indent=4)

# If it isn't pretty, this will make it pretty, if its already pretty, this is useless
save_config()

for file in requirement_files:
	with open(file) as f:
		lines = f.read().splitlines()
		requirements.extend(lines)

async def install_pip_requirements(requirements):
	if not config.get("pip_install", True):
		print("Not running the backend+gateway dependencies installation, its disabled in install-config.json")
		return
	installed_pkgs = [pkg.key for pkg in pip.get_installed_distributions()]
	for requirement in requirements:
		if requirement in installed_pkgs:
			print('Requirement "{}" is already satisfied, not installing!'.format(requirement))
		else:
			print('Installing "{}"'.format(requirement))
			result = not bool(await pip_install(requirement))
			if not result:
				print("Failed to install {}: {}".format(requirement, result))
			else:
				print("Successfully installed {}: {}".format(requirement, result))
	config['pip_install'] = False
	save_config()

async def pip_install(name, *, timeout=None):
	# https://github.com/Cog-Creators/Red-DiscordBot/blob/develop/red.py#L186 thanks red, I modified it a little bit
	args = [
		"pip", "install",
		"--upgrade",
		name
	]
	return await execute_command(args, timeout)

async def npm_install():
	if not config.get("npm_install", True):
		print("Not running the frontend dependencies installation, its disabled in install-config.json")
		return
	try:
		print(await execute_command("(cd frontend && npm install)", shell=True))
	except Exception as e:
		print("Can't npm install", e)
	config['npm_install'] = False
	save_config()

CONSTANTS = {
	"mongo_key": "mongo_uri"
}

async def execute_command(command, timeout=None, shell=False):
	# https://github.com/Cog-Creators/Red-DiscordBot/blob/develop/red.py#L186 thanks red, I modified it a little bit
	def install():
		code = subprocess.call(command, shell=shell)
		sys.path_importer_cache = {}
		return code
	response = asyncio.get_event_loop().run_in_executor(None, install)
	return await asyncio.wait_for(response, timeout=timeout)

def copyFiles(files):
	if not config.get("configs", True):
		print("Not running the configs installation, its disabled in install-config.json")
		return
	for key, val in files.items():
		if os.path.isfile(val):
			print('File "{}" already exists, not copying'.format(val))
		else:
			print('Copying "{}" to "{}"'.format(key, val))
			copyfile(key, val)
	config['configs'] = False
	save_config()

def mongo_url():
	if not config.get("mongo", True):
		print("Not running the mongo url installation, its disabled in install-config.json")
		return
	url = input("What Mongo URI do you want to use?\n>")
	print(url)
	for file in configfiles:
		data = json.loads(open(file).read())
		data[CONSTANTS['mongo_key']] = url
		json.dump(data, open(file, "w"), indent=4)
	config['mongo'] = False
	save_config()

async def install():
	print("Installing frontend dependencies...")
	await npm_install()
	print("Installing backend+gateway dependencies...")
	await install_pip_requirements(requirements)
	print("Copying configuration files...")
	copyFiles(copyfiles)
	print("Setting Mongo URL...")
	mongo_url()


loop = asyncio.get_event_loop()  
loop.run_until_complete(install())  
loop.close()