
hash_tag = "#"

content = "sdf#inhash#sdsd"

def getHashTagContent(str):
    content = str
    first_hash_tag = -1
    second_hash_tag = -1
    for index,single in zip(range(0,len(content)),content):
        if single == "#":
            if first_hash_tag == -1:
                first_hash_tag = index
            else:
                second_hash_tag = index
                break
    if first_hash_tag == -1 or second_hash_tag==-1:
        return ""
    return content[first_hash_tag+1:second_hash_tag]
contents=["sfsd#fs是a#sdf","#sdfsdf#","sdfsf#sfsf#","1213#","#sdfsdf","123#sdfsdf#"]
for str in contents:
    result = getHashTagContent(str)
    print(result)
#print(content[first_hash_tag+1:second_hash_tag])
