import requests
import json
import urllib3

#remove insecure https warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#input validation
def question(stuff):
    while True:
        answer = input(f"\n{stuff}:\n")
        if len(answer) != 0:
            False
            return answer 


# ask user for configuration 
def askConfig():

    print("\n[ Provide API/CMA/Domain Configuration ]\n")

    global username, password, api_ip, api_port, domain, hostname

    username = question("Username")
    password = question("Password")
    api_ip = question("API (MDM) IP Address")
    api_port = question("API Port")
    domain = question("Domain Name (in SmartConsole)")
    hostname = question("Host name to search by")

    formatanswer = f"""username = {username}
password = {password}
API IP = {api_ip}
API Port = {api_port}
Domain Name = {domain}
hostname = {hostname}
"""  

    result = question(f"\n{formatanswer}\nIs this information correct? (y/n)")   
    if result == "n":
        askConfig()
    elif result == "y": 
        print("\nContinuing... \n")



# API Login
def login(): 

    print("\n[ Login to API ]\n")
    
    api_url = f'{url}/login'
    headers = {'Content-Type' : 'application/json'}
    body = {'user' : f'{username}', 
            'password' : f'{password}',
            'domain' : f'{domain}',
            'session-timeout' : 1800}

    api_post = requests.post(api_url, data = json.dumps(body), headers=headers, verify=False)
    result = json.loads(api_post.text)

    response = api_post.status_code
    if response == 200: 
        print(f'{response}... Log in Successful.\n')
    else: 
        print(f'{response}... Login Failed.\n')

    return result 


def whereused(): 

    print(f"\n[ where-used {hostname} ]\n")
    
    api_url = f'{url}/where-used'
    body = {
        "name" : f'{hostname}'
        #"details-level" : "full"
    }
    x = sid["sid"]
    headers = {
    'Content-Type': 'application/json',
    'X-chkp-sid': f'{x}'
    }

    api_post = requests.post(api_url, data=json.dumps(body), headers=headers, verify=False, )
    b = api_post.json()
    
    with open ('output.json', 'w') as f: 
        f.write(json.dumps(b, indent=4, sort_keys=True))
    
    for item in b['used-directly']['nat-rules']:
        print(f"{item}\n")
        with open('nat-rules.txt', 'w+') as f:
            f.writelines(json.dump(item))


# API Logout
def logout(sid): 

    print("\n[ Log out of session ]\n")

    api_url = f'{url}/logout'
    x = sid["sid"]
    headers = {'Content-Type' : 'application/json',
                'X-chkp-sid' : f'{x}'} 
    body = {}
    api_post = requests.post(api_url, data=json.dumps(body), headers=headers, verify=False)
    result = api_post.json()

    response = api_post.status_code
    if response == 200: 
        print(f'{response}... Logged out\n')
    else: 
        print(f'{response}... Logout failed\n')


def main():
    
    askConfig()
    global url
    url = f'https://{api_ip}:{api_port}/web_api'
    
    global sid
    sid = login()
    
    whereused()
    
    
if __name__=="__main__":
    try:
        main()
    except Exception as e:
        print(f"[ Error ]\n{e}\n")
    finally:
        logout(sid)
        quit()