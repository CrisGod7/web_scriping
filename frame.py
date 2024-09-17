import appV2
import pandas as pd

while True:

    option = int(input("[1]Scripting\n[2]Crear csv\n[3] Leer csv\n[4] Salir\n"))
    if option == 1:
        url = "https://www.amazon.com/s?k=samsung&ref=nb_sb_noss"
        end_page = int(input("numero de paginas"))
        product = appV2.GetProducts()
        dic_data= product.products_amazon(url, start_page=0, end_page=end_page)

    elif option == 2:
        df_2 = pd.DataFrame(dic_data)
        nombre_csv = input("Nombre del csv: ")
        df_2.to_csv(nombre_csv+".csv", index=False)
    elif option == 3:

        nombre_csv = input("Nombre del csv: ")
        df_r = pd.read_csv(nombre_csv+".csv")
        print(df_r)



# Crear un DataFrame a partir del StringIO


