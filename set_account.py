import requests

def set_account(account, cookie):

    response = requests.post('https://login.eagleeyenetworks.com/g/aaa/switch_account', {'account_id': account}, cookies=cookie)
    print(response)
    return(response)

def reset_account(cookie):
    response = requests.post('https://login.eagleeyenetworks.com/g/aaa/switch_account', cookies=cookie)
    print(response)
    if response.status_code == 200:
        print('Success returning to master account.')
    else:
        print('Account change failed.')

def change_account(cookie):
    account = raw_input('Type sub account ID or "0" to return to menu. >>> ')
    if account == 0:
        print('Return to menu.')
    else:
        response = set_account(account, cookie)
        if response.status_code == 200:
            print('Success change account.')
        else:
            print('Account change failed.')
