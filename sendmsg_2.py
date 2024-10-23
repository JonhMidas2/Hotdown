from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# API 
agent = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

# CHAVE xgLNUFtZsAbhZZaxkRh5ofM6Z0YIXwwv
with open("api.txt", "r") as file:
     api = file.read()
api = api.split(".n.")
bolinha_notificacao = api[3].strip()
contato_cliente = api[4].strip()
caixa_msg = "//*[@id='main']/footer/div[1]/div/span/div/div[2]/div[2]/button/span"
msg_cliente = api[6].strip()
caixa_msg2 = api[7].strip()
caixa_pesquisa = api[8].strip()

progress_file = 'progress.txt'

def save_progress(line_number: int, progress_file: str):
    with open(progress_file, "w") as file:
        file.write(str(line_number))

def read_progress(progress_file: str) -> int:
    if os.path.exists(progress_file):
        with open(progress_file, "r") as file:
            return int(file.read().strip())
    return 0

# SALVA SESSAO
dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + dir_path + "/pasta/sessao2")
driver = webdriver.Chrome(options=chrome_options2)
driver.get('https://web.whatsapp.com/')

# Aguarda a página carregar completamente
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.XPATH, "//div[@id='side']"))
)

promotion = "%E2%9A%A0%EF%B8%8F%20MUITA%20ATEN%C3%87%C3%83O%20NA%20MENSAGEM%20ABAIXO%0A%0AOl%C3%A1!%20Ainda%20n%C3%A3o%20faz%20parte%20da%20nossa%20comunidade?..."

resp_1 = "Olá, como vai? Espero que esteja tudo bem! Entre para nossa comunidade do telegram, e fique por dentro das novidades, cursos, bate-papo e referências: https://t.me/rateiogarantido"

def aut_msg():
    start_line = read_progress(progress_file)
    with open("CONT2.txt", "r") as file:
        for current_line, line in enumerate(file):
            if current_line < start_line:
                continue
            number = line.strip()
            try:
                link = f'https://web.whatsapp.com/send?phone={number}&text={resp_1}'
                driver.get(link)
                
                # Aguarda até que o alerta apareça e o aceita
                try:
                    WebDriverWait(driver, 10).until(EC.alert_is_present())
                    driver.switch_to.alert.accept()
                except:
                    pass

                # Aguarda até que o botão ou a caixa de mensagem estejam prontos
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, caixa_msg))
                )

                campo_de_texto = driver.find_element(By.XPATH, caixa_msg)
                campo_de_texto.click()
                campo_de_texto.send_keys(Keys.ENTER)
                
                time.sleep(5)  # Tempo extra para garantir que a mensagem foi enviada
                save_progress(current_line + 1, progress_file)

            except Exception as e:
                print(f"Erro no número {number}: {e}")
                continue

aut_msg()
