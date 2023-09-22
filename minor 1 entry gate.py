import pymysql
import serial
import datetime
import time
from twilio.rest import Client

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

ser = serial.Serial('COM4', 9600, timeout=1)  # Replace 'COMx' with your Arduino's serial port

# Function to authenticate RFID card against the database
def send(slt):
    a="""hello from smart parking management \n
      namaste\n
     welcome to\n
    centrio mall\n"""
    b="your slot number is:"
    c=slt
    d=a+b+c
    e="\nthankyou for visiting"
    f=d+e
    return f
def enter_details(uid):
    conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
    cursor = conn.cursor()
    try:
        current_time = datetime.datetime.now().time()
        current_date = datetime.date.today()
        pslot=push()
        sql_insert =""" UPDATE entery_data
        SET rfid = %s, entry_time = %s, entry_date = %s
        WHERE slot_no = %s"""

    # Define the values to be inserted
        values = (uid,current_time,current_date,pslot)  # Replace with your actual values
        print("done")
    # Execute the SQL query with the values
        cursor.execute(sql_insert, values)
       
        conn.commit()
        
        
        return pslot

    except Exception as e:
        print("Database Error:", e)
        return False

    finally:
        cursor.close()
        conn.close()
        
def push():
    try:
        conn = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_database)
        

    

        # Create a cursor object
        cursor = conn.cursor()

        # Find the topmost vacant parking slot (last in the stack)
        cursor.execute("SELECT slot_no FROM parking_slots WHERE is_occupied = FALSE ORDER BY slot_no DESC LIMIT 1")
   

        slot = cursor.fetchone()[0]
        if slot:
            # Mark the slot as occupied
            print(cursor.execute("UPDATE parking_slots SET is_occupied = TRUE WHERE slot_no = %s", (slot,)))
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()
        return slot
    except pymysql.Error as e:
        print(f"Error: {e}")
        
        
        
        
        
        ###########################################################################
        
        
        
        
        
        
        
try:
    while True:
        
        
        uidd = ser.readline().decode().strip() # Read RFID UID from Arduino
        print(uidd)
        if uidd!='':
           if uidd!=0:
               if len(uidd)>6:
                   slot=enter_details(uidd)
                   str_slot=str(slot)
                   print(send(str_slot))
                   message = client.messages.create(
                       body=send(str_slot),
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
