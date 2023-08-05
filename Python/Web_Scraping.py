from bs4 import BeautifulSoup
import requests
import json
import re

expresion_regular = r'\d{1,3}(?:,\d{3})*\.\d+'

divisas_colombia = []
divisas_peru = []
divisas_uruguay = []
divisas_mexico = []
divisas_argentina = []


#Web Scraping


# monedaCambio = input("Escriba a que moneda desea cambiar: ")
# monedaCambio = monedaCambio.lower()


urls_colombia = {"dolar":"https://www.google.com/finance/quote/USD-COP?sa=X&sqi=2&ved=2ahUKEwiphJfHprmAAxXnlokEHZZtDSIQmY0JegQIDRAr",
        "euro":"https://www.google.com/finance/quote/EUR-COP?sa=X&sqi=2&ved=2ahUKEwicpeS_qLmAAxW5TDABHbt7DHwQmY0JegQIDRAr",
        "libra esterlina": "https://www.google.com/finance/quote/GBP-COP?sa=X&ved=2ahUKEwjB2e2QqLmAAxWDRTABHcl1DuMQmY0JegQIBhAr",
        "yen japones":"https://www.google.com/finance/quote/JPY-COP?sa=X&sqi=2&ved=2ahUKEwj2xtXQqLmAAxVpVTABHUBkA9IQmY0JegQIDhAr",
        "won soul-coreano":"https://www.google.com/finance/quote/KRW-COP?sa=X&ved=2ahUKEwiHifv_qLmAAxXinYQIHYUuAXAQmY0JegQIEBAr"}

urls_peru = {"dolar":"https://www.google.com/finance/quote/USD-PEN?sa=X&ved=2ahUKEwif7ti2xryAAxVfkokEHbEhB_kQmY0JegQIARAn",
        "euro":"https://www.google.com/finance/quote/EUR-PEN?sa=X&ved=2ahUKEwjetueBx7yAAxUJhYkEHVl8DjEQmY0JegQIARAn",
        "libra esterlina": "https://www.google.com/finance/quote/GBP-PEN?sa=X&ved=2ahUKEwjegdONx7yAAxVbkIkEHUy0Av0QmY0JegQIARAn",
        "yen japones":"https://www.google.com/finance/quote/JPY-PEN?sa=X&ved=2ahUKEwj864-lx7yAAxXBj4kEHY7PDsAQmY0JegQIARAn",
        "won soul-coreano":"https://www.google.com/finance/quote/KRW-PEN?sa=X&ved=2ahUKEwjSsaOux7yAAxUDkYkEHTMDC0wQmY0JegQIARAn"}

urls_argentina = {"dolar":"https://www.google.com/finance/quote/USD-PEN?sa=X&ved=2ahUKEwif7ti2xryAAxVfkokEHbEhB_kQmY0JegQIARAn",
        "euro":"https://www.google.com/finance/quote/EUR-ARS?sa=X&ved=2ahUKEwiOq6iRyLyAAxX2rYkEHVFRAeQQmY0JegQIARAn",
        "libra esterlina": "https://www.google.com/finance/quote/GBP-ARS?sa=X&ved=2ahUKEwiIht2byLyAAxUbjIkEHYPrANsQmY0JegQIARAn",
        "yen japones":"https://www.google.com/finance/quote/JPY-ARS?sa=X&ved=2ahUKEwjF2IqkyLyAAxUIlIkEHS43CtAQmY0JegQIARAn",
        "won soul-coreano":"https://www.google.com/finance/quote/KRW-ARS?sa=X&ved=2ahUKEwjI0-uqyLyAAxUZlYkEHVcWCGIQmY0JegQIARAn"}

urls_uruguay = {"dolar":"https://www.google.com/finance/quote/USD-UYU?sa=X&ved=2ahUKEwjussDEyLyAAxVLk4kEHeGwCQoQmY0JegQIARAn",
        "euro": "https://www.google.com/finance/quote/EUR-UYU?sa=X&ved=2ahUKEwjW_f3PyLyAAxXGkYkEHZgQDEQQmY0JegQIARAn",
        "libra esterlina": "https://www.google.com/finance/quote/GBP-UYU?sa=X&ved=2ahUKEwjHyfjgyLyAAxV_j4kEHd8oDycQmY0JegQIARAn",
        "yen japones":"https://www.google.com/finance/quote/JPY-UYU?sa=X&ved=2ahUKEwji5eXvyLyAAxW3kYkEHcY2AFAQmY0JegQIARAn",
        "won soul-coreano":"https://www.google.com/finance/quote/KRW-UYU?sa=X&ved=2ahUKEwi3_dD5yLyAAxVwlokEHYmmA_oQmY0JegQIARAn"}

urls_mexico = {"dolar":"https://www.google.com/finance/quote/USD-MXN?sa=X&ved=2ahUKEwj6qdeFybyAAxVHtokEHdcgDbMQmY0JegQIARAn",
        "euro":"https://www.google.com/finance/quote/EUR-MXN?sa=X&ved=2ahUKEwj9lvCOybyAAxVehYkEHQZACg8QmY0JegQIARAn",
        "libra esterlina": "https://www.google.com/finance/quote/GBP-MXN?sa=X&ved=2ahUKEwixquSUybyAAxUbkIkEHfxPDMMQmY0JegQIARAn",
        "yen japones":"https://www.google.com/finance/quote/JPY-MXN?sa=X&ved=2ahUKEwix6v2aybyAAxVLkYkEHYPwAV0QmY0JegQIARAn",
        "won soul-coreano":"https://www.google.com/finance/quote/KRW-MXN?sa=X&ved=2ahUKEwjAwbehybyAAxWKhIkEHd36DrAQmY0JegQIARAn"}

content = [urls_colombia, urls_argentina, urls_mexico, urls_peru, urls_uruguay]
count = 0

for e in content:
        elemento = e.values()
        for i in elemento:
                
                page = requests.get(i) #Inspeccionamos la pagina
                soup = BeautifulSoup(page.content, "html.parser") #Pasamos la pagina a documento html

                #Divisas

                dv = soup.find_all("div", class_ = "YMlKec fxKbKc") #Establecemos el tipo de etiqutea | Verificamos si es clase o id | Ponemos el nombre
                conversion_dato = str(dv) #Pasamos el dato de arriba a un string para analizarlo con expresiones regulares
                valor_numerico = re.search(expresion_regular, conversion_dato).group()

                #Establecemos un contador el cual va a ir agregando a cada lista su respectivo elemento
                # Como los valores que se imprimen son str vamos a pasarlos a flotantes
                if count < 5:
                        divisas_colombia.append(valor_numerico)
                        count = count + 1
                elif count < 10:
                        divisas_argentina.append(valor_numerico)
                        count = count + 1

                elif count < 15:
                        divisas_mexico.append(valor_numerico)
                        count = count + 1

                elif count < 20:
                        divisas_peru.append(valor_numerico)
                        count = count + 1
                elif count < 25:
                        divisas_uruguay.append(valor_numerico)
                        count = count + 1

divisas_colombia = list(map(lambda x: float(x.replace(',', '')), divisas_colombia))
divisas_argentina = list(map(lambda x: float(x.replace(',', '')), divisas_argentina))
divisas_peru = list(map(lambda x: float(x.replace(',', '')), divisas_peru))
divisas_mexico = list(map(lambda x: float(x.replace(',', '')), divisas_mexico))
divisas_uruguay = list(map(lambda x: float(x.replace(',', '')), divisas_uruguay))

        
# crendo Formato Json 

data = {}

data["Dolar"]=[]
data["Euro"]=[]
data["Libras_Esterlinas"]=[]
data["Yen_Japones"]=[]
data["Won_Sul-Coreano"]=[]

data["Dolar"].append({
    "Peru": divisas_peru[0],
    "Colombia": divisas_colombia[0],
    "Uruguay": divisas_uruguay[0],
    "Mexico": divisas_mexico[0],
    "Argentina": divisas_argentina[0]
})
data["Euro"].append({
    "Peru": divisas_peru[1],
    "Colombia": divisas_colombia[1],
    "Uruguay": divisas_uruguay[1],
    "Mexico": divisas_mexico[1],
    "Argentina": divisas_argentina[1]
})
data["Libras_Esterlinas"].append({
    "Peru": divisas_peru[2],
    "Colombia": divisas_colombia[2],
    "Uruguay": divisas_uruguay[2],
    "Mexico": divisas_mexico[2],
    "Argentina": divisas_argentina[2]
})
data["Yen_Japones"].append({
    "Peru": divisas_peru[3],
    "Colombia": divisas_colombia[3],
    "Uruguay": divisas_uruguay[3],
    "Mexico": divisas_mexico[3],
    "Argentina": divisas_argentina[3]
})
data["Won_Sul-Coreano"].append({
    "Peru": divisas_peru[4],
    "Colombia": divisas_colombia[4],
    "Uruguay": divisas_uruguay[4],
    "Mexico": divisas_mexico[4],
    "Argentina": divisas_argentina[4]
})

with open("data.json", "w") as file:
        json.dump(data, file, indent=4)