
"""   A program that would print the book synopsis from it's isbn sourced from a data set
      provided in a csv file
      API USED: GoogleBooksAPI
      API Limit: 1000 queries/day
      API Acceptable rate: 1 query/sec

                                           """
import pandas as pd #for working with csv files
import requests     #for making the url requests
import json         #for working with json data returned

#the Api Key
googleApiKey = "AIzaSyBgkfNeOQggSUa5LELO3q7Kd3Bkhw4WuS0"
backupgoogleApiKey = "AIzaSyCuR3dTMRYEqOsRgarsb3DWs4__jZ-ME2w"
#function
#input: Book's ISBN  | Requires: API Key
#output: Book's Title & Summary
#Returns: None


synopsisList = [] #this list would store synopsis for all the books sequentially
def searchURL(parms):
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
        return r.json()
        

def lookup(ISBN,TITLE,count):
        try:
            #attempting to look up by ISBN
            print('\tinside the lookup function')
            parmsISBN = {'q':"isbn:"+ISBN, 'key':googleApiKey}
            rj = searchURL(parmsISBN)
            book = rj["items"][0]["volumeInfo"]
            print("\t\tTITLE: " + book["title"])    #printing desired fields
            print("\t\tSYNOPSIS:\n\t" + book["description"])
            synopsisList.append(book["description"])
        except Exception as e:
            #Will be fired when no/invalid ISBN is provided in the dataset
            #attempting to look by TITLE
            print("\t\tException is :s "+str(e))
            print("\t\t\tFailed to look up the book by ISBN")
            print("\t\t\t\tLooking up by Title...")
            try:
                parmsTITLE = {'q':"intitle:"+title, 'key':googleApiKey}
                rj = searchURL(parmsTITLE)
                book = rj["items"][0]["volumeInfo"]
                print("\t\t\t\t\tTITLE: " + book["title"])
                print("\t\t\t\t\t\tSYNOPSIS:\n\t" + book["description"])
                synopsisList.append(book["description"])
            except Exception as ee:
               #Executed when the book is not found on the engine
               #Unable to lookup the book        
               print("\t\t\t\tException: "+str(ee)+"\n\t"+" BOOK NOT FOUND!")
               synopsisList.append("BOOK NOT FOUND!")   #add in case the ISBN is invalid
               count+=1
        finally:
                return count
            


#reading from the csv file
path = "C:/Users/AnshulAggarwal/Desktop/datase.csv"
df = pd.read_csv(path)
count = 0 #This will count the number of books not found
for isbn, title in zip(df["ISBN"], df["Title"]):    #read the ISBN,TITLE only
    print("---------",end="\n")
    print("Looking for ISBN: "+str(isbn)+ "  with TITLE: "+title)
    count = lookup(isbn,title,count)
    
#adding the synopsis to the csv file
df["Summary"] = synopsisList      #appending a new column to the dataframe
df.to_csv(path)                 #writing the dataframe to the csv file
print("book\'s synopsis successfully inserted into the file ")
print(str(count)+" Books not found!")        #no. of books not found!
