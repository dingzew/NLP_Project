import re
import string

s = "Who's cup is this, and why?"
# = re.sub('\\w+', '', sentence)
s = re.findall(r'[\w.].*[\w.]', s)
print(s)