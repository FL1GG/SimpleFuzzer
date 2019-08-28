import urllib.request
import argparse
import sys
from time import sleep

parser = argparse.ArgumentParser()

parser.add_argument("url", help="The url you want to check with FUZZing, ex. http://this.com/page.php?id=FUZZ")
parser.add_argument("-t", "--test", help="get the default return of a webpage without arguments", action="store_true")
parser.add_argument("-w", "--wordlist", help="the wordlist to use while fuzzing")
parser.add_argument("-b", "--basetext", help="what the webpage looks like before adding arguments, use -t to get this")
parser.add_argument("-s", "--waitTime", help="amount of time in milliseconds to wait between requests")

args = parser.parse_args()

if(args.test):
    with urllib.request.urlopen(args.url) as response:
        html = response.read()
    print(html.strip())
    sys.exit(0)



wordlist = ["0"]
#set up the words
if(args.wordlist):
    print("[+] Setting Up Wordlist")
    wordsfile = open(args.wordlist, "r")

    for lines in wordsfile:
        word = lines.strip()
        wordlist.append(str(word))

print("[+] Starting FUZZ")
url = args.url
if(args.basetext):
    baseurl = args.basetext
else:
    urlConf = url.replace("FUZZ", "")
    with urllib.request.urlopen(urlConf) as response:
        html = response.read()
    baseurl = html

if(args.waitTime):
    waitTime = float(args.waitTime)/1000
else:
    waitTime = .001


#url management
for i in wordlist:

    #place the fuzz in the right place
    urlConf = url.replace("FUZZ", i)

    #get the url
    with urllib.request.urlopen(urlConf) as response:
        html = response.read()
    #check if it not the same as our current url.
    if(not(html == baseurl)):
        print(i)

    sleep(waitTime)
