from tkinter import Tk, filedialog
import pandas as pd
import os
import csv


def select_path():
    try:
        root = Tk()
        root.withdraw()
        path = filedialog.askdirectory(title='Seleccionar el path')
        return path
    except Exception as e:
        raise Exception(f'Error en la función select_path: {e}')


def get_date_from_name(file):
    try:
        date = file[-12:-4]
        return date[:4], date[-4:-2], date[-2:]
    except Exception as e:
        raise Exception(f'Error en la función get_date_from_name: {e}')


def clean_duplicates(df):
    try:
        return df.drop_duplicates()
    except Exception as e:
        raise Exception(f'Error en la función clean_duplicates: {e}')


def filter_by_date(df, date):
    try:
        year, month, day = date
        target_date = pd.to_datetime(f'{year}-{month}-{day}').date()
        column_date_type = pd.to_datetime(
            df["Fecha y hora actualizacion tiena x"]).dt.date
        df['Fecha y hora actualizacion tiena x'] = column_date_type
        return df[df['Fecha y hora actualizacion tienda x'] == target_date]
    except Exception as e:
        raise Exception(f'Error en la función filter_by_date: {e}')


def rename_columns(df):
    try:
        return df.rename(columns={
            'Precio 1': 'Precio 1 tienda x',
            'Precio 2': 'Precio 2 tienda x',
            'Precio 3': 'Precio 3 tienda x',
            'SKU': 'Sku tienda x',
            'URL': 'URL tienda x',
            'Posee stock': 'Stock tienda x'
        })
    except Exception as e:
        raise Exception(f'Error en la función rename_columns: {e}')


def transform_data(df):
    try:
        df_columns = list(df.columns)
        df_list = []
        stores = [string[4:] for string in df_columns if 'Sku' in string]

        for store in stores:
            df_store = pd.DataFrame()
            df_store['SKU'] = df[f'Sku {store}']
            df_store['Categoría'] = df['Categoria (nivel 1)']
            df_store['Marca'] = df['Marca']
            df_store['Nombre'] = df['Nombre']
            df_store['Precio 1'] = df[f'Precio 1 {store}']
            df_store['Precio 2'] = df[f'Precio 2 {store}']
            df_store['Precio 3'] = df[f'Precio 3 {store}']
            df_store['Stock'] = df[f'Stock {store}']
            df_store['Tienda'] = store
            df_store['Fecha'] = df['Fecha y hora actualizacion tienda x']
            df_list.append(df_store)

        df = pd.concat(df_list, ignore_index=True)
        df = df[df['SKU'] != 0]
        df = df[df['Stock'] == 'con_stock']
        df['Categoría'] = df['Categoría'].replace({
            'niÃ±os': 'niños',
            'ninos': 'niños',
            'linea blanca': 'línea blanca',
            'zapatos': 'zapatos y zapatillas',
            'tecno': 'tecnología'
        })
        return df.drop_duplicates()
    except Exception as e:
        raise Exception(f'Error en la función transform_data: {e}')


def save_transformed_file(df, path, file_name):
    try:
        output_dir = f'{path}/output'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_file_name = f'{os.path.splitext(file_name)[0]}-transformado.csv'
        df.to_csv(f'{path}/output/{output_file_name}', index=False)
        print(f'Archivo transformado y guardado como {output_file_name}')
    except Exception as e:
        raise Exception(f'Error en la función save_transformed_file: {e}')


def detect_delimiter(file, encodings):
    for encoding in encodings:
        try:
            with open(file=file, mode='r', encoding=encoding) as f:
                file_content = ""
                # Leer máximo 10 líneas
                for _ in range(10):
                    line = f.readline()
                    if not line:
                        break
                    file_content += line
                sniffer = csv.Sniffer()
                delimiter = sniffer.sniff(file_content).delimiter
            return delimiter
        except Exception as e:
            raise Exception(f'Error en la función detect_delimiter: {e}')
