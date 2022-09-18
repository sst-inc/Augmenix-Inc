import utils
import progressbadges.prog_badges_completion
import progressbadges.prog_requirements_completion
import test2.test

def get_prog_user_input():
    print(
        """
Now managing progress badges, select an action:
1. Update badge requirements completion status for single member
2. Update badge requirements completion status for all members
3. Update badge requirements completion status for members from a spreadsheet (coming soon)
4. Update progress badge completion status for single member
5. Update progress badge completion status for all members
6. Update progress badge completion status for members from a spreadsheet (coming soon)
b. Go back (to previous menu)
""")
    choice = input("Your choice (1-5, b): ")
    while not utils.validate_choice_input(choice, 5):
        choice = input("Invalid input. Re-enter your choice (1-5): ")
    print("")
    if choice == "1":
        progressbadges.prog_requirements_completion.get_update_member_req_user_input()
    elif choice == "2":
        progressbadges.prog_requirements_completion.get_update_all_members_req_user_input()
    elif choice == "4":
        progressbadges.prog_badges_completion.get_update_member_req_user_input()
    elif choice == "5":
        progressbadges.prog_badges_completion.get_update_all_members_req_user_input()
    elif choice == "b":
        utils.get_first_user_input()
