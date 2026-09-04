import mysql.connector

# ---------- DATABASE CONNECTION ----------
def connect_db():
    return mysql.connector.connect(host="localhost",user="root",password="mysql123",database="HOTEL")
    print('CONNECTION SUCCESSFUL')
    
# ---------- CREATE DATABASE ----------
def create_database():
    con = mysql.connector.connect(host="localhost", user="root", password="mysql123")
    cur = con.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS HOTEL")
    con.close()
    print('DATABSE CREATION SUCCESSFUL')

  
# ---------- CREATE ROOMS TABLE ----------
def create_rooms_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms 
            (room_id INT PRIMARY KEY,
            room_type VARCHAR(50),
            price INT,
            available VARCHAR(10),
            features VARCHAR(200))""")
    con.close()
    print('ROOMS TABLE CREATED SUCCESSFULLY')

# ---------- CREATE SERVICES TABLE ----------
def create_services_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS services (
            service_id INT PRIMARY KEY,
            service_name VARCHAR(50),
            cost INT)""")
    con.close()
    print('SERVICES TABLE CREATED SUCCESSFULLY')

# ---------- CREATE BOOKINGS TABLE ----------
def create_bookings_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS bookings (
            booking_id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(50),
            phone VARCHAR(15),
            room_type VARCHAR(50),
            room_id INT,
            status VARCHAR(20),
            days INT,
            service_id INT,
            FOREIGN KEY (room_id) REFERENCES rooms(room_id),
            FOREIGN KEY (service_id) REFERENCES services(service_id))""")
    con.close()
    print('BOOKINGS TABLE CREATED SUCCESSFULLY')


# ---------- CREATE CHECK-IN / CHECK-OUT TABLE ----------
def create_check_in_out():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS check_in_out (
            id INT PRIMARY KEY AUTO_INCREMENT,
            booking_id INT,
            room_id INT,
            check_in_date DATE,
            check_out_date DATE,
            FOREIGN KEY (booking_id) REFERENCES bookings(booking_id),
            FOREIGN KEY (room_id) REFERENCES rooms(room_id))""")
    con.close()
    print('CHECK IN/CHECK OUT TABLE CREATED SUCCESSFULLY')


# ---------- CREATE BILLING TABLE ----------
def create_billing_table():
    con = connect_db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS billing (
            bill_id INT PRIMARY KEY AUTO_INCREMENT,
            booking_id INT,
            amount INT)""")
    con.close()
    print('BILLING TABLE CREATED SUCCESSFULLY')


# ---------- CREATE FEEDBACK TABLE ----------
def create_feedback_table():
    con = connect_db()
    cur = con.cursor()   
    cur.execute("""CREATE TABLE IF NOT EXISTS feedback
            (feedback_id INT PRIMARY KEY AUTO_INCREMENT,
            NAME VARCHAR(50),
            rating FLOAT,
            comments VARCHAR(200))""")
    con.close()
    print('FEEDBACK TABLE CREATED SUCCESSFULLY')

# ---------- SETUP DATABASE ----------
def setup_database():
    create_database()
    create_rooms_table()
    create_services_table()
    create_bookings_table()
    create_check_in_out()
    create_billing_table()
    create_feedback_table()


# ---------- MAIN PROGRAM ----------
setup_database()
print('ALL SETUP PROCESSES AND CREATION SUCCESSFUL')



