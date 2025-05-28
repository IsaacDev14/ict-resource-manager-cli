from app.database import SessionLocal
from app.models.device import Device
from app.models.location import Location
from sqlalchemy.exc import SQLAlchemyError

db = SessionLocal()  # creates a db session

# function to add a new device
def add_device():
    # getting device info from user
    name = input("Device Name: ")
    device_type = input("Device Type (e.g., Laptop, Router): ")
    serial_number = input("Serial Number: ")
    status = input("Status (available, assigned, damaged): ")
    location_id = input("Location ID (integer): ")

    # create a new Device object using the provided data
    new_device = Device(
        name=name,
        device_type=device_type,
        serial_number=serial_number,
        status=status,
        location_id=int(location_id) if location_id else None
    )

    # Try to save the device to the database
    try:
        db.add(new_device)
        db.commit()
        print("✅ Device added successfully.")
    except SQLAlchemyError as e:
        db.rollback()
        print("❌ Error adding device:", e)

def view_devices():
    try:
        devices = db.query(Device).all()  # Fetch all device records
        if not devices:
            print("No devices found.")
            return

        print("\nList of Devices:")
        print("-" * 70)
        for device in devices:
            print(f"ID: {device.id} | Name: {device.name} | Type: {device.device_type} | Serial: {device.serial_number}")
            print("-" * 70)
    except SQLAlchemyError as e:
        print("❌ Error retrieving devices:", e)

def add_location():
    session = SessionLocal()
    try:
        name = input("Location Name: ")
        description  = input("Location Description: ")
        new_location = Location(name=name, description=description)
        session.add(new_location)
        session.commit()
        print("✅ Location added successfully.")
    except Exception as e:
        session.rollback()
        print(f"❌ Error adding location: {e}")
    finally:
        session.close()


def view_locations():
    session = SessionLocal()
    try:
        locations = session.query(Location).all()
        if not locations:
            print("No locations found.")
            return
        print("\nList of Locations:")
        print("-" * 70)
        for loc in locations:
            print(f"ID: {loc.id} | Name: {loc.name} | Description: {loc.description}")
            print("-" * 70)
    except Exception as e:
        print(f"❌ Error viewing locations: {e}")
    finally:
        session.close()






if __name__ == "__main__":
    while True:
        print("\n1. Add Device")
        print("2. View Devices")
        print("3. Add Location")
        print("4. View Locations")
        print("q. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            add_device()
        elif choice == "2":
            view_devices()
        elif  choice == "3":
            add_location()
        elif  choice == "4":
            view_locations() 
        elif choice == "q":
            print("👋 Exiting program...")
            break
        else:
            print("Invalid option, please try again.")
