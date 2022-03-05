import requests

class MediaWiki:
    def __init__(self, endpoint, verify):
        self._endpoint = endpoint
        self._verify = verify
        self._session = requests.Session()

    def _get_login_token(self):
        params = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }

        response = self._session.get(
            url=self._endpoint, 
            params=params,
            verify=self._verify
        )
        data = response.json()

        login_token = data['query']['tokens']['logintoken']

        return login_token

    def _get_edit_token(self):
        params = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }

        response = self._session.get(url=self._endpoint, params=params)
        data = response.json()

        try:
            edit_token = data['query']['tokens']['csrftoken']
        except:
            print("Failed to get edit token:")
            print(data)
            raise

        return edit_token

    def login(self, bot_username, bot_password):
        login_token = self._get_login_token()

        params = {
            'action': "login",
            'lgname': bot_username,
            'lgpassword': bot_password,
            'lgtoken': login_token,
            'format':"json"
        }

        response = self._session.post(self._endpoint, data=params, verify=self._verify)
        data = response.json()

        return data

    def create_page(self):
        edit_token = self._get_edit_token()

        params = {
            "action": "edit",
            "format": "json",
            "title": "Test",
            "text": "This is an automatically generated page by wikidot-to-mediawiki",
            "token": edit_token
        }
        response = self._session.post(self._endpoint, data=params, verify=False)
        data = response.json()

        print("data:", data)
        if "error" in data:
            raise Exception("Failed to create page: "+str(data))    