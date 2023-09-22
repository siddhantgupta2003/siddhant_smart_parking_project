import pymysql
import serial
from datetime import datetime
import time
from twilio.rest import Client
import datetime as dt

# Your Twilio credentials
account_sid = 'ACca4e7c9eae5c5e7ca7bb8f66619b3fa8'
auth_token = '892ce47d324f4fbb2ff560b933ded619'

# Create a Twilio client
client = Client(account_sid, auth_token)

# Replace with your database credentials
db_host = "localhost"
db_user = "root"
db_password = "siddhant"
db_database = "fpparking"

ser = serial.Serial('COM3', 9600, timeout=1)  # Replace 'COMx' with your Arduino's serial port

# Function to authenticate RFID card against the database
def minute_difference(time_stamp1, time_stamp2):
    # Parse the time stamps into datetime objects
    try:
        datetime1 = datetime.strptime(time_stamp1, "%Y-%m-%d %H:%M:%S")
        datetime2 = datetime.strptime(time_stamp2, "%Y-%m-%d %H:%M:%S")
        
        # Calculate the time difference
        time_difference = abs(datetime2 - datetime1)
        
        # Convert the time difference to minutes
        minutes = time_difference.total_seconds() / 60
        
        return int(minutes)
    except ValueError:
        return None
    
    
    
def send(rfid,entry_time,exit_time,entry_date,exit_date,total_bill):
    a="bill\n"
    b1="your id:"
    b=str(rfid)
    c1="\nentry_time:"
    c=str(entry_time)
    d1="\nexit_time:"
    d=str(exit_time)
    e1="\nentry_date:"
    e=str(entry_date)
    f1="\nexit_date:"
    f=str(exit_date)
    h1=("\nammount payable:")
    h=str(total_bill)
    
    g="\nthankyou for visiting"
    x=a+b1+b+c1+c+d1+d+e1+e+f1+f+h1+h+g
    
    return x
    
def exit_details(uid):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
    cursor = conn.cursor()
    try:
       
        slot_popped="SELECT slot_no FROM entery_data WHERE rfid=%s"
        cursor.execute(slot_popped,uid)
        slot = cursor.fetchone()[0]
        pop(slot)
        
        cursor.execute("SELECT * FROM entery_data WHERE rfid = %s", (uid,))
        
        # Fetch the row as an array
        row = cursor.fetchone()
        
        # Process the row (print as an example)
        return row[0],row[1],row[2],row[3]
        

    except Exception as e:
        print("Database Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()
        
def pop(slot_no):
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
        

    

        # Create a cursor object
        cursor = conn.cursor()

        cursor = conn.cursor()

         # Mark the slot as vacant (push it back onto the stack)
        cursor.execute("UPDATE parking_slots SET is_occupied = FALSE WHERE slot_no = %s", (slot_no,))
        print(f"Slot {slot_no} deallocated and pushed back onto the stack")

         # Commit the changes
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        
    except pymysql.Error as e:
        print(f"Error: {e}")
        
def calculate_bill(entry_time,entry_date,rfid):

    et=str(entry_time)
    ed=str(entry_date)
    time_stamp1 = ed +" "+ et
    print(time_stamp1)
  
    current_time= dt.datetime.now().time()
    t1= current_time.strftime("%H:%M:%S")
    t=str(t1)
    d = str(dt.date.today())
    time_stamp2 = d+" "+t
    print(time_stamp2)
    minute_spent = minute_difference(time_stamp1, time_stamp2)
    print(minute_spent)
    total_ammount= minute_spent * 5
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
      
    cursor = conn.cursor()

    
    # Fetch the row as an array
    cursor.execute("UPDATE entery_data SET rfid=NULL,entry_time=NULL,entry_date = NULL WHERE rfid = %s", (rfid,))
    conn.commit()

# Close the cursor and connection
    cursor.close()
    conn.close()
    return total_ammount
    
           
        
        
        
        ###########################################################################
        
        
        
        
        
        
        
try:
    while True:
        
        
        uidd = ser.readline().decode().strip() # Read RFID UID from Arduino
        print(uidd)
        if uidd!='':
           if uidd!=0:
               if len(uidd)>6:
                   data=exit_details(uidd)
                   entry_time=data[2]
                   entry_date=data[3]
                   
                   
                   cost=calculate_bill(entry_time,entry_date,data[1])
                                 
                   
                   exitt = dt.datetime.now().time()
                   exitd = dt.date.today()
                   
                   message = client.messages.create(
                       body=send(data[1],data[2],exitt,data[3],exitd,cost),
                       from_='+15179956945',
                       to='+919358120776'
                   
                    
                  )
                   a=1
                   
                   time.sleep(1)
               else:
                   a=0
           else:
               a=0
        else:
            a=0
               
        if (a==1):
            trigger_str = 1
            ser.write(str(trigger_str).encode())   # Send the trigger to Arduino
            time.sleep(1)
            
            
        else:
            a=0

except KeyboardInterrupt:
         ser.close()
