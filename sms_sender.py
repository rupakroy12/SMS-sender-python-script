import requests
import json
import random as r
import csv
# from csv import DictWriter

#Api hitting 
def send_sms(number, message):
    url = "https://www.fast2sms.com/dev/bulk"
    params = {
        'authorization': '8iQnCNvMcg69lHoyYfK2arVmOGUBtkAzjLRqPThd70W3bsuDXeUvWTbntzmrO5ARKHVcoQGZDLa49PFp',
        'sender_id': 'FSTSMS',
        'message': message,
        'language': 'english',
        'route': 'p',
        'numbers': number
    }

    response = requests.get(url, params=params)

    dict = response.json()
    # print(dict)
    return dict

#generate 4-digit random OTP
def otpgen():
    otp = ""
    for i in range(4):
        otp += str(r.randint(1, 9))
    # print("Your One Time Password is " + otp)
    return otp



#read a csv file from filename ('Phonebook.csv in our case)
def read_file():
    #reading file
    with open('Phonebook.csv') as contacts:
        reader = csv.DictReader(contacts)

        contact_list = []

        #to store number of invalid contacts found in contact_list    
        invalid_contacts = 0

        for row in reader:
            num = row['Mobile Number']

            #check for invalid numbers (length not equals 10, for INDIAn numbers)
            if (len(str(num)) is not 10):
                print(f'Invalid Number : {num}')
                invalid_contacts += 1
            else:
                contact_list.append(num)
        
        #function returns a list of contact numbers which can be iterated over to send sms
        return contact_list

#write some records in a new csv file (named final_csv, in our case)
def write_file(records):
    
    #creating and opening  a new csv file(final_csv, in our case) in 'WRITE' mode
    with open('final_csv.csv', 'w', newline= '\n') as f:
        
        #writing headers to our CSV, its mandatory to write header in newly generated empty csv file
        csv_writer = csv.DictWriter(
            f, fieldnames=['Phone Numbers', 'return', 'request_id', 'message'])    
        csv_writer.writeheader()
        
        count = 0
        
        #iterating over records, here record is a dictionary passed to the function from main
        #records = {'phone_number' : {'return' : 'True', 'id' : 'some_value', 'message':['message']} }
        for record in records:
            reports = records[record]

            #writing entries to the csv
            csv_writer.writerow({
                'Phone Numbers': record ,
                'return': reports['return'],
                'request_id': reports['request_id'],
                'message': reports['message']
            })

            #number of entries made
            count += 1

        #printing
        print(f'Write successful \n{count} numbers written to final_csv.csv')





if __name__ == '__main__':
    contact_list = read_file()
    records = {}

    for number in contact_list:

        otp = int(otpgen())
        message = 'Your One time Password is ' + str(otp)
        

        dict = send_sms(number, message)

        if dict.get('return') is False:
            print("Sorry, Otp could not be sent ! ")
               
        else:
            records[number] = dict

    write_file(records)
