import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pprint


class TmobileHomeInternetGateway(object):
    def __init__(self, address="192.168.12.1"):
        self.address = address
        self.http = None

    def login(self, username, password):
        body = {"username": username, "password": password}
        response = requests.post("http://192.168.12.1/TMI/v1/auth/login", json=body)
        if response.status_code == 401:
            print(response.json()["result"]["error"])
            print(response.json()["result"]["message"])
            return False
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.http = requests.Session()
        self.http.headers.update({"Authorization": "Bearer " + str(response.json()['auth']['token'])})
        self.http.mount("https://", adapter)
        self.http.mount("http://", adapter)
        return True

    def __check_login(self):
        if self.http is None:
            raise Exception("No established HTTP session, please login first")

    def get_network_settings(self):
        self.__check_login()
        response = self.http.get("http://192.168.12.1/TMI/v1/network/configuration?get=ap")
        if response.status_code == 200:
            return response.json()

    def disable_wifi(self):
        properties = self.get_network_settings()
        properties["2.4ghz"]["isRadioEnabled"] = False
        properties["5.0ghz"]["isRadioEnabled"] = False
        try:
            response1 = self.http.post("http://192.168.12.1/TMI/v1/network/configuration?set=ap", json=properties, timeout=1.5)
        except requests.exceptions.ReadTimeout:
            print("Post request timed out but this is most likely fine as it probably disabled Wifi")
            return
        if response1.status_code == 200:
            print("Disabled wifi")

    def enable_wifi(self):
        properties = self.get_network_settings()
        properties["2.4ghz"]["isRadioEnabled"] = True
        properties["5.0ghz"]["isRadioEnabled"] = True
        try:
            response1 = self.http.post("http://192.168.12.1/TMI/v1/network/configuration?set=ap", json=properties, timeout=1.5)
        except requests.exceptions.ReadTimeout:
            print("Post request timed out but this is most likely fine as it probably enabled Wifi")
            return
        if response1.status_code == 200:
            print("Enabled wifi")

    def get_connection_status(self):
        self.__check_login()
        response = self.http.get("http://192.168.12.1/TMI/v1/gateway?get=all")
        if response.status_code == 200:
            return response.json()

    def reboot(self):
        self.__check_login()
        response1 = self.http.post("http://192.168.12.1/TMI/v1/gateway/reset?set=reboot")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    TM = TmobileHomeInternetGateway()
    print(TM.login("admin", "secret_password"))
    pprint.pprint(TM.get_network_settings())
    pprint.pprint(TM.get_connection_status())
    # Examples of other actions
    # TM.disable_wifi()
    # TM.enable_wifi()
    # TM.reboot()
