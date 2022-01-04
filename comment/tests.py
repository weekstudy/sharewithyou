from django.test import TestCase

# Create your tests here.


import emoji
with open('emoji.txt','r') as f:
    lines = f.readlines()

for line in lines:

    print("'"+emoji.demojize(line.strip())+"'", end=',')

