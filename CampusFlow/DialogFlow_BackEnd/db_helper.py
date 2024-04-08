import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="campusflow"
)

def get_bus_fee(destination_name):
    cursor = cnx.cursor()

    query = f"SELECT Fees FROM bus_timings WHERE BoardingPoint = '{destination_name}' limit 1"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None

def get_bus_time(destination_name, bus_name):
    cursor = cnx.cursor()

    query = f"SELECT Time FROM bus_timings WHERE BoardingPoint = '{destination_name}' and BusNo = '{bus_name}' limit 1"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None


def get_all_bus_names(destination_name):
    cursor = cnx.cursor()

    query = f"SELECT BusNo FROM bus_timings WHERE BoardingPoint = '{destination_name}'"
    cursor.execute(query)

    results = cursor.fetchall()

    cursor.close()

    if results:
        return [result[0] for result in results]
    else:
        return None


def get_room_info(room_name):
    cursor = cnx.cursor()

    room_name = room_name[0] if isinstance(room_name, list) else room_name

    room_name = room_name.strip("[]")

    query = f"SELECT BlockName, Floor, Landmark FROM roomloc WHERE RoomNo like '%{room_name}%' LIMIT 1"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return {
            'BlockName': result[0],
            'Floor': result[1],
            'Landmark': result[2]
        }
    else:
        return None

def get_lec_info(lec_name):
    cursor = cnx.cursor()

    query = f"SELECT BlockName, Floor, Landmark FROM roomloc WHERE RoomNo like '%{lec_name}%' LIMIT 1"
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return {
            'BlockName': result[0],
            'Floor': result[1],
            'Landmark': result[2]
        }
    else:
        return None



def get_link_helper(link_name, link_type):
    cursor = cnx.cursor()

    if link_type=="":
        query = f"SELECT FileLink FROM file_links WHERE FileName like '%{link_name}%' limit 1"
    else:
        query = f"SELECT FileLink FROM file_links WHERE FileName like '%{link_name} {link_type}%' limit 1"
        
    cursor.execute(query)

    result = cursor.fetchone()

    cursor.close()

    if result:
        return result[0]
    else:
        return None