from datetime import datetime, timedelta

class ConferenceHall:
    def _init_(self, location, availability, cost_per_day):
        self.location = location
        self.availability = availability
        self.booked = False
        self.cost_per_day = cost_per_day

class ResourceBookingSystem:
    def _init_(self):
        self.halls = {}
        self.admin_username = "admin"
        self.admin_password = "admin@123"
        self.user_username = "user"
        self.user_password = "user@123"
    
    def login(self):
        user_type = input("Are you user or admin: ")
        while True:
            username = input("Enter username: ")
            password = input("Enter password: ")

            if user_type == 'admin' and username == self.admin_username and password == self.admin_password:
                print("Login successful! Welcome, Admin.")
                return True, False
            elif user_type == 'user' and username == self.user_username and password == self.user_password:
                print(f"Login successful! Welcome, {username}.")
                return False, True
            else:
                print("Invalid credentials. Access denied. Please try again.")

    def show_menu(self, admin_access):
        if admin_access:
            print("\nAdmin Menu:")
            print("1. Create a resource")
            print("2. View all resources")
            print("3. Update a resource")
            print("4. Delete a resource")
            print("5. Exit")
        else:
            print("\nUser Menu:")
            print("1. View all resources")
            print("2. Book a resource")
            print("3. Cancel booking")
            print("4. Exit")

    def run(self):
        admin_access, user_access = self.login()
        if not admin_access and not user_access:
            return

        while True:
            if admin_access:
                self.show_menu(True)
                admin_choice = int(input("Enter your choice (1-5): "))
                if admin_choice == 5:
                    y = input("Do you want to continue (yes/no)? ")
                    if y.lower() == "yes":
                        self.run()
                    else:
                        exit()
                else:
                    self.process_admin_choice(admin_choice)
            else:
                self.show_menu(False)
                user_choice = int(input("Enter your choice (1-4): "))
                if user_choice == 4:
                    n = input("Do you want to continue (yes/no)? ")
                    if n.lower() == "yes":
                        self.run()
                    else:
                        exit()
                else:
                    self.process_user_choice(user_choice)

    def process_admin_choice(self, choice):
        if choice == 1:
            self.create_hall_availability()
        elif choice == 2:
            self.view_hall_availability()
        elif choice == 3:
            self.update_hall_details()
        elif choice == 4:
            self.delete_hall()

    def process_user_choice(self, choice):
        if choice == 1:
            self.view_hall_availability()
        elif choice == 2:
            self.book_hall()
        elif choice == 3:
            self.cancel_booking()

    def create_hall_availability(self):
        location = input("Enter the location of the conference hall: ")
        availability = input("Enter the availability of the conference hall (YYYY-MM-DD): ")
        cost_per_day = float(input("Enter the cost per day for the conference hall: "))

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime("%Y-%m-%d")

        if datetime.strptime(availability, "%Y-%m-%d") < tomorrow:
            print("Invalid date. Availability date must be from tomorrow onwards.")
            return

        if location not in self.halls:
            self.halls[location] = []
        
        self.halls[location].append(ConferenceHall(location, availability, cost_per_day))
        print(f"Conference hall created successfully at {location}.")

    def view_hall_availability(self):
        if not self.halls:
            print("No conference halls have been created yet.")
        else:
            print("Available Conference Halls:")
            for location, halls in self.halls.items():
                print(f"Location: {location}")
                for hall in halls:
                    print(f"Availability: {hall.availability}, Cost per day: {hall.cost_per_day}, Booked: {hall.booked}")
                print("---------------")

    def update_hall_details(self):
        location = input("Enter the location of the conference hall to update: ")
        if location in self.halls:
            availability = input("Enter the date to update the hall (YYYY-MM-DD): ")

            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")

            if datetime.strptime(availability, "%Y-%m-%d") < tomorrow:
                print("Invalid date. Availability date must be from tomorrow onwards.")
                return

            for hall in self.halls[location]:
                if hall.availability == availability:
                    cost_per_day = float(input("Enter the new cost per day: "))
                    hall.cost_per_day = cost_per_day
                    print(f"Conference hall details updated successfully at {location}.")
                    return
            print(f"No hall found for {availability} at {location}.")   
        else:
            print(f"No conference hall found at {location}.")

    def delete_hall(self):
        location = input("Enter the location of the conference hall to delete: ")
        if location in self.halls:
            availability = input("Enter the date to delete the hall (YYYY-MM-DD): ")
            for hall in self.halls[location]:
                if hall.availability == availability:
                    self.halls[location].remove(hall)
                    print(f"Hall at {location} for {availability} deleted successfully.")
                    return
            print(f"No hall found for {availability} at {location}.")
        else:
            print(f"No conference hall found at {location}.")

    def book_hall(self):
        location = input("Enter the location of the conference hall to book: ")
        if location in self.halls:
            availability = input("Enter the date to book the hall (YYYY-MM-DD): ")
            for hall in self.halls[location]:
                if hall.availability == availability:
                    if not hall.booked:
                        hall.booked = True
                        print(f"Hall booked successfully for the entire day on {availability}.")
                    else:
                        print("Hall already booked for the entire day.")
                    return
            print(f"No available hall found for {availability} at {location}.")
        else:
            print(f"No conference hall found at {location}.")

    def cancel_booking(self):
        location = input("Enter the location of the conference hall to cancel booking: ")
        if location in self.halls:
            availability = input("Enter the date to cancel the booking (YYYY-MM-DD): ")
            for hall in self.halls[location]:
                if hall.availability == availability and hall.booked:
                    hall.booked = False
                    print(f"Booking canceled successfully for the entire day on {availability}.")
                    return
            print(f"No booking found for {availability} at {location} or already canceled.")
        else:
            print(f"No conference hall found at {location}.")

if __name__ == "_main_":
    booking_system = ResourceBookingSystem()
    booking_system.run()