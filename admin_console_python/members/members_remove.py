import utils
import members.members_main


def validate_email_input(email: str):
    return email in utils.main_table[0]


def get_removemember_user_input():
    email = input("Enter email (must be a valid SST email): ")
    while not validate_email_input(email):
        email = input(
            "A member with this email does not exist. Enter another email (must be a valid SST email): ")
    user_index = utils.main_table[0].index(email)
    name = utils.main_table[1][user_index]
    cfm = input(
        f"Confirm remove {name} with {email} from the unit? (Y/N): ").upper()
    while cfm != "Y" and cfm != "N":
        cfm = input(
            f"Invalid input. Confirm remove {name} with {email} from the unit? (Y/N): ").upper()
    if cfm == "Y":
        remove_member(user_index)
    else:
        print("Now returning back to the previous menu.")
        members.members_main.get_members_user_input()


def remove_member(user_index):
    prog_badges_url = utils.main_table[5][user_index]
    prog_badges_table = utils.get_csv_table(
        prog_badges_url, include_headers=False)
    rc_urls = prog_badges_table[3]
    for url in rc_urls:
        if url == "": continue
        utils.drive_service.files().delete(fileId=utils.get_file_id(url),
                                           supportsAllDrives=True).execute()
    utils.drive_service.files().delete(
        fileId=utils.get_file_id(prog_badges_url), supportsAllDrives=True).execute()
    utils.main_table[0].pop(user_index)
    utils.main_table[1].pop(user_index)
    utils.main_table[2].pop(user_index)
    utils.main_table[3].pop(user_index)
    utils.main_table[4].pop(user_index)
    utils.main_table[5].pop(user_index)
    utils.main_table[6].pop(user_index)
    utils.main_table[7].pop(user_index)
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
        "Member removed successfully. Would you like to continue managing members (Y/N): ").upper()
    while cont != "Y" and cont != "N":
        cont = input(
            f"Invalid input. Would you like to continue managing members (Y/N): ").upper()
    if cont == "Y":
        members.members_main.get_members_user_input()
    elif cont == "N":
        utils.get_first_user_input()
