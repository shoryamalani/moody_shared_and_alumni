#We have to make a system which allows us to login to our account or we can make a new username and password 
#Our username should be stored as a class with attributes such as height, weight, age, etc............
import json

user=None

class user:
  def __init__(self,username):
    self.username = username
 
def process(data):
  values_wanted=["create account","login","exit","logout","age","weight","nickname","height"]
  if data in values_wanted:
    return data
  else:
    return None

def process_data(data):
  if data == "login":
    pass
  elif data == "exit":
    return True

def recieve_input():
  data_in = True
  while data_in:
    recieve_data = input("What would you like to do: ")
    return_data = process(recieve_data)
    if return_data:
      data_in = False
      end = process_data(recieve_data)
      if end:
        return False
      else:
        return True 


  
  


def loop():
  if_looping_ended = True
  while if_looping_ended:
    if_looping_ended = recieve_input()
    




def main():
  loop()

if __name__ == '__main__':
  main()

