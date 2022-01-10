import os,json,sys,subprocess

def find_drive(file_path):
    for number in range(65,91):
        drive_letter = chr(number)
        if os.path.exists(drive_letter+file_path):
            return drive_letter+file_path
    print("\n Searched file could not be found on any drive with path:" + file_path)
    return False

def load_json_file(file_path,variable):
    file = open(file_path)
    data = json.load(file)
    file.close()
    return data.get(variable)


def get_administrator_status():
    command = "(Get-LocalUser | Where-Object{$_.SID -like \"S-1-5-*-500\"}).Enabled"
    run = subprocess.run(["powershell", "-Command", command], stdout=subprocess.PIPE, universal_newlines=True)
    print("Is admin account enabled already: " + run.stdout)
    return run.stdout


def enable_administrator_account():
    command = "(Get-LocalUser | Where-Object{$_.SID -like \"S-1-5-*-500\"}).Name | Enable-LocalUser"
    run = subprocess.run(["powershell", "-Command", command], stdout=subprocess.PIPE, universal_newlines=True)
    print("\n Administrator account is activated by localscript")
    return run.stdout

#execute

meta_data_path = find_drive(":\OPENSTACK\LATEST\META_DATA.json")
if meta_data_path != "False":
    meta_data = load_json_file(meta_data_path,"meta")
else:
    sys.exit(0)

if meta_data["admin_username"] in ["Administrateur","Administrator"] and "False" in get_administrator_status():
    run = enable_administrator_account()
    sys.exit(1001)
else:
    print("Cloud-init user is not Administrateur/Administrator or Admin account is already enabled, script aborted.")
    sys.exit(0)