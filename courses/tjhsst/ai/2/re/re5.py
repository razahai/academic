import sys; args = sys.argv[1:]
idx = int(args[0])-70

# RE5 - 90%
# target length is 246 - current 391

regex = [
    r"/^(?=.*a)(?=.*e)(?=.*i)(?=.*o)(?=.*u)[a-z]+$/m", # 70
    r"/^([b-df-hj-np-tv-z]*[aeiou][b-df-hj-np-tv-z]*){5}$/m", # 71
    r"/^[a-z]*[b-df-hj-np-tvxz]w(?![aeiou][rh]|[rh][aeiou])[b-df-hj-np-tvxz][a-z]*$/m", # 72 (^[a-z]*[b-df-hj-np-tvxz]w(?![aeiou](r|h)|(r|h)[aeiou])[b-df-hj-np-tvxz][a-z]*$)
    r"/^([a-z])(([a-z])(([a-z])[a-z]*\5|[a-z]?)\3|[a-z]?)\1$|^a$/m", # 73 (^([a-z])([a-z])([a-z])[a-z]*\3\2\1$|^([a-z])[a-z]\4$|^([a-z])([a-z])[a-z]?\6\5$|^([a-z])\7$|^a$)
    r"/^[ac-su-z]*(tb|bt)[ac-su-z]*$/m", # 74
    r"/^[a-z]*(.)\1[a-z]*$/m", # 75
    r"/^(?=.*(.)(.*\1.*){5})[a-z]*$/m", # 76
    r"/^[a-z]*((.)\2){3}[a-z]*$/m", # 77
    r"/^([aeiou]*[b-df-hj-np-tv-z]){13}[aeiou]*$/m", # 78
    r"/^(([a-z])(?!.*\2.*\2))*$/m"  # 79
]

if idx < len(regex):
    print(regex[idx])

