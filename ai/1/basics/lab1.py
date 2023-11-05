
# * 9:48 EST to 11:28 EST 
# * Time Elapsed: 1h40m (kinda crazy)
# * All unmodified exercises were ran in codingbat and returned zero errors
# * Lab1 - 100%

# Warmup 1

def sleep_in(weekday, vacation):
   return not weekday or vacation

def monkey_trouble(a_smile, b_smile):
   return (a_smile and b_smile) or (not a_smile and not b_smile)

def sum_double(a, b):
   return a+b if a != b else (a+b)*2

def diff21(n):
   return abs(n-21) if n < 21 else 2*abs(n-21)

def parrot_trouble(talking, hour):
   return talking and (hour < 7 or hour > 20)

def makes10(a, b):
   return a + b == 10 or a == 10 or b == 10

def near_hundred(n):
   return abs(n-100) <= 10 or abs(n-200) <= 10

def pos_neg(a, b, negative):
   return (a < 0 and b < 0) if negative else ((a < 0 and b > 0) or (a > 0 and b < 0))

# String 1

def hello_name(name):
   return "Hello " + name + "!"

def make_abba(a, b):
   return a + b + b + a

def make_tags(tag, word):
   return "<" + tag + ">" + word + "</" + tag + ">"

# modified
def make_out_word(out, word): 
   return out[:len(out)//2] + word + out[len(out)//2:]

def extra_end(str):
   return str[-2:] + str[-2:] + str[-2:]

def first_two(str):
   return str[:2] if len(str) >= 2 else str

# modified
def first_half(str):
   return str[:len(str)//2]

def without_end(str):
   return str[1:-1]

# List 1

# modified
def first_last6(nums):
   return str(nums[0]) == "6" or str(nums[-1]) == "6"

# modified
def same_first_last(nums):
  return len(nums) >= 1 and (str(nums[0]) == str(nums[-1]))

# modified (heavy)
def make_pi(n):
   return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]

# modified
def common_end(a, b):
   return (str(a[0]) == str(b[0])) or (str(a[-1]) == str(b[-1]))

# modified
def sum3(nums):
   return sum(nums)

# modified
def rotate_left3(nums):
   return nums[1:] + [nums[0]] if len(nums) > 0 else nums

# modified
def reverse3(nums):
   return list(reversed(nums))

# modified
def max_end3(nums):
   return [nums[0]]*len(nums) if nums[0] > nums[-1] else [nums[-1]]*len(nums)

# Logic 1

def cigar_party(cigars, is_weekend):
   return True if cigars >= 40 and cigars <= 60 and not is_weekend else (True if cigars >= 40 and is_weekend else False)

def date_fashion(you, date):
   # precedence comes last in ternary 
   return 0 if you <= 2 or date <= 2 else (2 if you >= 8 or date >= 8 else 1)

def squirrel_play(temp, is_summer):
   return True if temp >= 60 and temp <= 90 and not is_summer else (True if temp >= 60 and temp <= 100 and is_summer else False)

def caught_speeding(speed, is_birthday):
   return 0 if speed <= 60 or (speed-5 <= 60 and is_birthday) else (1 if (speed >= 61 and speed <= 80) or ((speed-5 >= 61 and speed-5 <= 80) and is_birthday) else (2 if speed >= 81 or (speed-5 >= 81 and is_birthday) else -1))

def sorta_sum(a, b):
   return 20 if a+b >= 10 and a+b <= 19 else a+b

def alarm_clock(day, vacation):
   return "7:00" if day >= 1 and day <= 5 and not vacation else ("10:00" if (day < 1 or day > 5) and not vacation else ("10:00" if day >= 1 and day <= 5 and vacation else "off"))

def love6(a, b):
   return True if a == 6 or b == 6 else (True if a+b == 6 or abs(a-b) == 6 else False)

def in1to10(n, outside_mode):
   return True if (n <= 1 or n >= 10) and outside_mode else (True if n >= 1 and n <= 10 and not outside_mode else False) 
