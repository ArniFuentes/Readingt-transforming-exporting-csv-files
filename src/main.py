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
        csv_files = [file for file in file_list if file.endswith('.csv')]

        if not csv_files:
            print("El directorio seleccionado no contiene archivos .csv.")
            return

        encodings = ["windows-1252", "iso-8859-15", "ascii", "utf-16", "utf-8-sig", "utf-16-le",
                     "utf-16-be", "big5", "iso-8859-1", "shift-jis", "euc-kr", "gb18030", "cp437",
                     "mac-roman", "koi8-r", "gb2312", "cp1251", "cp850", "utf-8",
                     ]

        for file in csv_files:
            try:
                date = utilities.get_date_from_name(file)
                if not date:
                    print(f"Fecha no válida en el archivo {
                          file}, saltar archivo.")
                    continue

                delimiter = utilities.detect_delimiter(
                    f'{path}/{file}', encodings)
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
