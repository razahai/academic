import sys; args = sys.argv[1:]
import subprocess

def main():
    print(f"LOG: compiling current version of coins.cpp")
    subprocess.run(["/csl/users/--/cluster/cv/lab", "2/coins"])
    
    
    if len(args) >= 1 and args[0].lower() == "g":
        print(f"LOG: running all 100 coin grids...")
        log_file = open("coins_grid.log", "w")
        for i in range(100):
            filename = f"grid/case{str(i).zfill(4)}"
            print(f"COINS: running for grid {filename}")
            subprocess.call(["/csl/users/--/cluster/cv/mainlab", filename], stdout=log_file)
    else:
        print(f"LOG: running all 100 coin oogs...")
        log_file = open("coins_oog.log", "w")
        for i in range(100):
            filename = f"oog/case{str(i).zfill(4)}"
            print(f"COINS: running for oog {filename}")
            subprocess.call(["/csl/users/--/cluster/cv/mainlab", filename], stdout=log_file)
       

if __name__ == "__main__":
    main()
