import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import argparse

def read_data_file(file_path):

    """Чтение данных из файла"""

    #Определяем расширения файла,в дальнейшем используем подходящую библиотечную функию
    file_extension = os.path.splitext(file_path)[1]
    
    if file_extension == '.csv':
        return pd.read_csv(file_path, header=None)
    elif file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, header=None)
    else:
         #В случае, если файл имеет иное расширение, вызов исключения
         raise ValueError(f"Unsupported file format: {file_extension}")

def parse_data_types(pd_data, data_type):

    """Парсинг и преобразование типов данных"""

    # Извлекаем название графика и осей
    x_label = pd_data.iloc[0, 0]
    y_label = pd_data.iloc[0, 1]
    title = pd_data.iloc[0, 2]
    
    # Удаляем первую строку, где находились данные графика
    pd_data_clean = pd_data.drop(0)
    
    # Удаляем третий столбец если существует
    if len(pd_data_clean.columns) > 2:
        pd_data_clean = pd_data_clean.drop(pd_data_clean.columns[2], axis=1)
    
    # Переименовываем столбцы
    pd_data_clean.columns = [x_label, y_label]
    
    # Преобразуем типы данных
    if data_type == 'date':
        pd_data_clean[x_label] = pd.to_datetime(pd_data_clean[x_label])
    else:
        pd_data_clean[x_label] = pd.to_numeric(pd_data_clean[x_label])
    
    # Обрабатываем начения с запятыми
    pd_data_clean[y_label] = pd_data_clean[y_label].astype(str).str.replace(',', '.').astype(float)
    
    return (pd_data_clean, x_label, y_label, title)

def create_demo_data():

    """Создание демонстрационных данных"""

    data = {'time': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
            'temperature': [15, 16, 18, 20, 22, 23, 22, 20, 19, 17]}
    return pd.DataFrame(data)

def plot_data(pd_data, x_label, y_label, title, data_type):

    """Отрисовка графика"""

    plt.figure(figsize=(10, 6))
    
    # Определяем подпись для легенды
    legend_label = y_label if data_type == 'date' else y_label
    
    # Строим график
    plt.plot(
        pd_data[x_label], 
        pd_data[y_label], 
        label=legend_label
    )
    
    plt.xlabel(x_label, fontsize=12)
    
    if data_type == 'date':
        plt.ylabel(f'{y_label} (°C)', fontsize=12)
    else:
        plt.ylabel(y_label, fontsize=12)
    
    plt.title(title, fontsize=14)
    
    # Форматируем дату в нужный для построения графика формат
    if data_type == 'date':
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())e
        plt.xticks(rotation=45, )
    else:
        plt.xticks()
    
    # Форматируем ось y для чисел
    plt.gca().yaxis.set_major_formatter('{x:.2f}')
    plt.yticks()
    
    plt.grid(True)
    plt.legend()

def plot_demo_data():

    """Отрисовка демонстрационных данных"""
    
    data_frame = create_demo_data()
    
    plt.figure(figsize=(10, 6))
    plt.plot(data_frame['time'], data_frame['temperature'], label='Температура')
    
    plt.title('Температура за день')
    plt.xlabel('Время (часы)')
    plt.ylabel('Температура (°C)')
    
    plt.gca().yaxis.set_major_formatter('{x:.2f}')
    plt.yticks()
    plt.xticks()
    
    plt.legend()
    plt.grid(True)

def main():

    """Основная функция"""

    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', type=str, nargs='?')
    parser.add_argument('--data-type', type=str, choices=['date', 'num', 'base'], default='base')
    args = parser.parse_args()
    
    #Если файл имеет необрабатываемое расширение, вывод ошибки данных
    try:
        if args.file_path:

            # Обработка файла с данными
            pd_data = read_data_file(args.file_path)
            pd_data_clean, x_label, y_label, title = parse_data_types(pd_data, args.data_type)
            plot_data(pd_data_clean, x_label, y_label, title, args.data_type)
        else:
            # Использование демо-данных
            print("Использование демонстрационных данных")
            plot_demo_data()
            
        plt.show()

    except ValueError as e:
        print(f"Ошибка данных: {e}")



if __name__ == "__main__":
    main()

"""Запуск основной функции"""
