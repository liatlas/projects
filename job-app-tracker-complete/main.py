import csv

#main execution
def execute_option(user_input):
    if user_input == "ADD":
        add_application()
    if user_input == "SHOW":
        show_applications()
# csv manipulation
def add_application():
    company_name = input("Company?\n").lower().strip()
    job_title = input("Job Title\n").lower().strip()
    date_applied = input("Date?\n").lower().strip()

    with open("./jobs.csv", 'a') as f:
        f.write(f"{company_name}, {job_title}, {date_applied}")

#display functions
def show_applications():
    with open('./jobs.csv', "r") as f:
        for row in f:
            print(row, end='')
    print()

def show_stats():
    count = 0
    with open('./jobs.csv', 'r') as f:
        for _ in f:
            count += 1
    return count - 1


# input checks
def invalid_input(user_input):
    options = ['ADD', 'SHOW', 'QUIT']
    if user_input not in options:
        return True
    return False

def check_quit(user_input):
    if user_input == "QUIT":
        return True
    return False

def main():
    state = True

    while state:
        print(f"Jobs Applied: {show_stats()}")

        user_input = input("What would you like to do? SHOW ADD QUIT\n").upper().strip()

        if invalid_input(user_input):
            continue

        if check_quit(user_input):
            print("Done")
            break

        execute_option(user_input)

if __name__ == "__main__":
    main()
