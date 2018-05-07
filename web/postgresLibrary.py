#postgresLibrary
#Collection of functions for abstracting away database requests into simple
#method calls for usage throughout the server and applications
#!/usr/bin/python
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import uuid

#Setup/Close Connection Methods - Will paramaterize and clean up other code later
def setupConnection():
    """Sets up connection to the database and creates a cursor on this database"""
    conn = psycopg2.connect("dbname=docker user=docker password=docker host=postgres")
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def closeConnection( conn, cur ):
    """Closes the connections passed in. Cursor must be closed first"""
    cur.close()
    conn.close()

def getAll( query ):
    conn, cur = setupConnection()
    cur.execute(query)
    values = cur.fetchall()
    closeConnection(conn, cur)
    return values

def getItembyUUID( query, uuid ):
    conn, cur = setupConnection()
    cur.execute(query, (uuid,))
    value = cur.fetchone()
    closeConnection(conn, cur)
    return value

def getItemsbyCol( query, col ):
    conn, cur = setupConnection()
    cur.execute(query, (col,))
    value = cur.fetchall()
    closeConnection(conn, cur)
    return value    

def insertItem( query, tuple ):
    conn, cur = setupConnection()
    cur.execute( query, tuple )
    inserted = cur.fetchone()
    conn.commit()
    closeConnection(conn, cur)
    return inserted['uuid']

def deleteItem( query, param ):
    conn, cur = setupConnection()
    cur.execute( query, (param,))
    conn.commit()
    closeConnection(conn, cur)

def updateItem(query, tuple):
    conn, cur = setupConnection()
    cur.execute( query, tuple)
    status = cur.rowcount
    conn.commit()
    closeConnection(conn, cur)
    return status

#User Select Functions
def getUsers():
    """Returns all information on all users in the database"""
    query = "SELECT * from users;"
    users = getAll(query)
    return users
    
def getUserbyUUID( userUUID ) :
    """Returns all information for selected user in the database
    input-> userUUID - uuid of the user wanted"""
    query = "Select * from users WHERE uuid =(%s);"
    userInfo = getItembyUUID(query, userUUID)
    return userInfo

def getUserbyEmail( email ) :
    query = "Select * from users WHERE email = (%s);"
    userInfo = getItembyUUID(query, email)
    return userInfo

#User Insert Functions
def insertUser( email ):
    #uncertain what we are doing with the hash. Can change later
    query = "INSERT INTO users (email) VALUES ( %s ) RETURNING uuid;"
    tuple = (email,)
    uuid = insertItem(query, tuple)
    return uuid 

def deleteUser( userUUID ) :
    query = "DELETE FROM users WHERE uuid = %s;"
    deleteItem(query, userUUID)

#User Update Function    
def updateUserEmail( newEmail, userUUID ):
    query = "UPDATE users SET email = (%s) WHERE uuid = (%s);"
    return updateItem(query, (newEmail, userUUID))
    
#Guest Select Functions
def getGuests():
    """Returns all information on all of the guests in the database"""
    query = "SELECT * from guests"
    guests = getAll(query)
    return guests

def getGuestbyUUID( guestUUID ) :
    """Returns information on one user based on either the random uuid or 
    user(uuid)"""
    query = "SELECT * from guests WHERE uuid = (%s);"
    guest = getItembyUUID(query, guestUUID)
    return guest

def getGuestbyName(first, last):
    conn, cur = setupConnection()
    cur.execute("SELECT * from guests WHERE first_name = (%s) AND last_name = (%s);", (first, last))
    guest = cur.fetchone()
    closeConnection(conn, cur)
    return guest

def getGuestbyRoomUUID( roomUUID ) :
    """Returns information on one user based on the room uuid"""
    query = "SELECT * from guests g INNER JOIN reservations r on g.uuid = r.guest_uuid and r.room_uuid = (%s);"
    guest = getItembyUUID(query, roomUUID)
    return guest

#Guest Insert Functions
def insertGuestwithUUID( userUUID, first, middle, last, email=None, phone=None, address=None, city=None, state=None, zip=None ):
    query = """INSERT INTO guests (user_uuid, first_name, middle_name, last_name, email, phone, address, city, state, zip) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING uuid"""
    tuple = (userUUID, first, middle, last, email, phone, address, city, state, zip)
    guest = insertItem(query, tuple)
    return guest

def insertGuest(first, middle, last, email=None, phone=None, address=None, city=None, state=None, zip=None):
    query = """INSERT INTO guests (first_name, middle_name, last_name, email, phone, address, city, state, zip) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING uuid"""
    tuple = (first, middle, last, email, phone, address, city, state, zip)
    guest = insertItem(query, tuple)
    return guest

def attachUsertoGuest( guestUUID, userUUID):
    query = """UPDATE guests SET user_uuid = (%s) where uuid = (%s);"""
    tuple = (userUUID, guestUUID)
    return updateItem(query, tuple)

def deleteGuest( guestUUID ) :
    query = "DELETE FROM guests WHERE uuid = (%s);"
    deleteItem(query, guestUUID)

def updateGuestEmail( newEmail, guestUUID ) :
    query = "UPDATE guests SET email = (%s) WHERE uuid = (%s);"
    return updateItem(query, (newEmail, guestUUID))

#Session select functions
def getSessions():
    query = "SELECT * from sessions;"
    sessions = getAll(query)
    return sessions

def getSessionbyUUID( sessionUUID ):
    """returns information on one user by uuid or users(uuid)"""
    query = "SELECT * from sessions WHERE uuid = (%s);"
    session = getItembyUUID(query, sessionUUID)
    return session

def getTimeRangebyUUID( sessionUUID ):
    """returns just the time range based on the uuid or user(uuid)"""
    session = getSessionbyUUID(sessionUUID)
    timeStart = session["created"]
    timeEnd = session["expires"]
    return timeStart, timeEnd

#Session Insert Functions
def insertSession( userUUID, token, ip):
    query = "INSERT INTO sessions (user_uuid, token, ip) VALUES (%s, %s, %s) RETURNING uuid;"
    tuple = (userUUID, token, ip)
    sessUUID = insertItem(query, tuple)
    return sessUUID

def deleteSession( sessUUID ):
    query = "DELETE FROM sessions WHERE uuid = (%s);"
    deleteItem(query, sessUUID)

def updateSessionValue( valid, sessUUID ):
    query = "UPDATE sessions SET invalidated = (%s) WHERE uuid = (%s)"
    return updateItem(query, (valid, sessUUID))

#Rooms Select Functions

def getRooms():
    """returns information for all rooms in the database"""
    query = "SELECT * from rooms;"
    rooms = getAll(query)
    return rooms

def getRoombyUUID( roomUUID ):
    """returns information on room in the database"""
    query = "SELECT * from rooms WHERE uuid = (%s);"
    room = getItembyUUID(query, roomUUID)
    return room

#Room Insert Functions
def insertRoom( name, number, floor=None):
    query = "INSERT INTO rooms (name, number, floor) VALUES (%s,%s,%s) RETURNING uuid"
    tuple = (name, number, floor)
    return insertItem( query, tuple)

def deleteRoom( roomUUID ):
    query = "DELETE FROM rooms WHERE uuid = (%s);"
    deleteItem(query, roomUUID)
    
#Peripheral Select Functions
def getPeripherals():
    query="SELECT * from peripherals;"
    peripherals = getAll(query)
    return peripherals

def getPeripheralbyUUID( periUUID ):
    """returns information by uuid"""
    query = "SELECT * from peripherals WHERE uuid = (%s);"
    peripheral = getItembyUUID(query, periUUID)
    return peripheral

def getPeripheralsbyRoom( roomUUID ):
    """returns information by room_uuid for all peripherals in room"""
    query = "SELECT * from peripherals WHERE room_uuid = (%s);"
    peripherals = getItemsbyCol(query, roomUUID)
    return peripherals

def getStatusbyUUID ( periUUID ) :
    """return status for periUUID """
    query = "SELECT active from peripherals WHERE uuid = (%s);"
    status = getItembyUUID(query, periUUID)
    return status

def getPeripheralsbyType(type):
    query = "SELECT * from peripherals WHERE type = (%s);"
    peripherals = getItemsbyCol(query, type)
    return peripherals

#Peripheral Insert Functions
def insertPeripheral(roomUUID, name, type, active=False, power=False, state= 0, last_update=None):
    query = "INSERT INTO peripherals (room_uuid, name, type, active, power,state, last_update) VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING uuid;"
    tuple = (str(roomUUID), name, type, active, power, state, last_update)
    peri = insertItem(query, tuple)
    return peri

def deletePeripheral(periUUID):
    query = "DELETE FROM peripherals WHERE uuid = (%s);"
    deleteItem(query, periUUID)
    
def updatePeripheralActive( active, periUUID):
    query = "UPDATE peripherals SET active = (%s) WHERE uuid = (%s);"
    return updateItem( query, (active, periUUID))

#TV Channel Select Functions
def getChannels():
    query = "SELECT * from tv_channels;"
    channels = getAll(query)
    return channels

def getChannelbyUUID( chanUUID ):
    query = "SELECT * from tv_channels WHERE uuid = (%s);"
    channel = getItembyUUID(query, chanUUID)
    return channel
    
#Channel Insert Functions
def insertChannel(name, number, image=None):
    query = "INSERT INTO tv_channels (name, number, image) VALUES (%s,%s,%s) RETURNING uuid;"
    tuple = (name, number, image)
    chanUUID = insertItem(query, tuple)
    return chanUUID

def deleteChannel(chanUUID):
    query = "DELETE FROM tv_channels WHERE uuid = (%s);"
    deleteItem(query, chanUUID)

#Room Service Select Functions
def getRoomServiceItems():
    query = "SELECT * from roomservice_item;"
    items = getAll(query)
    return items

def getRoomServiceItembyUUID( rsiUUID ):
    query = "SELECT * from roomservice_item WHERE uuid = (%s);"
    item = getItembyUUID(query, rsiUUID)
    return item

#Room Service Insert Functions
def insertRoomServiceItem(name, desc, cost, image=None, sku=None):
    query = """INSERT INTO roomservice_item (name, description, cost, image,
 sku) VALUES (%s,%s,%s,%s,%s) RETURNING uuid;"""
    tuple = (name, desc, cost, image, sku)
    rsItem = insertItem(query, tuple)
    return rsItem

def deleteRoomServiceItem(rsiUUID):
    query = "DELETE FROM roomservice_item WHERE uuid = (%s);"
    deleteItem(query, rsiUUID)

#Room Service Request Select Functions
def getRoomServiceRequests():
    query = "SELECT * from roomservice_requests;"
    requests = getAll(query)
    return requests


def getRoomServiceRequestbyUUID( rsrUUID ):
    """ get room service request by the various uuids - uuid, room_uuid, user_uuid"""
    query = "SELECT * from roomservice_requests WHERE uuid = (%s);"
    request = getItembyUUID(query, rsrUUID)
    return request

def isCompletedRoomServicebyUUID( rsrUUID ):
    """ boolean if the request is completed"""
    request = getRoomServiceRequestbyUUID(rsrUUID)
    return request["completed"]

def getRoomServiceRequestsUncompleted():
    """ returns information on all noncompleted requests"""
    query = "SELECT * from roomservice_requests WHERE completed = (%s);"
    requests = getItemsbyCol(query, False)
    return requests

#Room Service Request Insert Functions
def insertRoomServiceRequest( room_uuid, user_uuid, type_uuid, end_time, start_time=None, quantity= 1, comp=False):
    query = """INSERT INTO roomservice_requests ( room_uuid, user_uuid, 
type_uuid, start_time, end_time, quantity, completed) VALUES 
(%s,%s,%s,%s,%s,%s,%s) RETURNING uuid;"""
    tuple = (room_uuid, user_uuid, type_uuid, start_time, end_time, quantity, comp)
    rsrUUID = insertItem(query, tuple)
    return rsrUUID
    
def deleteRoomServiceRequest( rsrUUID ):
    query = "DELETE FROM roomservice_requests WHERE uuid = (%s);"
    deleteItem(query, rsrUUID)

def updateRoomServiceRequestCompleted( completed, rsrUUID ):
    query = "UPDATE roomservice_requests SET completed = (%s) WHERE uuid = (%s);"
    return updateItem(query, (completed, rsrUUID))

#Maintenance request select function

def getMaintenanceRequests():
    query = "SELECT * from maintenance_requests;"
    requests = getAll(query)
    return requests

def getMaintenanceRequestbyUUID(mreqUUID):
    query = "SELECT * from maintenance_requests WHERE uuid = (%s);"
    request = getItembyUUID(query, mreqUUID)
    return request

def isCompletedMaintenanceRequestByUUID( mreqUUID ):
    request = getMaintenanceRequestbyUUID(mreqUUID)
    return request["completed"]

def getMaintenanceRequestsUncompleted():
    query = "SELECT * from maintenance_requests WHERE completed = (%s);"
    requests = getItemsbyCol(query, False)
    return requests

#Maintenance Request Insert Functions
def insertMaintenanceRequest( room_uuid, user_uuid, desc, end_time, quan = 1, comp = False):
    query = """INSERT INTO maintenance_requests ( room_uuid, user_uuid, description, end_time,
quantity, completed) VALUES (%s,%s,%s,%s,%s,%s) RETURNING uuid;"""
    tuple = (str(room_uuid), str(user_uuid), desc, end_time, quan, comp)
    mreqUUID = insertItem(query, tuple)
    return mreqUUID

def deleteMaintenanceRequest( mreqUUID ) :
    query = "DELETE FROM maintenance_requests WHERE uuid = (%s);"
    deleteItem(query, mreqUUID)

def updateMaintenanceRequestCompleted( completed, mreqUUID ):
    query = "UPDATE maintenance_requests SET completed = (%s) WHERE uuid = (%s);"
    return updateItem(query, (completed, mreqUUID))

#Transaction Select Functions
def getTransactions() :
    query = "SELECT * from transactions;"
    transactions = getAll(query)
    return transactions
    
def getTransactionbyUUID( tranUUID ) :
    query = "SELECT * from transactions WHERE uuid = (%s);"
    transaction = getItembyUUID(query, tranUUID)
    return transaction

#Transaction Insert Functions
def insertTransaction(room_uuid, user_uuid, desc, amount=0):
    query = "INSERT INTO transactions (room_uuid, user_uuid, amount, description) VALUES (%s,%s,%s,%s) RETURNING uuid;"
    tuple = (room_uuid, user_uuid, amount, desc)
    tranUUID = insertItem(query, tuple)
    return tranUUID

def deleteTransaction(tranUUID):
    query = "DELETE FROM transactions WHERE uuid = (%s);"
    deleteItem(query, tranUUID)

#Reservation Requests Select functions

def getReservations() :
    query = "SELECT * from reservations;"
    reservations = getAll(query)
    return reservations

def getReservationbyUUID(rreqUUID):
    """get reservation requests by uuid, room_uuid, guest_uuid"""
    query = "SELECT * from reservations WHERE uuid = (%s);"
    reservation = getItembyUUID(query, rreqUUID)
    return reservation

#Reservation Request Insert Functions
def insertReservation(roomUUID, guestUUID, startDate=None, endDate=None, checkIn =False, checkOut=False ):
    query = "INSERT INTO reservations (room_uuid, guest_uuid, start_date, end_date, check_in, check_out) VALUES (%s,%s,%s,%s,%s,%s) RETURNING uuid;"
    tuple = (str(roomUUID), str(guestUUID), startDate, endDate, checkIn, checkOut)
    resUUID = insertItem(query, tuple)
    return resUUID

def checkInReservation( uuid, status ):
    query = "UPDATE reservations SET check_in = (%s) WHERE uuid = (%s)"
    tuple = (status, str(uuid))
    updateItem(query, tuple)

def checkOutReservation( uuid, status ):
    query = "UPDATE reservations SET check_out = (%s) WHERE uuid = (%s)"
    tuple = (status, str(uuid))
    updateItem(query, tuple)

def deleteReservation( resUUID ) :
    query = "DELETE FROM reservations WHERE uuid = (%s);"
    deleteItem(query, resUUID)

#Employee Select Functions

def getEmployees():
    query = "SELECT * from employees;"
    employees = getAll(query)
    return employees 

def getEmployeebyUUID(empUUID):
    """get employee by uuid, user_uuid"""
    query = "SELECT * from employees WHERE uuid = (%s);"
    employee = getItembyUUID(query, empUUID)
    return employee

def isAdminEmployee(empUUID):
    """return if employee is admin"""
    employee = getEmployeebyUUID( empUUID ) 
    return employee["admin"]

#Employee Insert Functions
def insertEmployee(userUUID, first, last, admin=False):
    query = "INSERT INTO employees (user_uuid, first_name, last_name, admin) VALUES (%s,%s,%s,%s) RETURNING uuid;"
    tuple = (str(userUUID), first, last, admin)
    emp = insertItem(query, tuple)
    return emp

def deleteEmployee( empUUID ):
    query = "DELETE FROM employees WHERE uuid = (%s);"
    deleteItem(query, empUUID)

def updateEmployeeAdmin( admin, empUUID):
    query = "UPDATE employees SET admin = (%s) WHERE uuid = (%s);"
    return updateItem(query, (admin,empUUID))
