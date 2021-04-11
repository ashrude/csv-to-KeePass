import csv
from pykeepass import PyKeePass
import sys
import pykeepass as pky

input_file = ''
output_file = ''
password = ''

REMOVE_URL = ["http://", "https://", "www.", ".com", ".ca", ".us", ".org", '.cg', '.cs', '.nz', '.lv', '.gw', '.ke', '.pw', '.info', '.kg', '.cl', '.co', '.jobs', '.se', '.tl', '.gd', '.ck', '.gm', '.cc', '.ni', '.mn', '.gh', '.na', '.so', '.uz', '.org', '.jo', '.cz', '.ki', '.aero', '.ug', '.museum', '.dk', '.mz', '.nf', '.th', '.ph', '.hn', '.gg', '.sg', '.za', '.pg', '.hu', '.ge', '.uk', '.bd', '.np', '.er', '.ro', '.pt', '.yt', '.be', '.aq', '.tm', '.bn', '.ag', '.lr', '.tn', '.my', '.fo', '.tg', '.bf', '.es', '.jm', '.tv', '.gn', '.it', '.ee', '.rw', '.bm', '.km', '.bg', '.as', '.gf', '.re', '.bi', '.br', '.com', '.mk', '.ar', '.sz', '.int', '.mt', '.ye', '.pn', '.tf', '.mw', '.mobi', '.ga', '.tr', '.ao', '.sv', '.li', '.bt', '.ch', '.bv', '.ky', '.fi', '.nr', '.ir', '.travel', '.fj', '.st', '.pk', '.sn', '.uy', '.ng', '.vn', '.vu', '.mv', '.pm', '.mq', '.tj', '.hk', '.mx', '.gs', '.dj', '.ml', '.cv', '.bh', '.ec', '.ae', '.cr', '.wf', '.cat', '.tk', '.kw', '.is', '.aw', '.pl', '.um', '.si', '.je', '.gb', '.kz', '.fr', '.gl', '.mc', '.arpa', '.sm', '.mp', '.at', '.im', '.lt', '.ru', '.mil', '.lc', '.il', '.gy', '.af', '.ba', '.ne', '.lk', '.nl', '.eu', '.eg', '.cm', '.ls', '.by', '.edu', '.va', '.net', '.yu', '.web', '.id', '.to', '.name', '.iq', '.et', '.fm', '.us', '.cy', '.in', '.pf', '.bj', '.firm', '.nc', '.py', '.ly', '.ax', '.sy', '.bo', '.eh', '.no', '.gov', '.lu', '.tc', '.fk', '.pa', '.gt', '.sh', '.sa', '.ca', '.kr', '.bw', '.mo', '.sr', '.vg', '.bs', '.az', '.mr', '.vi', '.ma', '.kn', '.mg', '.vc', '.gr', '.ps', '.mh', '.nato', '.cx', '.bz', '.cn', '.sj', '.sd', '.al', '.pe', '.qa', '.ai', '.zm', '.nu', '.dm', '.ws', '.ad', '.coop', '.ie', '.tz', '.td', '.sk', '.de', '.ms', '.jp', '.tw', '.dz', '.ve', '.au', '.kp', '.tp', '.kh', '.cu', '.do', '.gu', '.store', '.am', '.bb', '.an', '.mu', '.hm', '.gp', '.sb', '.ht', '.ua', '.mm', '.la', '.sl', '.biz', '.pr', '.om', '.cd', '.lb', '.gi', '.sc', '.zw', '.ac', '.io', '.cf', '.ci', '.pro', '.tt', '.gq', '.md', '.hr']

taken_names = []

def check_duplicates(title):
    #please dont look at this, its probobly horrible
    if taken_names.count(title) != 0:
        i = 1
        working_title = f"{title}-1"
        while taken_names.count(working_title) != 0:
            working_title = f"{title}-{i}"
            i+=1
        taken_names.append(working_title)
        return working_title
    else:
        taken_names.append(title)
        return title

def get_name(url):
    for rule in REMOVE_URL:
        url = url.replace(rule, '')
    for char in url:
        if char == ":":
            url = url.split(":")[0]
    #check for duplicates
    url = check_duplicates(url)
    return url

def parse_data(reader):
    data = []
    for row in reader:
        current = []
        needed = [0,1,2]
        for i in needed:
            current.append(row[i])
        data.append(current)
    return data

def help():
    print(f"{sys.argv[0]} is a script to convert .csv files from firefox to .kdbx files for use in other applications.\nexample usage: python3 {sys.argv[0]} inputfile outputfile password")
    exit()

if len(sys.argv) == 1 or sys.argv[1] == "--help" or len(sys.argv) != 4:
    help()
else:
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        password = sys.argv[3]
    except:
        help()

try:
    open(input_file)
except:
    help()

try:
    open(output_file)
except:
    pky.create_database(output_file, password=password)
    

logins = csv.reader(open(input_file), delimiter=',')

kp = PyKeePass(output_file, password=password)

entries = parse_data(logins)

for entry in entries:
    kp.add_entry(kp.root_group, get_name(entry[0]), entry[1], entry[2], url=entry[0])

kp.save()