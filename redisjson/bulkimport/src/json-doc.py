import os, json
from rejson import Client, Path

rj = Client(host='localhost', port=6379, decode_responses=True)
print("Connected to Redis")
base_directory = "../bulkdata/"
cnt = 0
for (dirpath, dirnames, filenames) in os.walk(base_directory):
    print("dirpath=" + dirpath)
    for file in filenames:
        # print("file=" + file)
        if ("json" in file):
            shortname = file.replace(".json", "")
            print("Here's the shortname" + shortname)
            openname = dirpath + "/" + file
            print("Here's the openname " + openname)
            data = json.loads(open(openname, "r").readline())
            print("data is ")
            print(data['data'])
            print("members are")
            print(data['data']['members'])
            for member in data['data']['members']:
                print("Here's the ID:", member['id'])
                memberIdInt = member['id']
                memberId = str(memberIdInt)
                memberIdFloat = float(memberIdInt)
                keyname="member:" + memberId
                idxKeyName="memberIndex:" + memberId
                zkeyname = "identifier:"
                #  can't use jsonset command because index not available but otherwise, this worked
                rj.jsonset(keyname, Path.rootPath(), member)
