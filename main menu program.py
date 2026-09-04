from creationsetup import connect_db


def main_menu():
    while True:
        print("\n--------------------------------------WELCOME TO HOTEL BLUE RADDISON---------------------------------------------")
        print("1. Show Rooms Available")
        print("2. Booking")
        print("3. Search Booking by Phone Number")
        print("4. Check-In / Check-Out")
        print("5. Generate Bill")
        print("6. Give Feedback")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            show_rooms()
        elif choice == "2":
            booking()
        elif choice == "3":
            search_booking()
        elif choice == "4":
            check_in_out()
        elif choice == "5":
            generate_bill()
        elif choice == "6":
            feedback()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")

    
# ---------- SHOW ROOMS ----------
def show_rooms():
    con = connect_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM rooms WHERE available='YES'")
    rooms = cur.fetchall()
    print("\n--- Rooms Available ---")
    for r in rooms:
        print(f"Room ID: {r[0]}, Type: {r[1]}, Price: {r[2]}, Available: {r[3]}, Features: {r[4]}")
    con.close()

# ---------- BOOKING ----------
def booking():
    con = connect_db()
    cur = con.cursor()

    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    room_type = input("Enter room type to book: ")
    days = int(input("Enter number of days to stay: "))
    room_id=int(input("Enter the room id by taking refrence from list:"))

    cur.execute("""
        SELECT room_id, price, features 
        FROM rooms
        WHERE room_type=%s AND available='YES'
        ORDER BY room_id ASC
        LIMIT 1""", (room_type,))
    room = cur.fetchone()

    if not room:
        print("No room available of this type.")
        con.close()
        return
        room_id = room[0]

    # Show services
    print("\n--- Available Services ---")
    cur.execute("SELECT * FROM services")
    services = cur.fetchall()
    for s in services:
        print(f"{s[0]}: {s[1]} (Rs {s[2]})")

    service_choice = input("Enter service ID (0 for none): ")
    service_id = None if service_choice == "0" else int(service_choice)

 
    cur.execute("""INSERT INTO bookings (name, phone, room_type, room_id, status, days, service_id)
        VALUES (%s, %s, %s, %s, 'BOOKED', %s, %s)
    """, (name, phone, room_type, room_id, days, service_id))

    cur.execute("UPDATE rooms SET available='NO' WHERE room_id=%s", (room_id,))

    con.commit()
    print(f"\nRoom {room_id} booked successfully for {days} days!")
    con.close()
 


# ---------- SEARCH BOOKING ----------
def search_booking():
    con = connect_db()
    cur = con.cursor()
    phone = input("Enter phone number to search booking: ")
    cur.execute("SELECT * FROM bookings WHERE phone=%s", (phone,))
    bookings = cur.fetchall()
    if bookings:
        for b in bookings:
            print(f"Booking ID: {b[0]}, Name: {b[1]}, Phone: {b[2]}, Room: {b[3]}, Status: {b[4]}, Days: {b[5]}, ServiceID: {b[6]}")
    else:
        print("No booking found with this phone number.")
    con.close()

# ---------- CHECK-IN / CHECK-OUT ----------
def check_in_out():
    con = connect_db()
    cur = con.cursor()
    phone = input("Enter phone number: ")
    cur.execute("SELECT * FROM bookings WHERE phone=%s", (phone,))
    booking = cur.fetchone()
    cur.fetchall()  

    if booking:
        action = input("Enter 'IN' for Check-In or 'OUT' for Check-Out: ").upper()
        
        if action == "IN":
            room_id = input("Enter room number: ")
            booking_id = booking[0]
            room_id=booking[4]
            check_in = input("Enter check-in date (YYYY-MM-DD): ")
            cur.execute("""INSERT INTO check_in_out (room_id, booking_id, check_in_date, check_out_date)
                                     VALUES (%s, %s, %s, NULL)""", (room_id, booking_id, check_in))
            con.commit()
            print("Guest checked-in successfully!")


        elif action == "OUT":
            check_out = input("Enter check-out date (YYYY-MM-DD): ")
            booking_id = booking[0]
            room_id=booking[4]
            cur.execute("""UPDATE check_in_out
                                     SET check_out_date=%s
                                     WHERE booking_id=%s""", (check_out, booking_id))
            cur.execute("""UPDATE rooms  SET available='YES'
                         WHERE room_id=%s""", (room_id,))
            cur.execute("""UPDATE bookings
                                     SET status='CHECKED-OUT'
                                     WHERE booking_id=%s""", (booking_id,))
            con.commit()
            print("Guest Checked-Out successfully!")

      
    else:
        print("No booking found.")
    con.close()

# ---------- GENERATE BILL ----------
def generate_bill():
    con = connect_db()
    cur = con.cursor()

    print("\n------ GENERATE BILL ------")
    booking_id = input("Enter your Booking ID: ")
    phone = input("Enter your Phone Number: ")

    cur.execute("""SELECT name, room_id, room_type, days 
        FROM bookings 
        WHERE booking_id=%s AND phone=%s""", (booking_id, phone))

    booking = cur.fetchone()

    if booking is None:
        print("\n❌ No booking found! Check Booking ID or Phone Number.")
        con.close()
        return

    customer_name, room_id, room_type, days = booking

    days = int(days)

    cur.execute("""SELECT price 
        FROM rooms 
        WHERE room_id=%s""", (room_id,))

    room_data = cur.fetchone()

    if room_data is None:
        print("\n❌ Room details missing in rooms table!")
        con.close()
        return

    room_rent = float(room_data[0])

    #Bill calculation
    amount = room_rent * days
    gst = amount * 0.18
    total = amount + gst

    con = connect_db()
    cur = con.cursor()

    cur.execute("""SELECT name, room_id, room_type, days 
        FROM bookings 
        WHERE booking_id=%s AND phone=%s""", (booking_id, phone))

    booking = cur.fetchone()

    if booking is None:
        print("\n❌ No booking found! Check Booking ID or Phone Number.")
        con.close()
        return

    customer_name, room_id, room_type, days = booking

    days = int(days)

    cur.execute("""SELECT price 
        FROM rooms 
        WHERE room_id=%s""", (room_id,))

    room_data = cur.fetchone()

    if room_data is None:
        print("\n❌ Room details missing in rooms table!")
        con.close()
        return

    room_rent = float(room_data[0])

    #Bill calculation
    amount = room_rent * days
    gst = amount * 0.18
    total = amount + gst


    cur.execute("""
        INSERT INTO billing (booking_id, amount)
        VALUES (%s, %s)""", (booking_id, total))

    con.commit()

    #Print Bill
    print("\n------ BILL INVOICE ------")
    print(f"Customer Name : {customer_name}")
    print(f"Room ID       : {room_id}")
    print(f"Room Type     : {room_type}")
    print(f"Rent per Day  : ₹{room_rent}")
    print(f"No. of Days   : {days}")
    print("----------------------------")
    print(f"Amount        : ₹{amount}")
    print(f"GST (18%)     : ₹{gst}")
    print("----------------------------")
    print(f"TOTAL BILL    : ₹{total}")
    print("----------------------------")

    con.close()


   
   
# ---------- FEEDBACK ----------
def feedback():
    con = connect_db()
    cur = con.cursor()
    NAME = input("Enter your NAME: ")
    rating = float(input("Rate your stay (1-5): "))
    comments = input("Enter your feedback: ")
    cur.execute("INSERT INTO feedback (NAME, rating, comments) VALUES (%s,%s,%s)", 
                (NAME, rating, comments))
    con.commit()
    print("Thank you for your feedback!")
    con.close()


#-----------CALLING FUNCTION---------------

main_menu()




    


    
