
from create_chrome import createChrome
from webdriver_setting import driver, driverURL
from time import sleep
from selenium.webdriver.common.by import By


# ** (1). automatically open chrome and login as a user
createChrome()

# ** (2). control (1) and go to admin page
driver = driver()
driver.get(driverURL)

a = driver.find_element(
    By.XPATH, '//div[@data-e2e-id="sidebar_customer_management_menu"]')

b = driver.find_element(
    By.XPATH, '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]')

print(a.click())
print(b.click())


sleep(10)
