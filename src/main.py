import os
import pandas as pd
import utilities


def main():
    try:
        path = utilities.select_path()
        if not path:
            print("No se seleccionó una ruta válida.")
            return

        file_list = os.listdir(path)
        
        for file in file_list:
            try:
                if file.endswith('.csv'):
                    date = utilities.get_date_from_name(file)
                    if not date:
                        print(f"Fecha no válida en el archivo {file}, saltar archivo.")
                        continue

                    delimiter = utilities.detect_delimiter(f'{path}/{file}')
                    df_1 = pd.read_csv(f'{path}/{file}', 
                                       encoding='windows-1252', sep=delimiter)
                    df_2 = utilities.clean_duplicates(df_1)
                    df_3 = utilities.filter_by_date(df_2, date)
                    df_4 = utilities.rename_columns(df_3)
                    df_5 = utilities.transform_data(df_4)
                    utilities.save_transformed_file(df_5, path, file)

            except Exception as e:
                print(f"Error al procesar el archivo {file}: {e}")

    except Exception as e:
        print(f"Error general: {e}")


if __name__ == "__main__":
    main()
