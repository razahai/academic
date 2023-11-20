import sys; args = sys.argv[1:]
idx = int(args[0])-50

# RE3 - undefined%
# absolute dog length

regex = [
    r"/\w*(\w)\w*\1\w*/i", # 50
    r"/\w*(\w)\w*(\1\w*){3}/i", # 51
    r"/^([01])([01]*\1)*$/", # 52
    r"/\b(?=\w*cat\w*)\w{6}\b/i", # 53
    r"/\b(?=\w*bri\w*)(?=\w*ing\w*)\w{5,9}\b/i", # 54
    r"/\b(?!\w*cat\w*)\w{6}\b/i", # 55
    r"/\b(?!\w*(\w)\w*\1\w*)\w+\b/i", # 56
    r"/^(1(?!0011)|0)*$/", # 57
    r"/\w*([aeiou])(?!\1)[aeiou]\w*/i", # 58
    r"/^(1(?!01|11)|0)*$/", # 59
]

if idx < len(regex):
    print(regex[idx])

