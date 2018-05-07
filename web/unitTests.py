import unittest
import time
import postgresLibrary as pL

class TestPostgresLibraryUserMethods(unittest.TestCase):
    @classmethod
    def setUp(self): #remove all used users for next test run
        users = pL.getUsers()
        for user in users:
            if str.startswith(user['email'], "User"):
                pL.deleteUser(user['uuid'])
    def test_insertUser(self): # attempt to insert new user
        uuid = pL.insertUser("UserInsertTest@test.com")
        self.assertTrue(uuid != None)
    def test_deleteUser(self): # attempt to delete a user
        uuid = pL.insertUser("UserDeleteTest@test.com")
        pL.deleteUser(uuid)
        self.assertTrue(pL.getUserbyUUID(uuid) == None)
    def test_getUserByUUID(self): # attempt to get user by UUID
        uuid = pL.insertUser("UserUUIDTest@test.com")
        user = pL.getUserbyUUID(uuid)
        self.assertTrue(user != None)
    def test_getUsers(self): # attempt to get all users
        usera = pL.insertUser("Users1Test@test.com")
        userb = pL.insertUser("Users2Test@test.com")
        users = pL.getUsers()
        presence = 0
        for user in users:
            if user['uuid'] == usera or user['uuid'] == userb:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_updateUserEmail(self): # attempt to alter user email
        usera = pL.insertUser("UserEmailSwitchA@test.com")
        pL.updateUserEmail("UserEmailSwitchB@test.com", usera)
        self.assertTrue(pL.getUserbyUUID(usera)['email'] == "UserEmailSwitchB@test.com")
    def test_getUserbyEmail(self):
        useruuid = pL.insertUser("UserEmailTest20@test.com")
        user = pL.getUserbyEmail("UserEmailTest20@test.com")
        self.assertTrue(user['uuid'] == useruuid)
    #SUGGESTION add getUserbyEmail

class TestPostgresLibraryGuestMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        users = pL.getUsers()
        guests = pL.getGuests()
        for g in guests:
            if g['last_name'] == "Test":
                pL.deleteGuest(g['uuid'])
        for u in users:
            if str.startswith(u['email'], "GuestUserTest"):
                pL.deleteUser(u['uuid'])
    def test_insertGuestwithUUID(self): # attempt to insert new Guest with a user
        user_uuid = pL.insertUser("GuestUserTest1@test.com")
        guest_uuid = pL.insertGuestwithUUID(user_uuid, "James", "F.", "Test", "GuestUserTest1@test.com", "555-3456", "12 Test Lane", "Testville", "Tenesssee", "00234")
        self.assertTrue(guest_uuid != None)
    def test_insertGuest(self): # attempt to insert new Guest without a user
        guest_uuid = pL.insertGuest("Mark", "B.", "Test", "GuestUserTest8@test.com", "555-3456", "12 Test Lane", "Testville", "Tenesssee", "00234")
        self.assertTrue(guest_uuid != None)
    def test_attachUsertoGuest(self): # create a guest without a user, a user, then a guest with a user
        user_uuid = pL.insertUser("GuestUserTest8@test.com")
        guest_uuid = pL.insertGuest("Paul", "E.", "Test", "GuestUserTest9@test.com", "555-3456", "12 Test Lane", "Testville", "Tenesssee", "00234")
        pL.attachUsertoGuest( guest_uuid, user_uuid)
        self.assertTrue(pL.getGuestbyUUID(guest_uuid)['user_uuid'] != None)
    def test_deleteGuest(self): # attempt to deleta a new Guest
        user_uuid = pL.insertUser("GuestUserTest2@test.com")
        guest_uuid = pL.insertGuestwithUUID(user_uuid, "Terry", "A.", "Test", "GuestUserTest2@test.com", "555-4567", "13 Test Lane", "Testville", "Tenesssee", "00234")
        pL.deleteGuest(guest_uuid)
        self.assertTrue(pL.getGuestbyUUID(guest_uuid) == None)
    def test_updateGuestEmail(self): # attempt to change the email of a guest
        user_uuid = pL.insertUser("GuestUserTest3@test.com")
        guest_uuid = pL.insertGuestwithUUID(user_uuid, "Monica", "A.", "Test", "GuestUserTest3@test.com", "555-2345", "11 Test Lane", "Testville", "Tenesssee", "00234")
        pL.updateGuestEmail("GuestUserTest4@test.com", guest_uuid)
        self.assertTrue(pL.getGuestbyUUID(guest_uuid)['email'] == "GuestUserTest4@test.com")
    def test_getGuestByUUID(self): # attempt to retrieve guest by UUID
        user_uuid = pL.insertUser("GuestUserTest5@test.com")
        guest_uuid = pL.insertGuestwithUUID(user_uuid, "Claire", "B.", "Test", "GuestUserTest5@test.com", "555-7745", "10 Test Lane", "Testville", "Tenesssee", "00235")
        self.assertTrue(pL.getGuestbyUUID(guest_uuid) != None)
    def test_getGuests(self): # Add two guests, attempt to retrieve all guests, make sure both are present
        userA_uuid = pL.insertUser("GuestUserTest6@test.com")
        userB_uuid = pL.insertUser("GuestUserTest7@test.com")
        guestA_uuid = pL.insertGuestwithUUID(userA_uuid, "Bruce", "Z.", "Test", "GuestUserTest6@test.com", "555-7746", "9 Test Lane", "Testville", "Tenesssee", "00235")
        guestB_uuid = pL.insertGuestwithUUID(userB_uuid, "Mary", "X.", "Test", "GuestUserTest7@test.com", "555-7746", "9 Test Lane", "Testville", "Tenesssee", "00235")
        presence = 0
        guests = pL.getGuests()
        for guest in guests:
            if guest['uuid'] == guestA_uuid or guest['uuid'] == guestB_uuid:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getGuestByName(self): # attempt to retrieve guest by first and last name
        user_uuid = pL.insertUser("GuestUserTest8@test.com")
        guest_uuid = pL.insertGuestwithUUID(user_uuid, "Joseph", "E.", "Test", "GuestUserTest8@test.com", "555-9774", "40 Test Lane", "Testville", "Tenesssee", "00235")
        self.assertTrue(pL.getGuestbyName("Joseph", "Test") != None)

class TestPostgresLibrarySessionMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        Sessions = pL.getSessions()
        for Session in Sessions:
            if Session['token'] == "TOKENABCDEF":
                pL.deleteSession(Session['uuid'])
        Users = pL.getUsers()
        for User in Users:
            if str.startswith(User['email'], "SessionUserTest"):
                pL.deleteUser(User['uuid'])
    def test_insertSession(self): # attempt to insert a Session
        user_uuid = pL.insertUser("SessionUserTest1@test.com")
        sessUUID = pL.insertSession(user_uuid, "TOKENABCDEF", "0.0.0.123")
        self.assertTrue(sessUUID != None)
    def test_deleteSession(self): # attempt to delete a Session
        user_uuid = pL.insertUser("SessionUserTest2@test.com")
        sessUUID = pL.insertSession(user_uuid, "TOKENABCDEF", "0.0.0.123")
        pL.deleteSession(sessUUID)
        self.assertTrue(pL.getSessionbyUUID(sessUUID) == None)
    def test_getSessionbyUUID(self): # attempt to get a Session by UUID
        user_uuid = pL.insertUser("SessionUserTest3@test.com")
        sessUUID = pL.insertSession(user_uuid, "TOKENABCDEF", "0.0.0.123")
        self.assertTrue(pL.getSessionbyUUID(sessUUID) != None)
    def test_getSessions(self): # add two users, attempt to get all Sessions, confirm their presence
        userA_uuid = pL.insertUser("SessionUserTest4@test.com")
        userB_uuid = pL.insertUser("SessionUserTest5@test.com")
        sessAUUID = pL.insertSession(userA_uuid, "TOKENABCDEF", "0.0.0.123")
        sessBUUID = pL.insertSession(userB_uuid, "TOKENABCDEF", "0.0.0.123")
        sessions = pL.getSessions()
        presence = 0
        for session in sessions:
            if session['uuid'] == sessAUUID or session['uuid'] == sessBUUID:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_TimeRangebyUUID(self): # get time range from session, verify times exist, verify expires > created
        user_uuid = pL.insertUser("SessionUserTest6@test.com")
        sessUUID = pL.insertSession(user_uuid, "TOKENABCDEF", "0.0.0.123")
        created, expired = pL.getTimeRangebyUUID(sessUUID)
        self.assertTrue(created != 0)
        self.assertTrue(expired != 0)
        self.assertTrue(expired > created)
    def test_updateSessionvalue(self): # insert Session, change value to False verify, then to True verify
        user_uuid = pL.insertUser("SessionUserTest7@test.com")
        sessUUID = pL.insertSession(user_uuid, "TOKENABCDEF", "0.0.0.123")
        pL.updateSessionValue(False, sessUUID)
        self.assertFalse(pL.getSessionbyUUID(sessUUID)['invalidated'])
        pL.updateSessionValue(True, sessUUID)
        self.assertTrue(pL.getSessionbyUUID(sessUUID)['invalidated'])

class TestPostgresLibraryRoomMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        Rooms = pL.getRooms()
        for Room in Rooms:
            if Room['floor'] == "Test":
                pL.deleteRoom(Room['uuid'])
    def test_insertRoom(self): # attempt to insert a room
        ruuid = pL.insertRoom("Test Room #1", "1", "Test")
        self.assertTrue(ruuid != None)
    def test_deleteRoom(self): # attempt to deleta a room
        ruuid = pL.insertRoom("Test Room #2", "2", "Test")
        pL.deleteRoom(ruuid)
        self.assertTrue(pL.getRoombyUUID(ruuid) == None)
    def test_getRooms(self): # add two rooms, attempt to get all rooms, confim presence of both
        ruuid1 = pL.insertRoom("Test Room #3", "3", "Test")
        ruuid2 = pL.insertRoom("Test Room #4", "4", "Test")
        rooms = pL.getRooms()
        presence = 0
        for room in rooms:
            if room['uuid'] == ruuid1 or room['uuid'] == ruuid2:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getRoombyUUID(self): # add a room, find it using its uuid
        ruuid = pL.insertRoom("Test Room #5", "5", "Test")
        self.assertTrue(pL.getRoombyUUID(ruuid) != None)

class TestPostgressLibraryPeripheralMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        Peris = pL.getPeripherals()
        for Peri in Peris:
            if str.startswith(Peri['name'], "Test"):
                pL.deletePeripheral(Peri['uuid'])
        Rooms = pL.getRooms()
        for Room in Rooms:
            if Room['floor'] == "PTest":
                pL.deleteRoom(Room['uuid'])
    def test_insertPeripheral(self):
        ruuid = pL.insertRoom("PTest Room", "1", "PTest")
        puuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        self.assertTrue(puuid != None)
    def test_deletePeripheral(self):
        ruuid = pL.insertRoom("PTest Room", "2", "PTest")
        puuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        pL.deletePeripheral(puuid)
        self.assertTrue(pL.getPeripheralbyUUID(puuid) == None)
    def test_getPeripheralbyUUID(self):
        ruuid = pL.insertRoom("PTest Room", "3", "PTest")
        puuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        self.assertTrue(pL.getPeripheralbyUUID(puuid) != None)
    def test_getPeripheralsbyRoom(self):
        ruuid = pL.insertRoom("PTest Room", "4", "Test")
        p1uuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        p2uuid = pL.insertPeripheral(ruuid, "Test", "Camera", "True", "True", 1.0, None)
        peris = pL.getPeripheralsbyRoom(ruuid)
        presence = 0
        for peri in peris:
            presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getStatusbyUUID(self):
        ruuid = pL.insertRoom("PTest Room", "5", "PTest")
        puuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        self.assertTrue(pL.getStatusbyUUID(puuid))
    def test_getPeripherals(self):
        r1uuid = pL.insertRoom("PTest Room", "6", "PTest")
        r2uuid = pL.insertRoom("PTest Room", "7", "PTest")
        p1uuid = pL.insertPeripheral(r1uuid, "Test", "Light", "True", "True", 1.0, None)
        p2uuid = pL.insertPeripheral(r2uuid, "Test", "Camera", "True", "True", 1.0, None)
        AllPeris = pL.getPeripherals()
        presence = 0
        for Peri in AllPeris:
            if Peri['uuid'] == p1uuid or Peri['uuid'] == p2uuid:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getPeripheralsbyType(self):
        ruuid = pL.insertRoom("PTest Room", "8", "PTest")
        p1uuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        p2uuid = pL.insertPeripheral(ruuid, "Test", "Camera", "True", "True", 1.0, None)
        Lights = pL.getPeripheralsbyType("Light")
        p1present = False
        p2present = False
        for Light in Lights:
            if Light['uuid'] == p1uuid:
                p1present = True
            if Light['uuid'] == p2uuid:
                p2present = True
        self.assertTrue(p1present and not p2present)
        Cameras = pL.getPeripheralsbyType("Camera")
        p1present = False
        p2present = False
        for Camera in Cameras:
            if Camera['uuid'] == p1uuid:
                p1present = True
            if Camera['uuid'] == p2uuid:
                p2present = True
        self.assertTrue(not p1present and p2present)
    def test_updatePeripheralActive(self):
        ruuid = pL.insertRoom("PTest Room", "9", "PTest")
        puuid = pL.insertPeripheral(ruuid, "Test", "Light", "True", "True", 1.0, None)
        pL.updatePeripheralActive( "False", puuid)
        self.assertFalse(pL.getPeripheralbyUUID(puuid)['active'])
        pL.updatePeripheralActive( "True", puuid)
        self.assertTrue(pL.getPeripheralbyUUID(puuid)['active'])

class TestPostgressLibraryRoomServiceItemMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        RRSIs = pL.getRoomServiceItems()
        for RRSI in RRSIs:
            if str.startswith(RRSI['name'], "Test"):
                pL.deleteRoomServiceItem(RRSI['uuid'])
    def test_insertRoomServiceItem(self):
        rrsiuuid = pL.insertRoomServiceItem("Test Room Service Item 1", "Description", "3.50", None, "0000123")
        self.assertTrue(rrsiuuid != None)
    def test_deleteRoomServiceItem(self):
        rrsiuuid = pL.insertRoomServiceItem("Test Room Service Item 2", "Description", "3.50", None, "0000123")
        pL.deleteRoomServiceItem(rrsiuuid)
        self.assertTrue(pL.getRoomServiceItembyUUID(rrsiuuid) == None)
    def test_getRoomServiceItembyUUID(self):
        rrsiuuid = pL.insertRoomServiceItem("Test Room Service Item 3", "Description", "3.50", None, "0000123")
        RRSI = pL.getRoomServiceItembyUUID(rrsiuuid)
        self.assertTrue(RRSI != None)
    def test_getRoomServiceItems(self):
        rrsiuuid1 = pL.insertRoomServiceItem("Test Room Service Item 4", "Description", "3.50", None, "0000123")
        rrsiuuid2 = pL.insertRoomServiceItem("Test Room Service Item 5", "Description", "3.50", None, "0000123")
        presence = 0
        RRSIs = pL.getRoomServiceItems()
        for RRSI in RRSIs:
            if RRSI['uuid'] == rrsiuuid1 or RRSI['uuid'] == rrsiuuid2:
                presence = presence + 1
        self.assertTrue(presence == 2)

class TestPostgressLibraryRoomServiceRequestMethods(unittest.TestCase):
    _user = None
    _room = None
    _type = None
    @classmethod
    def setUp(self):
        RSR = pL.getRoomServiceRequests()
        for rsr in  RSR:
            pL.deleteRoomServiceRequest(rsr['uuid'])
        Users = pL.getUsers()
        for user in Users:
            if str.startswith(user['email'], "TestingEmail"):
                pL.deleteUser(user['uuid'])
        Rooms = pL.getRooms()
        for room in Rooms:
            if str.startswith(room['floor'], "Test"):
                pL.deleteRoom(room['uuid'])
        TPs = pL.getRoomServiceItems()
        for TP in TPs:
            if str.startswith(TP['name'], "Test"):
                pL.deleteRoomServiceItem(TP['uuid'])
        self._user = pL.insertUser("TestingEmail@test.com")
        self._room = pL.insertRoom("Test Room", "12", "Test")
        self._type = pL.insertRoomServiceItem("Test Room Service Item 6", "Description", "3.50", None, "0000123")
    @classmethod
    def tearDown(self):
        RSR = pL.getRoomServiceRequests()
        for rsr in  RSR:
            pL.deleteRoomServiceRequest(rsr['uuid'])
    def test_insertRoomServiceRequest(self):
        RSR = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1018", None, "350", False)
        self.assertTrue(RSR != None)
    def test_deleteRoomServiceRequest(self):
        RSR = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1018", None, "350", False)
        pL.deleteRoomServiceRequest(RSR)
        self.assertTrue(pL.getRoomServiceRequestbyUUID(RSR) == None)
    def test_getRoomServiceRequests(self):
        RSRA = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1018", None, "350", False)
        RSRB = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1018", None, "350", False)
        RoomServiceRequests = pL.getRoomServiceRequests()
        presence = 0
        for RSR in RoomServiceRequests:
            if RSR['uuid'] == RSRA  or RSR['uuid'] == RSRB:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getRoomServiceRequestsbyUUID(self):
        RSR = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1018", None, "350", False)
        self.assertTrue(pL.getRoomServiceRequestbyUUID(RSR))
    def test_getRoomServiceRequestUncompleted(self):
        RSRA = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1000", None, "100", False)
        RSRB = pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1001", None, "900", True)
        Uncompleted = pL.getRoomServiceRequestsUncompleted()
        present = 1
        for Uncomp in Uncompleted:
            if Uncomp['uuid'] == RSRA:
                present = present + 1
            if Uncomp['uuid'] == RSRB:
                present = present - 1
        self.assertTrue(present == 2)
    def test_updateRoomServiceRequestCompleted(self):
        RSR =  pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1000", None, "100", False)
        pL.updateRoomServiceRequestCompleted(True, RSR)
        self.assertTrue(pL.getRoomServiceRequest(RSR)['completed'])
        pL.updateRoomServiceRequestCompleted(False, RSR)
        self.assertFalse(pL.getRoomServiceRequest(RSR)['completed'])
    def test_updateRoomServiceRequestCompleted(self):
        RSR =  pL.insertRoomServiceRequest(self._room, self._user, self._type, "Feb-26-1000", None, "100", False)
        pL.updateRoomServiceRequestCompleted(True, RSR)
        self.assertTrue(pL.isCompletedRoomServicebyUUID(RSR))
        pL.updateRoomServiceRequestCompleted(False, RSR)
        self.assertFalse(pL.isCompletedRoomServicebyUUID(RSR))

class TestPostgressLibraryMaintenanceRequestMethods(unittest.TestCase):
    _user = None
    _room = None
    @classmethod
    def setUp(self):
        RSR = pL.getMaintenanceRequests()
        for rsr in  RSR:
            pL.deleteMaintenanceRequest(rsr['uuid'])
        Users = pL.getUsers()
        for user in Users:
            if str.startswith(user['email'], "TestingEmail"):
                pL.deleteUser(user['uuid'])
        Rooms = pL.getRooms()
        for room in Rooms:
            if str.startswith(room['floor'], "Test"):
                pL.deleteRoom(room['uuid'])
        self._user = pL.insertUser("TestingEmail@test.com")
        self._room = pL.insertRoom("Test Room", "12", "Test")
    @classmethod
    def tearDown(self):
        RSR = pL.getMaintenanceRequests()
        for rsr in  RSR:
            pL.deleteMaintenanceRequest(rsr['uuid'])
    def test_insertMaintenanceRequest(self):
        RSR = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1018", None, "350", False)
        self.assertTrue(RSR != None)
    def test_deleteMaintenanceRequest(self):
        RSR = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1018", None, "350", False)
        pL.deleteMaintenanceRequest(RSR)
        self.assertTrue(pL.getMaintenanceRequestbyUUID(RSR) == None)
    def test_getMaintenanceRequests(self):
        RSRA = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1018", None, "350", False)
        RSRB = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1018", None, "350", False)
        MaintenanceRequests = pL.getMaintenanceRequests()
        presence = 0
        for RSR in MaintenanceRequests:
            if RSR['uuid'] == RSRA  or RSR['uuid'] == RSRB:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getMaintenanceRequestsbyUUID(self):
        RSR = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1018", None, "350", False)
        self.assertTrue(pL.getMaintenanceRequestbyUUID(RSR))
    def test_getMaintenanceRequestUncompleted(self):
        RSRA = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1000", None, "100", False)
        RSRB = pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1001", None, "900", True)
        Uncompleted = pL.getMaintenanceRequestsUncompleted()
        present = 1
        for Uncomp in Uncompleted:
            if Uncomp['uuid'] == RSRA:
                present = present + 1
            if Uncomp['uuid'] == RSRB:
                present = present - 1
        self.assertTrue(present == 2)
    def test_updateMaintenanceRequestCompleted(self):
        RSR =  pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1000", None, "100", False)
        pL.updateMaintenanceRequestCompleted(True, RSR)
        self.assertTrue(pL.getMaintenanceRequest(RSR)['completed'])
        pL.updateMaintenanceRequestCompleted(False, RSR)
        self.assertFalse(pL.getMaintenanceRequest(RSR)['completed'])
    def test_updateMaintenanceRequestCompleted(self):
        RSR =  pL.insertMaintenanceRequest(self._room, self._user, "Feb-26-1000", None, "100", False)
        pL.updateMaintenanceRequestCompleted(True, RSR)
        self.assertTrue(pL.isCompletedMaintenanceRequestByUUID(RSR))
        pL.updateMaintenanceRequestCompleted(False, RSR)
        self.assertFalse(pL.isCompletedMaintenanceRequestByUUID(RSR))

class TestPostgressLibraryTransactionMethods(unittest.TestCase):
    _user = None
    _room = None
    @classmethod
    def setUp(self):
        Ts = pL.getTransactions()
        for T in  Ts:
            pL.deleteTransaction(T['uuid'])
        Users = pL.getUsers()
        for user in Users:
            if str.startswith(user['email'], "TestingEmail"):
                pL.deleteUser(user['uuid'])
        Rooms = pL.getRooms()
        for room in Rooms:
            if str.startswith(room['floor'], "Test"):
                pL.deleteRoom(room['uuid'])
        self._user = pL.insertUser("TestingEmail@test.com")
        self._room = pL.insertRoom("Test Room", "12", "Test")
    @classmethod
    def tearDown(self):
        Ts = pL.getTransactions()
        for T in  Ts:
            pL.deleteTransaction(T['uuid'])
    def test_insertTransaction(self):
        Tuuid = pL.insertTransaction(self._room, self._user, "Test Description", 20)
        self.assertTrue(Tuuid != None)
    def test_deleteTransaction(self):
        Tuuid = pL.insertTransaction(self._room, self._user, "Test Description", 20)
        pL.deleteTransaction(Tuuid)
        self.assertTrue(pL.getTransactionbyUUID(Tuuid) == None)
    def test_getTransactions(self):
        Tuuid1 = pL.insertTransaction(self._room, self._user, "Test Description", 20)
        Tuuid2 = pL.insertTransaction(self._room, self._user, "Test Description", 20)
        Trans = pL.getTransactions()
        presence = 0
        for Tran in Trans:
            if Tran['uuid'] == Tuuid1 or Tran['uuid'] == Tuuid2:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getTransactionbyUUID(self):
        Tuuid = pL.insertTransaction(self._room, self._user, "Test Description", 30)
        self.assertTrue(pL.getTransactionbyUUID(Tuuid) != None)

class TestPostgressLibraryReservationMethods(unittest.TestCase):
    _guest = None
    _room = None
    @classmethod
    def setUp(self):
        Rs = pL.getReservations()
        for R in  Rs:
            pL.deleteReservation(R['uuid'])
        Guests = pL.getGuests()
        for guest in Guests:
            if str.startswith(guest['last_name'], "TestReservation"):
                pL.deleteGuest(guest['uuid'])
        Rooms = pL.getRooms()
        for room in Rooms:
            if str.startswith(room['floor'], "Test"):
                pL.deleteRoom(room['uuid'])
        self._guest = pL.insertGuest("Sam", "A.", "TestReservation", "TestingEmail@test.com", "555-1234", "12 Test Lane", "Testville", "Tenesse", "00022")
        self._room = pL.insertRoom("Test Room", "12", "Test")
    @classmethod
    def tearDown(self):
        Rs = pL.getReservations()
        for R in  Rs:
            pL.deleteReservation(R['uuid'])
    def test_insertReservation(self):
        Ruuid = pL.insertReservation(self._room, self._guest, None, None, False, False)
        self.assertTrue(Ruuid != None)
    def test_deleteReservation(self):
        Ruuid = pL.insertReservation(self._room, self._guest, None, None, False, False)
        pL.deleteReservation(Ruuid)
        self.assertTrue(pL.getReservationbyUUID(Ruuid) == None)
    def test_getReservations(self):
        Ruuid1 = pL.insertReservation(self._room, self._guest, None, None, False, False)
        Ruuid2 = pL.insertReservation(self._room, self._guest, None, None, False, False)
        Reserves = pL.getReservations()
        presence = 0
        for Reserve in Reserves:
            if Reserve['uuid'] == Ruuid1 or Reserve['uuid'] == Ruuid2:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getReservationbyUUID(self):
        Ruuid = pL.insertReservation(self._room, self._guest, None, None, False, False)
        self.assertTrue(pL.getReservationbyUUID(Ruuid) != None)
    def test_checkInReservation(self):
        Ruuid = pL.insertReservation(self._room, self._guest, None, None, False, False)
        self.assertFalse(pL.getReservationbyUUID(Ruuid)['check_in'])
        pL.checkInReservation(Ruuid, True)
        self.assertTrue(pL.getReservationbyUUID(Ruuid)['check_in'])
    def test_checkInReservation(self):
        Ruuid = pL.insertReservation(self._room, self._guest, None, None, False, False)
        self.assertFalse(pL.getReservationbyUUID(Ruuid)['check_out'])
        pL.checkOutReservation(Ruuid, True)
        self.assertTrue(pL.getReservationbyUUID(Ruuid)['check_out'])

class TestPostgressLibraryEmployeeMethods(unittest.TestCase):
    @classmethod
    def setUp(self):
        Employees = pL.getEmployees()
        for Employee in Employees:
            if str.startswith(Employee['last_name'], "Test"):
                pL.deleteEmployee(Employee['uuid'])
        Users = pL.getUsers()
        for User in Users:
            if str.startswith(User['email'], "TestingEmail"):
                pL.deleteUser(User['uuid'])
    @classmethod
    def tearDown(self):
        Employees = pL.getEmployees()
        for Employee in Employees:
            if str.startswith(Employee['last_name'], "Test"):
                pL.deleteEmployee(Employee['uuid'])
    def test_insertEmployee(self):
        user = pL.insertUser("TestingEmail0@test.com")
        empuuid = pL.insertEmployee(user, "Test", "Test", False)
        self.assertTrue(empuuid != None)
    def test_deleteEmployee(self):
        user = pL.insertUser("TestingEmail1@test.com")
        empuuid = pL.insertEmployee(user, "Test", "Test", False)
        pL.deleteEmployee(empuuid)
        self.assertTrue(pL.getEmployeebyUUID(empuuid) == None)
    def test_getEmployees(self):
        user1 = pL.insertUser("TestingEmail1@test.com")
        user2 = pL.insertUser("TestingEmail2@test.com")
        empuuid1 = pL.insertEmployee(user1, "Test", "Test", False)
        empuuid2 = pL.insertEmployee(user2, "Test", "Test", False)
        presence = 0
        Empls = pL.getEmployees()
        for Empl in Empls:
            if Empl['uuid'] == empuuid1 or Empl['uuid'] == empuuid2:
                presence = presence + 1
        self.assertTrue(presence == 2)
    def test_getEmployeebyUUID(self):
        user = pL.insertUser("TestingEmail3@test.com")
        empuuid = pL.insertEmployee(user, "Test", "Test", False)
        self.assertTrue(pL.getEmployeebyUUID(empuuid) != None)
    def test_isAdminEmployee(self):
        user1 = pL.insertUser("TestingEmail4@test.com")
        user2 = pL.insertUser("TestingEmail5@test.com")
        empuuid1 = pL.insertEmployee(user1, "Test", "Test", False)
        empuuid2 = pL.insertEmployee(user2, "Test", "Test", True)
        self.assertFalse(pL.isAdminEmployee(empuuid1))
        self.assertTrue(pL.isAdminEmployee(empuuid2))
    def test_updateEmployeeAdmin(self):
        user = pL.insertUser("TestingEmail6@test.com")
        empuuid = pL.insertEmployee(user, "Test", "Test", False)
        pL.updateEmployeeAdmin( True, empuuid)
        self.assertTrue(pL.isAdminEmployee(empuuid))
        pL.updateEmployeeAdmin( False, empuuid)
        self.assertFalse(pL.isAdminEmployee(empuuid))

if __name__ == '__main__':
    unittest.main()