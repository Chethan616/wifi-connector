import os
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def scan_wifi_networks():
    result = subprocess.run(['netsh', 'wlan', 'show', 'networks'], capture_output=True, text=True)
    print(result.stdout)
    return result.stdout

def connect_to_wifi(network_name):
    result = subprocess.run(['netsh', 'wlan', 'connect', f'name={network_name}'], capture_output=True, text=True)
    if "successfully" in result.stdout:
        print(f"Successfully connected to {network_name}")
    else:
        print(f"Failed to connect to {network_name}")
        print(result.stderr)

def login_to_wifi(username, password):
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("http://www.google.com")  # Trying to trigger the login page

        # Wait for the page to load
        driver.implicitly_wait(10)

        # Check if we are redirected to the login page
        if "login" in driver.current_url or "wifi" in driver.current_url:
            # Find username and password fields (these IDs/Names can be found using browser dev tools)
            username_field = driver.find_element(By.ID, "username")  # Replace with actual ID or Name
            password_field = driver.find_element(By.ID, "password")  # Replace with actual ID or Name

            # Enter credentials
            username_field.send_keys(username)
            password_field.send_keys(password)

            # Submit the form (assuming there's a submit button)
            password_field.send_keys(Keys.RETURN)

            print("Logged in successfully.")
        else:
            print("Not redirected to the login page. Please check the Wi-Fi connection.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def main():
    # Scan and display available Wi-Fi networks
    networks_output = scan_wifi_networks()

    # Input Wi-Fi name
    name_of_router = input("Enter the name of the Wi-Fi network you want to connect to: ")

    # Check if the network is in the scan results
    if name_of_router in networks_output:
        connect_to_wifi(name_of_router)
    else:
        print(f"The network {name_of_router} is not available. Please check the name and try again.")
        return

    # Input credentials
    username = "23BAI0093"
    password = "Letmein@171005#"

    # Automate login
    login_to_wifi(username, password)

if __name__ == "__main__":
    main()
