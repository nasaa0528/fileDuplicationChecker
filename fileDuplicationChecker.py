#!/usr/bin/python3 
import argparse, os, sys, logging, hashlib 
logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
def isDirExist(dirname): 
	""" Checks if the given folder exists and have read permission on that folder. If folder does not exists, then give error message with indication of error. Then stops the program """
	logging.debug('Checking if "{}" folder exists'.format(dirname))
	if (os.path.isdir(dirname)): 
		if (os.access(dirname, os.R_OK)): 
			logging.debug('SUCCESS: Directory exists and have read permission')
			return True 
		else: 
			print("{}: Read Permission Error. \nYou do not have read permission on {} folder, please check folder permission and try again".format(dirname, dirname))
			sys.exit() 
	else: 
		print("{} folder does not exist in your computer. Please check your folder name and try again".format(dirname))
		sys.exit()
		
def hashCalculator(filename): 
	BLOCK_SIZE = 65536
	file_hash = hashlib.md5()
	try:
		with open(filename, 'rb') as f: 
			fb = f.read(BLOCK_SIZE)
			while (len(fb) > 0): 
				file_hash.update(fb)
				fb = f.read(BLOCK_SIZE)
	except OSError: 
		print("ERROR: " + filename)
		return None
	else: 
		return str(file_hash.hexdigest())

# TODO: Default option 
## Traverse through given directory if provided one, or traverse in CWD 
## What to do with symbolic links 
def main(): 
	logging.debug('Creating argparses')
	parser = argparse.ArgumentParser(description='Finds file duplication in give directory')
	parser.add_argument('-d' ,'--directory', type=str, default='.', help='Either absolute or relative path of directory from which to check duplicated files.')
	args = parser.parse_args() 
	# if it did not specify other files, list of directories or did not enable disk options, then go to directory and check file traversals in given directory. Make changes when adding new features. 
	base_directory = args.directory 
	isDirExist(base_directory)
	no_read_permission = []
	duplication_dictionary = {}
	logging.debug('Traversing through the folder...')
	for dirname, subdirs, files in os.walk(base_directory): 
		for fname in files: 
			filename = os.path.join(dirname, fname)
			if os.access(filename, os.R_OK): 
				hash_result = hashCalculator(filename)
				if hash_result: 
					duplication_dictionary.setdefault(hash_result, []).append(filename)
					# print("HASH: {} in {}".format(hashCalculator(filename), filename))
					# duplication_dictionary[hash_result]
				else: 
					no_read_permission.append("Read error " + filename )
			else: 
				no_read_permission.append(filename) 
	logging.debug('Traversing done.')
	logging.debug('Files without read permission')
	# print("NO READ PERMISSION") 
	# for filename in no_read_permission:
		# print(filename)
	for k,v in duplication_dictionary.items(): 
		if len(v) > 1: 
			print("Duplicated files: ")
			for f in v: 
				print(f)
	logging.debug('Printing done')


## Calculate hash value on all files and create dictionary using key for hash and value with list of full paths on files 
## Print all files on which program doesn't have permission to read 
# TODO: Non default values 
## filter with size 
## filter with types 
# TODO: Get list of files or directories to check file duplication 
# TODO: Interactive delete option on file with option to read file with default option 
# TODO: Give filename and directory or list of directories to look for duplication of that specific file 
# TODO: Deep of folder to traverse... 
# TODO: Look for all duplication on given disk 

if __name__=='__main__': 
	logging.debug('Start of program')
	main()
	logging.debug('End of program')
