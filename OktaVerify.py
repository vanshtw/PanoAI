
OKTA_ISSUER = "https://adobe.okta.com/oauth2/aus1gan31wnmCPyB60h8",
CLIENT_ID = "0oa1hi7qnb3l2Wt8T0h8"

auth_url = f"{OKTA_ISSUER}/v1/authorize"
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "scope": "openid profile",
    "redirect_uri": 
    #"https://adobe.okta.com/oauth2/default/uri",
    "https://wiki.corp.adobe.com/pages/viewpage.action?spaceKey=utt&title=Runbook+Assessment+Initiation+Process",
    "state": "random_state_string"
}

full_auth_url = f"{auth_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
print("Open this URL in a browser to authenticate:", full_auth_url)