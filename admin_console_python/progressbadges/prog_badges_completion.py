from datetime import datetime
import utils
import progressbadges.prog_main


def validate_email_input(email: str):
    return email in utils.main_table[0]


def get_update_member_req_user_input():
    email = input("Enter email (must be a valid SST email): ")
    while not validate_email_input(email):
        email = input(
            "A member with this email does not exist. Enter another email (must be a valid SST email): ")
    user_index = utils.main_table[0].index(email)
    name = utils.main_table[1][user_index]
    print(f"Now updating badge requirements for {name}.")

    print("Loading badges...")
    print("")
    prog_badges_url = utils.main_table[5][user_index]
    prog_badges_table = utils.get_csv_table(
        prog_badges_url, include_headers=True)
    prog_badges_names = prog_badges_table[0]
    prog_badges_completed = prog_badges_table[4]
    prog_badges_completion_date = prog_badges_table[5]
    prog_badges_len = len(prog_badges_names)
    print("Badges available:")
    for i in range(1, prog_badges_len):
        print(f"{i}: {prog_badges_names[i]}", end=" - ")
        if prog_badges_completed[i] == "TRUE":
            print(f"√ Completed on {prog_badges_completion_date[i]}")
        else:
            print(f"Not completed")
    badge_choice = input(f"Enter number (1-{prog_badges_len - 1}): ")
    while not utils.validate_choice_input(badge_choice, prog_badges_len - 1):
        badge_choice = input(
            f"Invalid input. Enter number (1-{prog_badges_len - 1}): ")
    badge_choice = int(badge_choice)
    badge_completed = prog_badges_completed[badge_choice]

    cfm = ""
    while cfm != "Y" and cfm != "N":
        if badge_completed == "TRUE":
            cfm = input(
                "Would you like to make this badge not acquired? (Y/N): ").upper()
        else:
            cfm = input(
                "Would you like to make this badge acquired? (Y/N): ").upper()
    if cfm == "Y":
        update_single_batch_comp(
            prog_badges_table, prog_badges_url, badge_choice, "FALSE" if badge_completed == "TRUE" else "TRUE")
        print("")
        cont = input(
            "Progress badge details updated successfully. Would you like to continue managing progress badges? (Y/N): ").upper()
        while cont != "Y" and cont != "N":
            cont = input(
                f"Invalid input. Would you like to continue managing progress badges? (Y/N): ").upper()
        if cont == "Y":
            progressbadges.prog_main.get_prog_user_input()
        elif cont == "N":
            utils.get_first_user_input()
    else:
        progressbadges.prog_main.get_prog_user_input()

def get_update_all_members_req_user_input():
    print("Loading badges...")
    print("")
    prog_badges_urls = f"https://docs.google.com/spreadsheets/d/{utils.PROG_BADGES_TEMPLATE_ID}/edit?usp=sharing"
    prog_badges_table = utils.get_csv_table(
        prog_badges_urls, include_headers=True)
    prog_badges_names = prog_badges_table[0]
    prog_badges_len = len(prog_badges_names)
    print("Badges available:")
    for i in range(1, prog_badges_len):
        print(f"{i}: {prog_badges_names[i]}")
    badge_choice = input(f"Enter number (1-{prog_badges_len - 1}): ")
    while not utils.validate_choice_input(badge_choice, prog_badges_len - 1):
        badge_choice = input(
            f"Invalid input. Enter number (1-{prog_badges_len - 1}): ")
    badge_choice = int(badge_choice)

    completed_choice = input(
        "Enter Y to mark as completed or Enter N to mark as not completed. (Y/N): ").upper()
    while completed_choice != "Y" and completed_choice != "N":
        completed_choice = input(
            "Invalid input. Mark as completed? (Y/N): ").upper()
    new_badge_comp = "TRUE" if completed_choice == "Y" else "FALSE"

    print("")
    cfm = input("Confirm update details for ALL members? (Y/N): ").upper()
    while cfm != "Y" and cfm != "N":
        cfm = input(
            "Invalid input. Confirm update details for ALL members? (Y/N): ").upper()
    if cfm == "Y":
        prog_badges_urls = utils.main_table[5]
        members_len = len(prog_badges_urls)
        print("This operation may take up to a few minutes. Do not close this window.")
        for i in range(1, members_len):
            prog_badges_url = prog_badges_urls[i]
            prog_badges_table = utils.get_csv_table(
                prog_badges_url, include_headers=True)
            update_single_batch_comp(prog_badges_table, prog_badges_url, badge_choice, new_badge_comp)
        print("")
        cont = input(
            "Progress badge updated successfully. Would you like to continue managing progress badges? (Y/N): ").upper()
        while cont != "Y" and cont != "N":
            cont = input(
                f"Invalid input. Would you like to continue managing progress badges? (Y/N): ").upper()
        if cont == "Y":
            progressbadges.prog_main.get_prog_user_input()
        elif cont == "N":
            utils.get_first_user_input()
    else:
        progressbadges.prog_main.get_prog_user_input()

def update_single_batch_comp(prog_badges_table, prog_badges_url, badge_choice, new_badge_comp):
    prog_badges_completed = prog_badges_table[4]
    prog_badges_completion_date = prog_badges_table[5]
    prog_badges_completed[badge_choice] = new_badge_comp
    date = datetime.utcnow()
    if new_badge_comp == "TRUE":
        prog_badges_completion_date[badge_choice] = date.strftime("%m/%d/%Y")
    else:
        prog_badges_completion_date[badge_choice] = "-"
    badge_csv = utils.conv_table_csv(prog_badges_table)
    badge_file_id = utils.get_file_id(prog_badges_url)
    sheet_id = utils.sheets_service.spreadsheets().get(
        spreadsheetId=badge_file_id).execute()["sheets"][0]["properties"]["sheetId"]
    utils.sheets_service.spreadsheets().batchUpdate(spreadsheetId=badge_file_id, body={
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": sheet_id,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0",  # adapt this if you need different positioning
                },
                "data": badge_csv,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }).execute()
