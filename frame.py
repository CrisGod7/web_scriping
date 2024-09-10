from io import StringIO

import appV2
import pandas as pd


def diccionario_a_csv_pandas(diccionario, nombre_archivo):
    df = pd.DataFrame([diccionario])  # Crear un DataFrame con una sola fila
    df.to_csv(nombre_archivo, index=False)  # Guardar como CSV sin índice


url = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss"
product = appV2.GetProducts()
dic_data = product.products_amazon(url, start_page=0, end_page=4)
# Crear un DataFrame a partir del StringIO

diccionario_a_csv_pandas(dic_data, "Product_app.csv")

df = pd.read_csv("Product_app.csv")
