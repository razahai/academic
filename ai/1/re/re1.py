import sys; args = sys.argv[1:]
idx = int(args[0])-30

# * Length - 145 (min: 143)
# * RE1 - ~99%

regex = [
    r"/^10[01]$|^0$/",
    r"/^[01]*$/",
    r"/0$/",
    r"/\w*[aeiou]\w*[aeiou]\w*/i",
    r"/^0$|^1[01]*0$/",
    r"/^[01]*110[01]*$/",
    r"/^.{2,4}$/s", # /s
    r"/^\d{3} *-? *\d\d *-? *\d{4}$/",
    r"/^.*?d\w*/im", # i didn't realize it was matching from start to word
    r"/^0*$|^1*$|^0[01]*0$|^1[01]*1$/" 
]

if idx < len(regex):
    print(regex[idx])

