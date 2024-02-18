from collections import UserDict
from dataclasses import dataclass
import os  
import json

def log_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return print(str(e))
    return inner

class Name():
    def __init__(self, name):
        if not name:
            raise Exception("Name is required")
        self.name = name

class Phone():
      def __init__(self,phone):
        if not phone:
            raise Exception("Name is required")
        if len(phone) < 10:
            raise Exception("Phone number is too short")
        self.phone = phone
        
     
class Record(UserDict):
    __current_directory = os.getcwd()
    __contacts_file = "contacts.txt"
    def addName(self, name):
        self.name = Name(name).name

    def addPhone(self, phone):
        self.phone = Phone(phone).phone
    
    def get_users(self)->list:
        if not os.path.exists(self.get_file_path(self.__contacts_file)):
            return []
        try:
            with open(self.get_file_path(self.__contacts_file), "r") as file:
                users = file.read()
                if not users:
                    return []
                return json.loads(users)
        except FileNotFoundError :
            raise Exception("File not found!")  

    def get_file_path(self,file_name: str)->str:
        return os.path.join(self.__current_directory, file_name)

    def add_user(self):
        users = self.get_users()
        if not self.name or not self.name:
            raise  Exception("Name and phone are required")
        try:
            with open(self.get_file_path(self.__contacts_file), "w") as file:
                contacts_lsit = [
                    {"name": self.name, "phone": self.phone},
                ]
                if(len(users)):
                    contacts_lsit.extend(users)
                data =json.dumps(contacts_lsit)
                file.write(data)
                print("User added successfully")   
        except FileNotFoundError as e:
            raise Exception("Something went wrong!")

    def change_user_contact(self):
        if not self.name :
            raise Exception("Name is required")
        contacts:list[dict] = self.get_users()   
        print(contacts)
        try:
            with open(self.get_file_path(self.__contacts_file), "w") as file:
                for i in range(len(contacts)):
                    if self.name.lower() in contacts[i].get("name").lower():
                        phone = input("Enter new phone number: ")
                        contacts[i]["phone"] = phone
                        file.write(json.dumps(contacts))
                        print( "User contact changed successfully" ) 
                        return
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)    

    def get_user(self, name):
        contacts:list[dict] = self.get_users()   
        try:
            for i in range(len(contacts)):
                if name.lower() in contacts[i].get("name").lower():
                    print(contacts[i].get("name"), contacts[i].get("phone"))
                    return
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)
    
    def delete_user(self,name):
        contacts:list[dict] = self.get_users()   
        try:
            with open(self.get_file_path(self.__contacts_file), "w") as file:
                for i in range(len(contacts)):
                    if name.lower() in contacts[i].get("name").lower():
                        contacts.pop(i)
                        file.write(json.dumps(contacts))
                        print( "User deleted successfully" ) 
                        return
            raise Exception("User not found")
        except FileNotFoundError as e:
            raise Exception(e)
        

        
class AddressBook(Record):

    @log_error
    def add_record(self, name, phone):
        self.addName(name)
        self.addPhone(phone)
        self.add_user()
    @log_error
    def change_phone(self, name,):
        self.addName(name)
        self.change_user_contact()
    @log_error
    def get_phone(self, name):
        try:
           users = self.get_users()
           if not len(users):
                raise Exception("No users found")
           user = users.__getattribute__(name)
           print(user.get("name"), user.get("phone"))

        except FileNotFoundError as e:
            raise Exception(e)          
    @log_error       
    def print_all_users(self):
        try:
            users = self.get_users()
            if not len(users):
                raise Exception("No users found")
            for user in users:
                print(user.get("name"), user.get("phone"))
        except FileNotFoundError as e:
            raise Exception(e)
        
    @log_error       
    def delete(self, name):
        self.delete_user(name)    

    def print_user(self, name):
        self.get_user(name)    
        
    
    class Bot:
        def __init__(self):
            self.book = AddressBook()
        @log_error
        def parse_input(self):
            comand = {
                "1": "Add",
                "2": "Change",
                "3": "All",
                "4": "Delete user",
                "5": "Print user",
                "6": "Exit"
            }
            for key, value in comand.items():
                print(f"{key}: {value}")
            
            choice = input("How can I help you? Choose a command: ")
            
            if not choice :
                print("Choose a command")
                return   

            choice = choice.lower()
            match choice:
                case "1" | "add":
                    user = input("Enter user name and phone number: ").strip().split(" ")
                    self.book.add_record(user[0], user[1])
                case "2" |"change":
                    user = input("Enter user name : ").strip()
                    self.book.change_phone(user)
                case "3" | "all":
                    self.book.print_all_users()

                case "4" | "delete user":
                    user = input("Enter user name : ").strip()
                    self.book.delete_user(user)

                case "5" | "print user":
                    user = input("Enter user name : ").strip()
                    self.book.print_user(user)

                case "6" | "exit" | "close" | "quit":
                    print("Goodbye!")
                    exit()
                case _:
                    print("Invalid choice")
                    self.parse_input()
            self.parse_input()   

        def main(self):
            print("Welcome to Halper Bot!")
            self.parse_input()    

if __name__ == "__main__":
    bot = AddressBook.Bot()
    bot.main()
