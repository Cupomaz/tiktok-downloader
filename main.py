import downloader
import sys
import requests

if len(sys.argv) == 1:
    print("Usage: python main.py URL OUTPUT_FILE_NAME")
    print("Video is always downloaded as mp4")
    exit()

if len(sys.argv) > 3:
    print("Too many arguments")
    exit()

invalidChar = ["\\","/",":","*","?","\"","<",">","|"]

for char in invalidChar:
    if char in sys.argv[2]:
        print("Filename cannot contain these characters \\ / : * ? \" < > |")
        exit()

try:
    file = downloader.downloadVideo(sys.argv[1])
except requests.exceptions.MissingSchema:
    print("Invalid URL")
    exit()


open("{}.mp4".format(sys.argv[2]), "wb").write(file.content)