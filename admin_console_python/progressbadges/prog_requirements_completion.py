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
        prog_badges_url, include_headers=False)
    prog_badges_names = prog_badges_table[0]
    prog_badges_requirements = prog_badges_table[2]
    prog_badges_rc = prog_badges_table[3]
    prog_badges_len = len(prog_badges_names)
    print("Badges available:")
    for i in range(prog_badges_len):
        print(f"{i + 1}: {prog_badges_names[i]}")
    badge_choice = input(f"Enter number (1-{prog_badges_len}): ")
    while not utils.validate_choice_input(badge_choice, prog_badges_len):
        badge_choice = input(
            f"Invalid input. Enter number (1-{prog_badges_len}): ")
    badge_choice = int(badge_choice)
    badge_name = prog_badges_names[badge_choice - 1]
    requirements_url = prog_badges_requirements[badge_choice - 1]
    rc_url = prog_badges_rc[badge_choice - 1]

    print(f"Loading requirements for badge \"{badge_name}\"")
    print("")
    requirements_table = utils.get_csv_table(
        requirements_url, include_headers=False)
    requirements = requirements_table[0]
    requirements_len = len(requirements)
    rc_table = utils.get_csv_table(rc_url, include_headers=True)
    rc = rc_table[0]
    rc_completion_date = rc_table[1]
    print("Requirements available:")
    for i in range(requirements_len):
        print(f"{i + 1}: {requirements[i]}", end=" - ")
        if rc[i] == "TRUE":
            print(f"√ Completed on {rc_completion_date[i + 1]}")
        else:
            print(f"Not completed")
    req_choice = input(f"Enter number (1-{requirements_len}): ")
    while not utils.validate_choice_input(req_choice, requirements_len):
        req_choice = input(
            f"Invalid input. Enter number (1-{requirements_len}): ")
    rc_comp_index = int(req_choice)

    cfm = ""
    curr_req_comp = rc[rc_comp_index]
    while cfm != "Y" and cfm != "N":
        if curr_req_comp == "TRUE":
            cfm = input(
                "Would you like to make this requirement not completed? (Y/N): ").upper()
        else:
            cfm = input(
                "Would you like to make this requirement completed? (Y/N): ").upper()
    if cfm == "Y":
        update_single_batch_req_comp(
            rc_table, rc_url, rc_comp_index, "FALSE" if curr_req_comp == "TRUE" else "TRUE")
        print("")
        cont = input(
            "Requirement updated successfully. Would you like to continue managing progress badges? (Y/N): ").upper()
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
        prog_badges_urls, include_headers=False)
    prog_badges_names = prog_badges_table[0]
    prog_badges_requirements = prog_badges_table[2]
    prog_badges_len = len(prog_badges_names)
    print("Badges available:")
    for i in range(prog_badges_len):
        print(f"{i + 1}: {prog_badges_names[i]}")
    badge_choice = input(f"Enter number (1-{prog_badges_len}): ")
    while not utils.validate_choice_input(badge_choice, prog_badges_len):
        badge_choice = input(
            f"Invalid input. Enter number (1-{prog_badges_len}): ")
    badge_choice = int(badge_choice)
    badge_name = prog_badges_names[badge_choice - 1]
    requirements_url = prog_badges_requirements[badge_choice - 1]

    print("")
    print(f"Loading requirements for badge \"{badge_name}\"")
    print("")
    requirements_table = utils.get_csv_table(
        requirements_url, include_headers=False)
    requirements = requirements_table[0]
    requirements_len = len(requirements)
    print("Requirements available:")
    for i in range(requirements_len):
        print(f"{i + 1}: {requirements[i]}")
    req_choice = input(f"Enter number (1-{requirements_len}): ")
    while not utils.validate_choice_input(req_choice, requirements_len):
        req_choice = input(
            f"Invalid input. Enter number (1-{requirements_len}): ")
    rc_comp_index = int(req_choice)

    completed_choice = input(
        "Enter Y to mark as completed or Enter N to mark as not completed. (Y/N): ").upper()
    while completed_choice != "Y" and completed_choice != "N":
        completed_choice = input(
            "Invalid input. Mark as completed? (Y/N): ").upper()
    new_req_comp = "TRUE" if completed_choice == "Y" else "FALSE"

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
                prog_badges_url, include_headers=False)
            prog_badges_rc = prog_badges_table[3]
            rc_url = prog_badges_rc[badge_choice - 1]
            rc_table = utils.get_csv_table(rc_url, include_headers=True)
            update_single_batch_req_comp(
                rc_table, rc_url, rc_comp_index, new_req_comp)
        print("")
        cont = input(
            "Requirement updated successfully. Would you like to continue managing progress badges? (Y/N): ").upper()
        while cont != "Y" and cont != "N":
            cont = input(
                f"Invalid input. Would you like to continue managing progress badges? (Y/N): ").upper()
        if cont == "Y":
            progressbadges.prog_main.get_prog_user_input()
        elif cont == "N":
            utils.get_first_user_input()
    else:
        progressbadges.prog_main.get_prog_user_input()


def update_single_batch_req_comp(rc_table, rc_url, rc_comp_index, new_req_comp):
    rc = rc_table[0]
    rc_completion_date = rc_table[1]
    rc[rc_comp_index] = new_req_comp
    date = datetime.utcnow()
    if new_req_comp == "TRUE":
        rc_completion_date[rc_comp_index] = date.strftime("%m/%d/%Y")
    else:
        rc_completion_date[rc_comp_index] = "-"
    rc_completion_date[rc_comp_index] = date.strftime("%m/%d/%Y")
    rc_csv = utils.conv_table_csv(rc_table)
    rc_file_id = utils.get_file_id(rc_url)
    sheet_id = utils.sheets_service.spreadsheets().get(
        spreadsheetId=rc_file_id).execute()["sheets"][0]["properties"]["sheetId"]
    utils.sheets_service.spreadsheets().batchUpdate(spreadsheetId=rc_file_id, body={
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": sheet_id,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0",  # adapt this if you need different positioning
                },
                "data": rc_csv,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }).execute()
