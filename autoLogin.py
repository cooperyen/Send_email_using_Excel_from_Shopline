
from create_chrome import createChrome
from el_func import elementTarget
from webdriver_setting import driver, driverURL
from selenium.webdriver.common.by import By


# ** (1). automatically open chrome and login as a user
createChrome()

# ** (2). control (1) and go to admin page
driver = driver()
driver.get(driverURL)


elementTarget(driver,
            '//div[@data-e2e-id="sidebar_customer_management_menu"]', By.XPATH).click()
elementTarget(driver,
            '//a[@data-e2e-id="sidebar_customer_management_submenu_users"]', By.XPATH).click()
