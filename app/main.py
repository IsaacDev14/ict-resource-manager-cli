from app.database import SessionLocal
from app.models.device import Device
from sqlalchemy.exc import SQLAlchemyError

db = SessionLocal() #creates a db session

#function to add a new device
def add_device():
    #getting ddevice infor from user
    name = input("Device Name: ")
    device_type = input("Device Type (e.g, Laptop, Router): ")
    serial_number = input("Serial Number: ")
    status =   input("Status  (available, assigned, damaged): ")
    location_id = input("Location ID (integer): ")

    #create a new Device object using the provided data
    new_device = Device(
        name = name,
        device_type = device_type,
        serial_number = serial_number,
        status = status,
        location_id = int(location_id) if location_id  else None
    ) 

    # Try to save the device to the database
    try:
        db.add(new_device)
        db.commit()
        print("✅ Device added successfully.")
    except SQLAlchemyError as e:
        db.rollback()
        print("❌ Error adding device:", e)

# Call the add_device function directly for now
# if __name__ == "__main__":
#     add_device()

def view_devices():
    try:
        devices = db.query(Device).all #Fetch all device records
        if not devices:
            print("No devices found.")
            return
        
        print("\nList of Devices:")
        print("=" * 40 )
        for  device in devices:
            print(f"ID: {device.id} | Name: {device.name} | Type: {device.device_typeb} | serial: {device.serial_number}")
            print("=" * 40)
    except SQLAlchemyError as e:
        print("❌ Error retrieving devices:", e)

    if  __name__ == "__main__":
        print("1. Add Device")
        print("2. View Devices")
        choice = input("choose an option: ")

        if choice == "1"
            add_device()
        elif choice == "2":
            view_devices()
        else:
            print("Invalid option")