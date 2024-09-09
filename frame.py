from io import StringIO

import app
import pandas as pd
import app_v2


def dictionary_a_csv_pandas(diccionario, nombre_archivo):
  df = pd.DataFrame(diccionario)  # Crear un DataFrame con los datos
  df.to_csv(nombre_archivo, index=False)  # Guardar como CSV sin índice


url = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss"
product = app_v2.GetProducts()
dic_data = product.products_amazon(url, start_page=0, end_page=4)

dictionary_a_csv_pandas(dic_data, "Product_app.csv")

df = pd.read_csv("Product_app.csv")
print(df)
