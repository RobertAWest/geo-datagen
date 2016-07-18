# Copyright (c) 2016 Ravind Kumar, MongoDB Inc.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os
import sys
import random
import json
import getopt

#Global Declarations

   # This global indicates the program should create unique values 
   # This affects the following functions:
   # * generate_business_email()
   # * generate_phone_number()

make_unique = False

   # These globals are used in generate_business_email()
   # and allow for creation of unique emails 

email = set()

   # These globals are used in generate_phone_number()
   # and allow for creation of unique phone numbers by removing
   # an entry once it is chosen
phone_number = set()

def generate_categories():
   
   categories = []
   
   with open('categories.txt') as f:
      categories_list = f.read().splitlines()
   
   for x in range (0, random.randint(1,3)):
      categories.append(random.choice(categories_list))
      
   return categories

def generate_business_name():
   prefix = ""
   adjective = ""
   suffix = ""
   
   with open('prefix.txt') as f:
      prefix = f.read().splitlines()
      f.close()
      
   with open('adjective.txt') as f:
      adjective = f.read().splitlines()
      f.close()
      
   with open("suffix.txt") as f:
      suffix = f.read().splitlines()
      f.close()
      
   return random.choice(prefix) \
          + "'s " \
          + random.choice(adjective) \
          + " " \
          + random.choice(suffix)

def generate_business_owner():

   fname = ""
   lname = ""
   

   with open('fnames.txt') as f:
      fname = f.read().splitlines()
      f.close()
   
   with open('lnames.txt') as f:
      lname = f.read().splitlines()
      f.close()
      
   return random.choice(fname).lower() + " " + random.choice(lname).lower()
   
   
def generate_business_email(name):
   
   global email
   global make_unique

   name = name.replace(" ","")
   name = name.replace("'","")
   name = name.lower()
   
   domains = ["example.net","example.org","example.com"]
   
   domain = random.choice(domains)
   
   if make_unique == True:
   
      
      i = 1
      while name + "@" + domain in email:
         name = name + str(i)
         i = i+1
         
   email.add(name + "@" + domain)
   
   return name + "@" + domain
   
def generate_phone_number():

   excluded = [555,600,844,855,866,877,888]

   area = random.randint(111,999)
   while area in excluded:
      area = random.randint(111,999)
   
   global make_unique
   
   if make_unique == False:
      return str(area) \
             + '-555-0' \
             + str(random.randint(100,199))
   else:
      global phone_number
      
      num = str(area) + '-555-0' + str(random.randint(100,199))
      
      while num in phone_number:
         area = random.randint(111,999)
         while area in excluded:
            area = random.randint(111,999)
         num = str(area) + '-555-0' + str(random.randint(100,199))
      phone_number.add(num)
      return num
          
def generate_date():          
   y = random.choice(["2014","2015","2016"])
   m = random.choice(["01","02","03","04","05","06","07","08","09","10","11","12"])
   d = ""
   if m in ["01","03","05","07","08","10","12"]:
      d = random.randint(1,31)
   elif m in ["02"]:
      d = random.randint(1,28)
   else:
      d = random.randint(1,30)
      
   if d < 10:
      d = "0" + str(d)
   else:
      d = str(d)
      
   return y + "-" + m + "-" + d + "T09:00:00.000-02:00"

def generate_health_grades():

   grades = []
   
   for x in range (0,3):
      chance = random.random()
      score = ""
      if chance < 0.35:
         score = "A"
      elif chance >=0.35 and chance <0.75:
         score = "B"
      elif chance >= 0.75 and chance < 90:
         score = "C"
      else:
         score = "F"
      
      date = {"$date" : generate_date()}
      
      grade = {
         "score" : score,
         "date" : date
      }
      
      grades.append(grade)
   
   return grades

def generate_long_lat():

   longitude = random.uniform(-40,-35)
   latitude = random.uniform(30,35)
   
   location = [longitude, latitude]
   
   return location
   
def generate_restaurant():
   owner = generate_business_owner()
   contact = {
      "owner" : owner,
      "email" : generate_business_email(owner),
      "phone" : generate_phone_number()
   }

   doc = {
      "restaurant_name" : generate_business_name(),
      "cuisine" : generate_categories(),
      "grades" : generate_health_grades(),
      "contact" : contact,
      "location" : generate_long_lat()
   }

   return json.dumps(doc)
   
   
# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
## Thanks to brian-khuu at stack overflow for this code
## http://stackoverflow.com/a/15860757  

def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + \
                                               "-"*(barLength-block), 
                                               round(progress*100,1), 
                                               status
                                             )
    sys.stdout.write(text)
    sys.stdout.flush()



def main(argv):

   limit = 100
   
   try:
      opts, args = getopt.getopt(argv,"hl:du",["limit=","delete","unique"])
   except getopt.GetoptError, exc:
      print exc.msg
      print "geo_datagen.py -l <limit> -d -u"
      sys.exit(2)
      
   for opt, arg in opts:
      if opt == "-h":
         print "geo_datagen.py -l <int> -d"
         print "-l | --limit \n" + \
               "\t The number of restaurants to generate. \n" + \
               "\t Currently supports up to 88,000 documents."
         print "-d | delete \n" + \
               "\t Deletes the restaurants.json file" + \
               "if it already exists"
         print "-u | unique : \n " + \
               "\t Generates unique business owner and \n" + \
               "\t phone numbers. Also results in unique e-mail fields. \n" + \
               "\t Note that this option may result in longer run time \n" + \
               "\t and increased memory usage, especially with large \n" + \
               "\t values of -l. \n" + \
               "\t Setting this to true implies 'd | --delete'"
         print "\n geo_datagen.py creates a number of randomly generated \n" + \
               "restaurants for use with the MongoDB mongoimport tool, \n" + \
               "outputting the result to the restaurants.json file"
         sys.exit()
      elif opt in ("-l", "--limit"):
         print ("Setting limit to " + arg)
         limit = int(arg)
      elif opt in ("-d","--delete"):
         print ("Removing restaurants.json")
         os.remove('restaurants.json')
      elif opt in ("-u","--unique"):
         print ("Preparing Uniques")
         global make_unique
         make_unique = True
         print ("Removing restaurants.json")
         os.remove('restaurants.json')
   
   if make_unique == True:
      if limit > 88000:
         print ("`-u | --unique` only supports up to 88,000 unique documents")
         limit = 88000
   
   print "Creating " + str(limit) + " restaurants"
   
   with open ('restaurants.json', 'a') as myfile:
      for x in range (0,limit):
         myfile.write(generate_restaurant() + "\n")
         update_progress(float(x) / float(limit))
      update_progress(1)
   
      myfile.close()
   
   
if __name__ == "__main__":
   sys.exit(main(sys.argv[1:]))