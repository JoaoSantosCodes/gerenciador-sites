from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Configurações do Selenium
chrome_options = Options()
chrome_options.add_argument('--headless')  # Executa sem abrir janela
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1200,800')

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# Usuário único para cada execução
test_id = str(random.randint(1000, 9999))
username = f"testeuser{test_id}"
password = f"testesenha{test_id}"

try:
    # Acesse o frontend
    driver.get('http://localhost:8080/app.html')
    time.sleep(1)

    # Abrir tela de cadastro
    btn_cadastrar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Cadastrar') and not(@style)]")))
    btn_cadastrar.click()

    # Preencher cadastro
    wait.until(EC.visibility_of_element_located((By.ID, "reg_username")))
    driver.find_element(By.ID, "reg_username").send_keys(username)
    driver.find_element(By.ID, "reg_password").send_keys(password)
    btn_cadastrar2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='register']//button[contains(text(),'Cadastrar')]")))
    btn_cadastrar2.click()
    time.sleep(1)
    btn_voltar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Voltar')]")))
    btn_voltar.click()
    time.sleep(0.5)

    # Login
    wait.until(EC.visibility_of_element_located((By.ID, "username")))
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    btn_entrar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Entrar')]")))
    btn_entrar.click()
    time.sleep(1)

    # Debug: printar conteúdo da página após login
    print("[DEBUG] Página após login:\n", driver.page_source[:1000])

    # Adicionar credencial
    wait.until(EC.visibility_of_element_located((By.ID, "site_name")))
    driver.find_element(By.ID, "site_name").send_keys("Site Teste")
    driver.find_element(By.ID, "url").send_keys("https://site.com")
    driver.find_element(By.ID, "cred_username").send_keys("usuario1")
    driver.find_element(By.ID, "cred_password").send_keys("senha1")
    driver.find_element(By.ID, "notes").send_keys("nota teste")
    btn_add = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Adicionar')]")))
    btn_add.click()
    time.sleep(1)

    # Verifica se credencial aparece
    cred = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "cred-item")))
    assert "Site Teste" in cred.text
    print("[OK] Cadastro, login e adição de credencial funcionando.")

    # Exclusão de credencial
    btn_excluir = cred.find_element(By.XPATH, ".//button[contains(text(),'Excluir')]")
    btn_excluir.click()
    time.sleep(0.5)
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(1)
    assert "Nenhuma credencial cadastrada" in driver.page_source
    print("[OK] Exclusão de credencial funcionando.")

    # Logout
    btn_logout = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "logout")))
    btn_logout.click()
    time.sleep(0.5)
    assert "Entrar" in driver.page_source
    print("[OK] Logout funcionando.")

finally:
    driver.quit() 