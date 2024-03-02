import sys; args = sys.argv[1:]
idx = int(args[0])-60

# RE4 - 96% ish
# target length is 253  }
# current length is 280 } 27 chars - need to get <20 chars

regex = [
    r"/^(0(?!10)|1)*$/", # 60, ac
    r"/^(1(?!01)|0(?!10))*$/", # 61, ac
    r"/^(0|1)([01]*\1)?$/", # 62, wa; 3 chars
    r"/\b((\w)(?!\w*\2\b))+\b/i", # 63, wa; 1 char
    r"/\w*(\w)(?=\w*\1)(\w*(?!\1)(\w)\w*\3|(\w*\1){3})\w*/i", # 64, rml; 7 chars
    r"/\b(?=(\w)*\w*\1\w*\1)((\w)(?!\w*\3)|\1)+\b/i", # 65, ac
    r"/\b(?!\w*([aeiou])\w*\1)(\w*[aeiou]){5}\w*/i", # 66, wa; 2 chars
    r"/^(?=1*0(1|01*0)*$)(0|10*1)*$/", # 67, rml; 6 chars
    r"/^((1(01*0)*10*)+|0)$/", # 68, wa; 1 char
    r"/^(?!(1(01*0)*1|0)+$)[01]+$/", # 69, rml; 7 chars
]

if idx < len(regex):
    print(regex[idx])

