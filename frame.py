from io import StringIO

import appV2
import pandas as pd




url = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss"
product = appV2.GetProducts()
dic_data = product.products_amazon(url, start_page=0, end_page=1)
print(dic_data)

# Crear un DataFrame a partir del StringIO


df = pd.read_cv("product_app.csv")
df_2 = pd.DataFrame(dic_data)
df_2.to_csv("product2_app.csv", index=False)
print(df_2)