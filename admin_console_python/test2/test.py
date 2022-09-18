from io import BytesIO
import utils
from googleapiclient.http import MediaIoBaseUpload


def fix_rc():
    print("Loading badges...")
    print("")
    prog_badges_urls = f"https://docs.google.com/spreadsheets/d/{utils.PROG_BADGES_TEMPLATE_ID}/edit?usp=sharing"
    prog_badges_table = utils.get_csv_table(
        prog_badges_urls, include_headers=True)
    prog_badges_names = prog_badges_table[0]
    prog_badges_requirements = prog_badges_table[2]
    prog_badges_len = len(prog_badges_names)
    print("Badges available:")
    for i in range(1, prog_badges_len):
        badge_name = prog_badges_names[i]
        requirements_url = prog_badges_requirements[i]
        print("")
        print(f"Loading requirements for badge \"{badge_name}\"")
        print("")
        requirements_table = utils.get_csv_table(
            requirements_url, include_headers=False)
        requirements = requirements_table[0]
        requirements_len = len(requirements)
        print("Requirements available:")
        rc_table = [["Requirements Completed?"], [
            "Date of requirements completion"]]
        for i in range(requirements_len):
            rc_table[0].append("FALSE")
            rc_table[1].append("")
        rc_csv = utils.conv_table_csv(rc_table)
        f = utils.drive_service.files().create(body={
            "mimeType": "application/vnd.google-apps.spreadsheet",
            "driveId": utils.SHARED_DRIVE_ID,
            "supportsAllDrives": True,
            "parents": [utils.PROG_BADGES_RC_FOLDER_ID],
            "name": f"RC_Template_{badge_name}"
        }, media_body=MediaIoBaseUpload(BytesIO(str.encode(rc_csv)), mimetype='text/csv'), supportsAllDrives=True).execute()
