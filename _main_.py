from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


# Inicializar o WebDriver e o WebDriverWait
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 7)

# Variaveis  

baseFile_name = "teste.xlsx"
url_esl = "*****"
user_esl = "******"
password_esl = "*******"


# Carregar a planilha 'Base'
df = pd.read_excel(baseFile_name)



# Adicionar a coluna "cadastrado" se não existir
if "Cadastro" not in df.columns:
    df["Cadastro"] = ""

# Salvar a atualização da coluna de volta na planilha
with pd.ExcelWriter(baseFile_name, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df.to_excel(writer, sheet_name='Base', index=False)
    
    

def realizar_login(driver, wait, url_login, user_esl, password_esl):
    # Acessar a URL de login
    driver.get(url_login)
    driver.maximize_window()

    try:
        # Localizar e preencher o campo de email/usuário
        text_user = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="user_email"]'))
        )
        text_user.send_keys(user_esl)

        # Localizar e preencher o campo de senha
        text_password = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="user_password"]'))
        )
        text_password.send_keys(password_esl)

        # Localizar e clicar no botão de login
        send_credentials = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="new_user"]/div[2]/div/div[1]/input'))
        )
        send_credentials.click()

        print("Login realizado com sucesso.")
    except Exception as e:
        print(f"Erro ao realizar login: {e}")  

def search_and_select_table(driver, wait, nome_tb_redespacho):
        
    try:
        search_tsp_redispatch = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="search_price_tables_name"]'))
        )
        search_tsp_redispatch.click()
        search_tsp_redispatch.clear()
        search_tsp_redispatch.send_keys(nome_tb_redespacho)
        time.sleep(1.3)
        search_tsp_redispatch.send_keys(Keys.RETURN)

        select_btn_search = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))
        )
        time.sleep(1.4)
        select_btn_search.click()

        time.sleep(1.5)
        select_edit_tsp = wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="price_table"]/div/div/table/tbody[1]/tr[1]/td[7]/div/div/a'))
        ).click()
        
        return True
    except Exception as e:
        print(f"Erro na busca e seleção da tabela: {e}")
        return False

def fill_form(driver, wait, row):
    try:
        select_novo_trecho = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="new_redispatch_price_table"]/div[2]/div[2]/div/div[1]/div/button'))
        )
        select_novo_trecho.click()

        select_origem = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-stretch_origin_location_id-container"]'))
        ).click()
        input_origem = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        input_origem.send_keys(row['Origem'])
        time.sleep(1.9)
        input_origem.send_keys(Keys.RETURN)

        select_destino = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="select2-stretch_destination_location_id-container"]'))
        ).click()
        input_destino = wait.until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/span/span/span[1]/input'))
        )
        input_destino.send_keys(row['Destino'])
        time.sleep(2.2)
        input_destino.send_keys(Keys.RETURN)

        input_prazo = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="stretch_delivery_time"]'))
        )
        input_prazo.send_keys(row['Prazo'])
        
        print(row['Prazo'])
        
        return True
    except Exception as e:
        print(f"Erro ao preencher o formulário: {e}")
        return False

def save_and_confirm(driver, wait):
    try:
        
        select_save = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]'))
        )
        
        select_save.click()
        
        localizadores_botao = [
              (By.XPATH, '/html/body/div[10]/div/div[3]/button[1]'),
             (By.XPATH, '/html/body/div[11]/div/div[3]/button[1]')
             ]

        for localizador in localizadores_botao:
         try:
            confirm_save = wait.until(EC.element_to_be_clickable(localizador))
            break  # Sai do loop assim que encontrar o elemento
         except :
           continue  # Se não encontrar, tenta o próximo localizador

        if confirm_save:
         confirm_save.click()
         
         df.at[index, "Cadastro"] = "CADASTRADO"
        else:
          print("Botão não encontrado em nenhum dos locais")
        return True
    
    except Exception as e:
        print(f"Erro ao salvar e confirmar: {e}")
        return False

def handle_error(driver, wait1, index):    
    try:
        find_error_popup = driver.find_element(By.XPATH, '//*[@id="toast-container"]/div')
        if find_error_popup:
          close_error_popup = wait1.until(EC.element_to_be_clickable(By.XPATH, '//*[@id="toast-container"]/div/button'))
          close_error_popup.click()
    except:
        try:
            select_close = wait1.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="price-table-location-form"]/div[1]/button')))
            select_close.click()
        except Exception as e:
         print(f"Erro ao fechar o modal de erro:")

def process_row(driver, wait, row, index):
    if row["Cadastro"] == "CADASTRADO":
        return

    nome_tb_redespacho = row["Nome_Tb_Redespacho"]
    if pd.notna(nome_tb_redespacho) and nome_tb_redespacho.strip() != "":
        
        if fill_form(driver, wait, row):
            if save_and_confirm(driver, wait):
                    df.at[index, "Cadastro"] = "CADASTRADO"
            else:
                    handle_error(driver, wait, index)
        else:
                handle_error(driver, wait, index)
                
def open_screen_cad(driver, wait,):
    #Navegar para as tabelas de preço
 nav_cad = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div[1]/ul[2]/li[1]/a')))
 nav_cad.click()

 cad_price_tables = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="price_tables"]/a')))
 cad_price_tables.click()

 cad_table_redispatch = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="redispatch_price_table"]/a')))
 cad_table_redispatch.click()

def return_search(driver, wait):
    
    time.sleep(3)
    try:
     select_return_search = select_btn_search = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]/div/div/div/div[1]/ul/li[2]/a')))
     select_return_search.click()
    except:
        print("Não foi possível voltar para a tela de busca!")


realizar_login(driver, wait, url_esl, user_esl, password_esl)

open_screen_cad(driver, wait)

grouped_df = df.groupby('Nome_Tb_Redespacho')
# Iterating over each group


for name, group in grouped_df:
    print(name)
    print(group)
    
    # Assuming name represents the table name
    search_and_select_table(driver, wait, name)
    time.sleep(2)

    # Check if any item in the group is already registered
    if all(group['Cadastro'] == 'CADASTRADO'):
        
        print("Todos os itens já estão cadastrados!")
        time.sleep(3)
        
        return_search(driver, wait)
        continue
    
    time.sleep(2.5)

    # Process rows within the group
    for index, row in group.iterrows():
        process_row(driver, wait, row, index)
        print(index)
    
    return_search(driver, wait)
         

# This line seems misplaced. It should be outside the loops.
# Assuming it's for returning to search results.

         

# # Iterar pelas linhas do DataFrame
# for index, row in df.iterrows():
#     process_row(driver, wait, row, index)

# Fechar o WebDriver após a execução
df.to_excel(baseFile_name, sheet_name='Base', index=False, engine='openpyxl')
driver.quit()
