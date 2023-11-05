
# Warmup - Logic - String - List
# $$$$^$$^^ - $^^^$^^ - $$^^$^ - ^$^^1$
# Lab2 - ~97.69%

# Warmup 2

def string_times(str, n):
   return str*n

def front_times(str, n):
   return str[:3]*n

def string_bits(str):
   return str[::2]  

def string_splosion(str):
   return "".join(str[:n] for n in range(len(str)+1))

def last2(str):
   return sum(str[n:n+2] == str[-2:] for n in range(len(str)-2))

def array_count9(nums):
  return nums.count(9)

def array_front9(nums):
   return 9 in nums[:4]

def array123(nums):
   return any(nums[n:n+3] == [1,2,3] for n in range(len(nums)-2))

def string_match(a, b):
   return sum(1 for n in range(len(a)-1) if a[n:n+2] == b[n:n+2])

# String 2

def double_char(str):
   return "".join(s*2 for s in str)

def count_hi(str):
  return str.count("hi")

def cat_dog(str):
   return str.count("cat") == str.count("dog")

def count_code(str):
   return sum(1 for n in range(len(str)) if str[n:n+2] == "co" and str[n+3:n+4] == "e")

def end_other(a, b):
   return a.lower()[-len(b):] == b.lower()[-len(a):]

def xyz_there(str):
   return str.replace(".xyz", " ").count("xyz") > 0

# List 2

def count_evens(nums):
   return sum(1 for n in nums if n % 2 == 0)

def big_diff(nums):
   return max(nums)-min(nums)

def centered_average(nums):
   return (sum(nums)-min(nums)-max(nums))//(len(nums)-2)

def sum13(nums):
   return sum(n for i, n in enumerate(nums) if n != 13 and (nums[i-1] != 13 or i == 0))

def sum67(nums):
   # loop nums.count(6) times: make nums[6idx:7idx]:=0
   return sum(n for i,n in enumerate(nums) if not ((7 in nums[:i] and 6 in nums[i-nums[i-1::-1].index(7):i+1] or (6 in nums[:i+1] and not 7 in nums[:i])) and 7 in nums[i:]))

def has22(nums):
   return any(True for n in range(len(nums)) if nums[n]==2 and (nums[n-1]==2 and n!=0))

# Logic 2

def make_bricks(small, big, goal):
   return goal-5*min(big,goal//5) <= small

def lone_sum(a, b, c):
   return sum(n for n in[a,b,c]if[a,b,c].count(n)==1)

def lucky_sum(a, b, c):
   return sum(n for i,n in enumerate([a,b,c]) if not 13 in [a,b,c][:i+1])

def no_teen_sum(a, b, c):
   return sum(n for n in [a,b,c] if (n < 13 or n > 19) or (n == 15 or n == 16)) 

def round_sum(a, b, c):
   return sum((n+5)//10*10 for n in (a,b,c))

def close_far(a, b, c):
   return ((abs(b-a)>1) ^ (abs(c-a)>1))*abs(b-c)>1

def make_chocolate(small, big, goal):
   return [-1, goal-5*min(big, goal//5)][goal-5*min(big,goal//5)<=small]


