from io import BytesIO
import utils
import members.members_main
from googleapiclient.http import MediaIoBaseUpload


def validate_sclass_input(sclass: str):
    if len(sclass) != 5:
        return False
    if sclass[0] != "S":
        return False
    if not sclass[1].isdigit():
        return False
    if not 1 <= int(sclass[1]) <= 4:
        return False
    if sclass[2:4] != "-0":
        return False
    if not sclass[4].isdigit():
        return False
    if not 1 <= int(sclass[4]) <= 9:
        return False
    return True


def validate_email_input(email: str):
    return utils.main_table[0].count(email) == 0


def get_addmember_user_input():
    print("Now adding a member, fill in the required details.")

    email = input("Enter email (must be a valid SST email): ")
    while not validate_email_input(email):
        email = input(
            "A member with this email already exists. Enter another email (must be a valid SST email): ")

    name = input("Enter name: ")

    sclass = input("Enter class (using format SX-0X): ")
    while not validate_sclass_input(sclass):
        sclass = input("Invalid input. Re-enter class (using format SX-0X): ")

    patrol_choice = input("""
Select patrol of member:
1. Exa
2. Nano
3. Tera
4. Zetta
Your choice (1-4): """)
    while not utils.validate_choice_input(patrol_choice, 4):
        patrol_choice = input("Invalid input. Re-enter your choice (1-4): ")
    match patrol_choice:
        case "1":
            patrol = "Exa"
        case "2":
            patrol = "Nano"
        case "3":
            patrol = "Tera"
        case "4":
            patrol = "Zetta"
    print("")

    rank_choice = input("""
Select rank of member:
1. Patrol Leader
2. Assistant Patrol Leader
3. Logistics IC
4. Flag Raising IC
Your choice (1-4, leave blank for none): """)
    while not utils.validate_choice_input(rank_choice, 4) or rank_choice == "":
        rank_choice = input(
            "Invalid input. Re-enter your choice (1-4, leave blank for none): ")
    match rank_choice:
        case "1":
            rank = "Patrol Leader"
        case "2":
            rank = "Assistant Patrol Leader"
        case "3":
            rank = "Logistics IC"
        case "4":
            rank = "Flag Raising IC"
    print("")

    cfm = input(
        f"Confirm add {name} with {email} to the unit? (Y/N): ").upper()
    while cfm != "Y" and cfm != "N":
        cfm = input(
            f"Invalid input. Confirm add {name} with {email} to the unit? (Y/N): ").upper()
    if cfm == "Y":
        add_member(email, name, sclass, patrol, rank)
    else:
        print("Now returning back to the previous menu.")
        members.members_main.get_members_user_input()


def add_member(email: str, name: str, sclass: str, patrol: str, rank: str):
    prog_badges_template = utils.get_csv_table(
        f"https://docs.google.com/spreadsheets/d/{utils.PROG_BADGES_TEMPLATE_ID}/edit?usp=sharing", include_headers=True)
    print("Adding member, this may take up to a few minutes.")

    num_prog_badges = len(prog_badges_template[0])
    for i in range(1, num_prog_badges):
        rc_template_url = prog_badges_template[3][i]
        if rc_template_url == "":
            continue
        rc_template_csv = utils.get_csv(rc_template_url)
        f = utils.drive_service.files().create(body={
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "driveId": utils.SHARED_DRIVE_ID,
            "supportsAllDrives": True,
            "parents": [utils.PROG_BADGES_RC_FOLDER_ID],
            "name": f"RC_{name}_{prog_badges_template[0][i]}"
        }, media_body=MediaIoBaseUpload(BytesIO(str.encode(rc_template_csv)), mimetype='text/csv'), supportsAllDrives=True).execute()
        rc_url = f"https://docs.google.com/spreadsheets/d/{f.get('id')}/edit?usp=sharing"
        prog_badges_template[3][i] = rc_url

    prog_badges_csv = utils.conv_table_csv(prog_badges_template)
    f = utils.drive_service.files().create(body={
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "driveId": utils.SHARED_DRIVE_ID,
        "supportsAllDrives": True,
        "parents": [utils.PROG_BADGES_FOLDER_ID],
        "name": f"B_{name}"
    }, media_body=MediaIoBaseUpload(BytesIO(str.encode(prog_badges_csv)), mimetype='text/csv'), supportsAllDrives=True).execute()
    prog_badges_url = f"https://docs.google.com/spreadsheets/d/{f.get('id')}/edit?usp=sharing"

    '''event_badges_csv = utils.get_csv("")  # TODO: not implemented
    event_badges_file_id = ''.join(random.choices(
        string.ascii_letters + string.digits, k=28))
    utils.drive_service.files().create(body={
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "id": event_badges_file_id,
        "driveId": "0ANi9utLqR454Uk9PVA",
        "parents": ["1ceKbIgvs7wtkT06n86x51TzEuG92K-jp"],
        "name": f"E_{name}"
    }, media_body=MediaUpload(event_badges_csv))
    event_badges_url = f"https://docs.google.com/spreadsheets/d/{event_badges_file_id}/edit?usp=sharing"

    ua_csv = utils.get_csv("")  # TODO: not implemented
    ua_file_id = ''.join(random.choices(
        string.ascii_letters + string.digits, k=28))
    utils.drive_service.files().create(body={
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "id": ua_file_id,
        "driveId": "0ANi9utLqR454Uk9PVA",
        "parents": ["1zZLzUR5SCcW9TyR7lJZ9J2SEWnUvEg3Z"],
        "name": f"UA_{name}"
    }, media_body=MediaUpload(ua_csv))
    ua_url = f"https://docs.google.com/spreadsheets/d/{ua_file_id}/edit?usp=sharing"'''

    utils.main_table[0].append(email)
    utils.main_table[1].append(name)
    utils.main_table[2].append(sclass)
    utils.main_table[3].append(patrol)
    utils.main_table[4].append(rank)
    utils.main_table[5].append(prog_badges_url)
    utils.main_table[6].append("")  # TODO: not implemented
    utils.main_table[7].append("")  # TODO: not implemented
    main_table_csv = utils.conv_table_csv(utils.main_table)

    utils.sheets_service.spreadsheets().batchUpdate(spreadsheetId=utils.MAIN_TABLE_ID, body={
        'requests': [{
            'pasteData': {
                "coordinate": {
                    "sheetId": 0,
                    "rowIndex": "0",  # adapt this if you need different positioning
                    "columnIndex": "0",  # adapt this if you need different positioning
                },
                "data": main_table_csv,
                "type": 'PASTE_NORMAL',
                "delimiter": ',',
            }
        }]
    }).execute()

    cont = input(
        "Member added successfully. Would you like to continue managing members? (Y/N): ").upper()
    while cont != "Y" and cont != "N":
        cont = input(
            f"Invalid input. Would you like to continue managing members? (Y/N): ").upper()
    if cont == "Y":
        members.members_main.get_members_user_input()
    elif cont == "N":
        utils.get_first_user_input()
