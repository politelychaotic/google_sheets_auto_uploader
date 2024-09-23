from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait as Wait


# Since there's nothing private exposed in this code,
# I'm sharing a rendition of the QC automation program
# I created about a year ago.
#
# Davin. Feel free to use this to test your google sheets
# integration to enable us to dump data into our testing
# spreadsheet automatically.
#
# Feel free to edit/improve the code below, also. :)


EEN_ADMIN_URL = "https://eenadmin.eagleeyenetworks.com"


class AdminActions:

    def __init__(self, driver: WebDriver = None):
        if driver is None:
            self.driver = webdriver.Chrome()
        else:
            self.driver = driver

    def is_logged_in(self) -> bool:
        """
        Check for the presence of a web element to determine
        if we are logged in to EEN Admin.
        """
        for attempts in range(2):
            try:
                Wait(self.driver, 15).until(
                    EC.presence_of_element_located((By.NAME, 'search_type'))
                )
            except WebDriverException:
                # Refresh the webpage once between attempts
                if attempts < 1:
                    self.driver.refresh()
            else:
                return True

        return False

    def login(self, username: str, password: str) -> bool:
        """
        Attempt to log into EEN Admin.
        """
        print('Getting EEN Admin...')

        self.driver.get('https://eenadmin.eagleeyenetworks.com')

        print('Locating login fields...')

        username_field = Wait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password_field = Wait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'password'))
        )

        print(f"Attempting login as '{username}'...")

        username_field.clear()
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password, Keys.RETURN)

        # Start looking for the authentication web element "totp"
        # If present, then the login credentials were good

        auth_field = Wait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'totp'))
        )
        auth_code = input('Enter auth code: ')
        auth_field.clear()
        auth_field.send_keys(auth_code, Keys.RETURN, Keys.RETURN)

        return self.is_logged_in()

    def search(self, serial: str) -> dict[str, str]:
        """
        Query a serial number in EEN Admin and try to retrieve
        bridge data.
        """
        # Select a search type from the dropdown menu
        search_type = Select(Wait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'search_type')
        )))
        search_type.select_by_visible_text('Bridges and Cameras')

        # Enter serial into the search bar and press enter
        search_bar = Wait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'search'))
        )
        search_bar.clear()
        search_bar.send_keys(serial, Keys.RETURN)

        print(f"Querying Admin for '{serial}'...")

        # If the search yields a result, an ip address web element
        # will become visible.
        ip_addr = Wait(self.driver, 30).until(
            EC.presence_of_element_located((By.NAME, 'ip_addr'))
        ).text

        # Now scrape whatever other data we care about.
        #
        # There can be multiple query results, but the first one
        # is correct 99.9% of the time. So we only grab that.
        serial_res = self.driver.find_element(By.XPATH, "//td[@id='bridge-serial']").text
        connect_id = self.driver.find_element(By.XPATH, "//td[@id='bridge-connect_id']").text
        model_rev  = self.driver.find_element(By.XPATH, "//td[@id='bridge-model']").text

        # If the serial that shows up in the result doesn't match
        # what we searched for, let's let the user know.
        if serial_res != serial:
            print(f"Searched for '{serial}' but got results for '{serial_res}'!")

        data = {
            'ip_addr'   : ip_addr,
            'serial'    : serial_res,
            'conn_id'   : connect_id,
            'model_rev' : model_rev
        }

        for k, v in data.items():
            print(f"{k}: {v}")

        return data

    @staticmethod
    def get_input_serials() -> list[str]:
        """
        Prompt the user to enter serials, and return them as a list.
        """
        serials = []

        print('Enter serials. Press Enter with no input to submit.')

        while True:
            serial = input('Enter serial: ').strip().upper()
            if serial:
                serials.append(serial)
            else:
                break

        return serials


if __name__ == '__main__':
    # Sample usage
    #
    # It's all a bit crude, but should get the point across.
    driver = webdriver.Chrome()
    actions = AdminActions(driver)
    actions.login('your_username', 'your_password')

    serials = actions.get_input_serials()
    serials_to_data = {}

    for serial in serials:
        try:
            data = actions.search(serial)
            serials_to_data[serial] = data
        except:
            continue

    import json
    print(json.dumps(serials_to_data, indent=4))

