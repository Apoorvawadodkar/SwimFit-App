import mysql.connector
import numpy as np
import matplotlib.pyplot as plt


def connect_db():
    connection=mysql.connector.connect(host="localhost",user="root",password="Apoorva@",database="swimfit")
    return connection

#Admin registration
def register_admin(username, password_hash, email):
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = """Insert into admins (username, password_hash, email)
             values (%s, %s, %s)"""
    values = (username, password_hash, email)
    
    cursor.execute(sql, values)
    get_adminid="select admin_id from admins where username = %s"
    cursor.execute(get_adminid, (username,))
    result = cursor.fetchone()
    print("Your admin ID is",result,"DO NOT LOSE!")
    
    connection.commit()
    cursor.close()
    connection.close()
    

    print("User registered successfully!")

#User registration
def register_user(username, password_hash, email, fitness_level, goal, dietary_restrictions):
    connection = connect_db()
    cursor = connection.cursor()

    sql = """insert into users (username, password_hash, email, fitness_level, goal, dietary_restrictions)
             VALUES (%s, %s, %s, %s, %s, %s)"""
    values = (username, password_hash, email, fitness_level, goal, dietary_restrictions)

    cursor.execute(sql, values)
    get_userid ="select user_id from users where username = %s"
    cursor.execute(get_userid, (username,))
    result = cursor.fetchone()
    print("Your user ID is",result,"DO NOT LOSE!")
    connection.commit()

    cursor.close()
    connection.close()

    print("User registered successfully!")
    

#Admin Login
def login_admin(username, password_hash):
    connection = connect_db()
    cursor = connection.cursor()

    sql = "select password_hash from admins where username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result and password_hash == result[0]:
        print("Admin login successful!")
        return True
    else:
        print("Invalid admin username or password_hash.")
        return False

    cursor.close()
    connection.close()
    
#User login
def login_user(username, password_hash):
    connection = connect_db()
    cursor = connection.cursor()

    sql = "select password_hash from users where username = %s"
    cursor.execute(sql, (username,))
    result = cursor.fetchone()

    if result and password_hash == result[0]:
        print("User login successful!")
        return True
    else:
        print("Invalid user username or password_hash.")
        return False

    cursor.close()
    connection.close()
    
#Create Workout Plan
def create_workout_plan(admin_id, user_id, plan_details):
    connection = connect_db()
    cursor = connection.cursor()
    
    sql = "insert into workout_plans (admin_id, user_id, plan_details) values (%s, %s, %s)"
    values = (admin_id, user_id, plan_details)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    print("Workout plan created successfully!")

# Create a diet plan for a specific user, with dietary restrictions check
def create_diet_plan(admin_id, user_id, plan_details):
    connection = connect_db()
    cursor = connection.cursor()

    # Fetch dietary restrictions
    cursor.execute("SELECT dietary_restrictions FROM users WHERE user_id = %s", (user_id,))
    restrictions = cursor.fetchone()[0]
    print("User's dietary restrictions:", restrictions)

    # Admin can then proceed with creating the diet plan
    sql = "INSERT INTO diet_plans (admin_id, user_id, plan_details) VALUES (%s, %s, %s)"
    values = (admin_id, user_id, plan_details)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    print("Diet plan created successfully!")
    
#Update uder Details   
def update_user_details(admin_id, user_id, fitness_level=None, goal=None, dietary_restrictions=None):
    
    connection = connect_db()
    cursor = connection.cursor()

    if fitness_level:
        cursor.execute("update users set fitness_level = %s where user_id = %s", (fitness_level, user_id))
    if goal:
        cursor.execute("update users set goal = %s where user_id = %s", (goal, user_id))
    if dietary_restrictions:
        cursor.execute("update users set dietary_restrictions = %s where user_id = %s", (dietary_restrictions, user_id))
    

    connection.commit()
    cursor.close()
    connection.close()

    print("User details updated successfully!")
    
#Log Progress
def log_progress(user_id, workout_date, workout_summary, progress_notes):
    connection = connect_db()
    cursor = connection.cursor()

    sql = "insert into progress (user_id, workout_date, workout_summary, progress_notes) values (%s, %s, %s, %s)"
    values = (user_id, workout_date, workout_summary, progress_notes)

    cursor.execute(sql, values)
    connection.commit()

    cursor.close()
    connection.close()

    print("Progress logged successfully!")
    
#Get user Progress
def get_user_progress(user_id):
   
    connection = connect_db()
    cursor = connection.cursor()

    sql = "select * from progress where user_id = %s"
    cursor.execute(sql, (user_id,))
    progress = cursor.fetchall()

    cursor.close()
    connection.close()

    return progress

# Analyze performance with graph
def analyze_performance(user_id):
    connection = connect_db()
    cursor = connection.cursor()
    
    # Get event name and timings from the user
    event_name = input("Enter the event name (e.g., 50m Freestyle): ")
    timings = []

    while True:
        timing = input("Enter your timing for {} (or type 'done' to finish): ".format(event_name))
        if timing.lower() == 'done':
            break
        try:
            timings.append(float(timing))
        except ValueError:
            print("Please enter a valid number.")

    if not timings:
        print("No timings entered.")
        return

    # Analyze performance by plotting the timings
    timings = np.array(timings)
    races = np.arange(1, len(timings) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(races, timings, marker='o', linestyle='-', color='b')
    plt.title(f'{event_name} Performance')
    plt.xlabel('Race Number')
    plt.ylabel('Time (seconds/Minutes(Acoording to the user))')
    plt.grid(True)
    plt.show()

    # Additional analysis (e.g., average time)
    avg_time = np.mean(timings)
    print(f"Average time for {event_name}: {avg_time:.2f} seconds")

    cursor.close()
    connection.close()

    print("Performance analysis complete!")


#View workout plans
def view_plans(user_id):
    connection = connect_db()
    cursor = connection.cursor()
    
    cursor.execute("SELECT plan_details FROM workout_plans WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,))
    workout_plan = cursor.fetchone()
    
    if workout_plan:
        print(f"Workout Plan:\n{workout_plan[0]}")
    else:
        print("No workout plan found.")
        
    cursor.close()
    connection.close()

#View diet plans
def view_diet_plan(user_id):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT plan_details FROM diet_plans WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,))
    diet_plan = cursor.fetchone()

    if diet_plan:
        print(f"Diet Plan:\n{diet_plan[0]}")
    else:
        print("No diet plan found.")
    
    cursor.close()
    connection.close()
    
# This function displays a list of Frequently Asked Questions.
def show_faq():
    faqs = {
        "What is SwimFit?": "SwimFit is a personalized swimming fitness platform where users can track their workouts and diet plans.",
        "How do I register?": "You can register as a user or an admin by selecting the appropriate option from the main menu.",
        "How can I log my progress?": "Once logged in, go to the user menu and select 'Log Progress' to enter your workout details.",
        "Who can see my progress?": "Only you and admins can view the progress you've logged.",
        "What if I forget my User ID?": "Make sure to note down your User ID after registration. If lost, you will need to contact support."
    }

    print("Frequently Asked Questions:")
    for question, answer in faqs.items():
        print(f"\nQ: {question}\nA: {answer}")

    input("\nPress Enter to return to the main menu...")
        
#Main menu page.
def main():
    print("")
    print("Welcome to SwimFit! Swim your way to a fitter life.")
    print("")
    
    while True:
        user_type = input("Are you an [A]dmin, [U]ser, [F]AQ, or [E]xit:").lower()
        
        if user_type == 'f':
            show_faq()
            
        if user_type == 'a':
            choice = input("Choose an option: [1] Register Admin [2] Login Admin [3] Exit: ")

            if choice == '1':
                print("")
                print("REGISTRATION")
                print("")
                username = input("Username: ")
                password_hash = input("password: ")
                email = input("Email: ")
                register_admin(username, password_hash, email)
            
            elif choice == '2':
                print("")
                print("LOGIN")
                print("")
                username = input("Username: ")
                password_hash = input("password: ")
                if login_admin(username, password_hash):
                    while True:
                        admin_choice = input("Choose an option: [1] Create Workout Plan [2] Create Diet Plan [3] Update User Details [4] Logout: ")
                        
                        if admin_choice == '1':
                            admin_id = int(input("Admin ID: "))
                            user_id = int(input("User ID: "))
                            plan_details = input("Plan Details: ")
                            create_workout_plan(admin_id, user_id, plan_details)
                        
                        elif admin_choice == '2':
                            admin_id = int(input("Admin ID: "))
                            user_id = int(input("User ID: "))
                            plan_details = input("Plan Details: ")
                            create_diet_plan(admin_id, user_id, plan_details)
                        
                        elif admin_choice == '3':
                            admin_id = int(input("Admin ID: "))
                            user_id = int(input("User ID: "))
                            fitness_level = input("Fitness Level: ")
                            goal = input("Goal: ")
                            dietary_restrictions = input("Dietary Restrictions: ")
                            update_user_details(admin_id, user_id, fitness_level, goal, dietary_restrictions)
                        
                        elif admin_choice == '4':
                            Print("Logged Out")
                            break
            
            elif choice == '3':
                print("Goodbye!")
                break

        elif user_type == 'u':
            choice = input("Choose an option: [1] Register User [2] Login User [3] Exit: ")

            if choice == '1':
                print("")
                print("REGISTRATION")
                print("") 
                username = input("Username: ")
                password_hash = input("password: ")
                email = input("Email: ")
                fitness_level = input("Fitness Level: ")
                goal = input("Goal: ")
                dietary_restrictions = input("Dietary Restrictions: ")
                register_user(username, password_hash, email, fitness_level, goal, dietary_restrictions)
            
            elif choice == '2':
                print("")
                print("LOGIN")
                print("")
                username = input("Username: ")
                password_hash = input("password: ")
                if login_user(username, password_hash):
                    while True:
                        user_choice = input("Choose an option: [1] Log Progress [2] Analyze Performance [3] View Workout Plans [4] View Diet PLans [5] Logout: ")

                        if user_choice == '1':
                            user_id = int(input("User ID: "))
                            workout_date = input("Workout Date (YYYY-MM-DD): ")
                            workout_summary = input("Workout Summary: ")
                            progress_notes = input("Progress Notes: ")
                            log_progress(user_id, workout_date, workout_summary, progress_notes)
                        
                        elif user_choice == '2':
                            user_id = int(input("User ID: "))
                            analyze_performance(user_id)
                            
                        elif user_choice == '3':
                            user_id = int(input("User ID: "))
                            view_plans(user_id)
                        
                        elif user_choice == '4':
                            user_id = int(input("User ID: "))
                            view_diet_plan(user_id)
                        
                        elif user_choice == '5':
                            print("Logged out")
                            break
            
            elif choice == '3':
                print("Goodbye")
                break

        elif user_type == 'e':
            print("Goodbye")
            break

main()




    
    

    