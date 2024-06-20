import sys; args = sys.argv[1:]
idx = int(args[0])-40

# * Length - 214 (min: 180)
# * RE2 - 95.7%

regex = [
    r"/^[x.o]{64}$/i", # 40, ac
    r"/^[xo]*\.[xo]*$/i", # 41, ac
    r"/^\.|^x+o*\.|\.$|\.o*x+$/i", # 42, ac
    r"/^.(..)*$/s", # 43, ac
    r"/^(0|1[01])([01]{2})*$/", # 44, ac?
    r"/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i", # 45, ac
    r"/^[01]?(0|010|01)*1?$/", # 46, ac?
    r"/^([bc]+a?|a)[bc]*$/", # 47, rml? 
    r"/^(([bc]*a){2}[bc]*)+$|^[bc]+$/", # 48, rml?
    r"/^(2[02]*|(1[02]*){2})+$/" # 49, alm ac
]

if idx < len(regex):
    print(regex[idx])

