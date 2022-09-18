import utils
import members.members_add
import members.members_remove


def get_members_user_input():
    print(
        """
Now managing members, select an action:
1. Add member
2. Add multiple members from a spreadsheet (coming soon)
3. Remove member
4. Update details of member (coming soon)
b. Go back (to previous menu)
""")
    choice = input("Your choice (1-4, b): ")
    while not utils.validate_choice_input(choice, 4):
        choice = input("Invalid input. Re-enter your choice (1-4): ")
    print("")
    if choice == "1":
        members.members_add.get_addmember_user_input()
    elif choice == "3":
        members.members_remove.get_removemember_user_input()
    elif choice == "b":
        utils.get_first_user_input()
