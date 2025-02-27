import time
import getpass
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Configurar ChromeOptions para usar un perfil persistente
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=./chrome_profile")

# Inicializar el servicio de ChromeDriver con webdriver-manager
service = ChromeService(executable_path=ChromeDriverManager().install())

# Inicializar el controlador de Chrome con las opciones y el servicio
driver = webdriver.Chrome(service=service, options=options)

driver.maximize_window()

# Inicia sesión en Facebook (si no estás logueado ya en el perfil)
driver.get("https://www.facebook.com")
wait = WebDriverWait(driver, 5)

try:
    # Rechazar cookies si aparece el botón (en español, inglés o alemán)
    try:
        reject_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Rechazar') or contains(text(), 'Reject') or contains(text(), 'Ablehnen')]")))
        reject_cookies_button.click()
    except:
        print("No se encontró el botón de rechazo de cookies, continuando...")
    
    email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
    pass_field = driver.find_element(By.ID, "pass")
    email_field.clear()
    username = input("Introduce tu usuario de Facebook (correo o número): ")
    password = getpass.getpass("Introduce tu contraseña de Facebook: ")
    email_field.send_keys(username)
    pass_field.clear()
    pass_field.send_keys(password)
    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    time.sleep(60)
except Exception as e:
    print("Posiblemente ya iniciaste sesión. Continuando...")

# Cargar perfiles desde archivo
profiles = []
with open("profiles.csv", "r") as file:
    reader = csv.reader(file)
    profiles = [row[0] for row in reader]

# Cargar datos previos si existen
try:
    with open("friends.json", "r") as f:
        friends_dict = json.load(f)
except FileNotFoundError:
    friends_dict = {}

def scroll_to_bottom(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

for profile in profiles:
    if profile in friends_dict:
        continue  # Skip if already processed
    
    if "profile.php" in profile: driver.get(f"{profile}&sk=friends")
    else : driver.get(f"{profile}/friends_all")
    
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[role='link'][tabindex='0']")))
    
    scroll_to_bottom(driver, pause_time=2)
    
    links = driver.find_elements(By.CSS_SELECTOR, "a[role='link'][tabindex='0']")
    
    profile_hrefs = []
    for link in links:
        href = link.get_attribute("href")
        if href and href.count("/") <= 3:
            # Buscar el span que contiene el nombre del amigo
            try:
                name_element = link.find_element(By.XPATH, ".//span")
                name = name_element.text.strip()
            except:
                name = "Unknown"
            
            profile_hrefs.append({"name": name, "href": href})
    
    friends_dict[profile] = profile_hrefs
    
    # Guardar datos después de cada iteración
    with open("friends.json", "w") as f:
        json.dump(friends_dict, f, indent=4)
    
    print(f"Guardados {len(profile_hrefs)} amigos de {profile}")

driver.quit()
