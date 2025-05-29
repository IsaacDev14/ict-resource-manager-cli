from app.database import SessionLocal
from app.models.device import Device
from app.models.location import Location
from app.models.user import User
from datetime import date
from app.models.assignment import Assignment
from sqlalchemy.exc import SQLAlchemyError

db = SessionLocal()  # creates a db session

class Colors:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

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
        print(f"{Colors.GREEN}✅ Device added successfully.{Colors.RESET}")
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
        print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
        for device in devices:
            print(f"ID: {device.id} | Name: {device.name} | Type: {device.device_type} | Serial: {device.serial_number}")
            print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
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
        print(f"{Colors.GREEN}✅ Location added successfully.{Colors.RESET}")
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
        print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
        for loc in locations:
            print(f"ID: {loc.id} | Name: {loc.name} | Description: {loc.description}")
            print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
    except Exception as e:
        print(f"❌ Error viewing locations: {e}")
    finally:
        session.close()

def add_user():
    session = SessionLocal()
    try:
        name = input("Enter User Name: ")
        user_type = input("User Type (staff or department):")
        contact_info = input("Contact Info (email or phone):")

        new_user = User(name=name, user_type=user_type, contact_info=contact_info)
        session.add(new_user)
        session.commit()
        print(f"{Colors.GREEN}✅ User added successfully.{Colors.RESET}")

    except SQLAlchemyError as e:
        session.rollback()
        print("❌ failed to add user:", e)
    finally:
        session.close()

def view_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        if not users:
            print("No users found")
            return
        print("\nList Of users: ")
        print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
        for user in users:
            print(f"ID {user.id} | User Name:{user.name} | Type: {user.user_type} | Contact: {user.contact_info}" )
            print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
    except SQLAlchemyError as e:
        print(f"❌ Error Viewing Users: ", e)
    finally:
        session.close()

def update_user():
    session =  SessionLocal()
    try:
        user_id = input("Enter User ID to update: ").strip()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            print("❌ User not found.")
            return
        
        print(f"Current Name: {user.name}")
        new_name = input("New Name (leave blank to keep current): ").strip()
        if new_name:
            user.name = new_name

        print(f"Current Contact Info: {user.contact_info}")
        new_contact = input("New Contact Info (leave blank to keep current): ").strip()
        if new_contact:
            user.contact_info = new_contact

        session.commit()
        print(F"{Colors.GREEN}✅ User updated successfully.{Colors.RESET}")
    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Error updating user:", e)
    finally:
        session.close()

def delete_user():
    session = SessionLocal()
    try:
        user_id = input("Enter User ID to delete: ").strip()
        user = session.query(User).filter_by(id=user_id).first()

        if not user:
            print("❌ User not found.")
            return

        confirm = input(f"Are you sure you want to delete user '{user.name}'? (y/n): ").strip().lower()
        if confirm == "y":
            session.delete(user)
            session.commit()
            print(f"{Colors.GREEN}✅ User deleted successfully.{Colors.RESET}")
        else:
            print("ℹ️ Deletion cancelled.")
    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Error deleting user:", e)
    finally:
        session.close()

def assign_device_to_user():
    session = SessionLocal()
    try:
        device_id = input("Enter Device ID: ").strip()
        user_id = input("Enter User ID: ").strip()

        # Check if the device is already assigned and not returned
        existing = session.query(Assignment).filter_by(device_id=device_id, return_date=None).first()
        if existing:
            print("❌ Device is already assigned and not yet returned.")
            return

        new_assignment = Assignment(
            device_id=int(device_id),
            user_id=int(user_id),
            assigned_date=date.today()
        )
        session.add(new_assignment)

        # Update device status to "assigned"
        device = session.query(Device).get(int(device_id))
        if device:
            device.status = "assigned"
        session.commit()
        print(f"{Colors.GREEN}✅ Device assigned successfully.{Colors.RESET}")

    except SQLAlchemyError as e:
        session.rollback()
        print("❌ Error assigning device:", e)
    finally:
        session.close()

def view_assignments():
    session = SessionLocal()
    try:
        assignments = session.query(Assignment).all()
        if not assignments:
            print("No assignments found.")
            return

        
        print("\n📋 List of Assignments:")
        print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
        for a in assignments:
            user_name = a.user.name if a.user else "Unknown User"
            device_name = a.device.name if a.device else "Unknown Device"
            return_status = a.return_date if a.return_date else "Still Assigned"
            print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
            print(f"Device: {device_name} (ID: {a.device_id}) | User: {user_name} (ID: {a.user_id}) | Assigned: {a.assigned_date} | Returned: {return_status}")
        print(f"{Colors.GREEN}-{Colors.RESET}" * 100)
    except SQLAlchemyError as e:
        print("❌ Error retrieving assignments:", e)
    finally:
        session.close()





if __name__ == "__main__":
    while True:
        print(f"1. {Colors.CYAN}Add Device{Colors.RESET}")
        print(f"2. {Colors.MAGENTA}View Devices{Colors.RESET}")
        print(f"3. {Colors.CYAN}Add Location{Colors.RESET}")
        print(f"4. {Colors.MAGENTA}View Locations{Colors.RESET}")
        print(f"5. {Colors.CYAN}Add User{Colors.RESET}")
        print(f"6. {Colors.MAGENTA}View Users{Colors.RESET}")
        print(f"7. {Colors.YELLOW}Update User{Colors.RESET}")
        print(f"8. {Colors.RED}Delete User{Colors.RESET}")
        print(f"9. {Colors.BLUE}Assign Device to User{Colors.RESET}")
        print(f"10. {Colors.GREEN}View Assignments{Colors.RESET}")


        print("-" * 3)
        print(f"{Colors.RED}q. Exit{Colors.RESET}")
        choice = input("Choose an option: ")

        if choice == "1":
            add_device()
        elif choice == "2":
            view_devices()
        elif  choice == "3":
            add_location()
        elif  choice == "4":
            view_locations() 
        elif  choice == "5":
            add_user()
        elif  choice == "6":
            view_users()
        elif choice == "7":
            update_user()
        elif choice == "8":
            delete_user()
        elif choice == "9":
            assign_device_to_user()
        elif choice == "10":
            view_assignments()


        elif choice == "q":
            print("👋 Exiting program...")
            break
        else:
            print("Invalid option, please try again.")
