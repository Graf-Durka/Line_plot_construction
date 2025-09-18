import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import argparse

def read_data_file(file_path):
    """
    Чтение данных из файла CSV или Excel без заголовков.
    
    Parameters
    ----------
    file_path : str
        Путь к файлу с данными. Поддерживаются форматы .csv, .xlsx, .xls
        
    Returns
    -------
    pandas.DataFrame
        DataFrame с данными из файла без заголовка столбцов
        
    Raises
    ------
    ValueError
        Если формат файла не поддерживается
        
    """
    
    #Определяем расширения файла,в дальнейшем используем подходящую библиотечную функию
    file_extension = os.path.splitext(file_path)[1]
    
    if file_extension == '.csv':
        return pd.read_csv(file_path, header=None)
    elif file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path, header=None)
    else:
         #В случае, если файл имеет иное расширение, вызов исключения
         raise ValueError(f"Unsupported file format: {file_extension}")

def safe_convert_to_float(value):
    """
    Безопасное преобразование значения в float с заменой запятых на точки.
    
    Parameters
    ----------
    value : any
        Значение для преобразования
        
    Returns
    -------
    float
        Преобразованное числовое значение
    """
    try:
        if isinstance(value, str):
            value = value.replace(',', '.')
        return float(value)
    except (ValueError, TypeError):
        raise ValueError(f"Не удалось преобразовать значение в число: {value}")

def parse_data_types(pd_data, data_type):
    """
    Парсинг и преобразование типов данных из сырого DataFrame.
    
    Ожидает, что первая строка содержит метки: x_label, y_label, title.
    Остальные строки содержат данные для построения графика.
    
    Parameters
    ----------
    pd_data : pandas.DataFrame
        Сырые данные из файла (первая строка - метаданные)
    data_type : str
        Тип данных для оси X: 'date' для дат, 'num' для числовых данных
        
    Returns
    -------
    tuple
        (pd_data_clean, x_label, y_label, title) - очищенные данные и метки
        
    Raises
    ------
    ValueError
        Если не удается преобразовать типы данных
           Examples
    --------
    >>> demo_data = create_demo_data()
    >>> print(demo_data.head())
       time  temperature
    0     1           15
    1     2           16
    2     3           18
    Examples
    --------
    >>> raw_data = pd.DataFrame([['Date', 'Temperature', 'График температуры'],
    ...                         ['2023-01-01', '20,5', ''],
    ...                         ['2023-01-02', '22,3', '']])
    >>> clean_data, x_label, y_label, title = parse_data_types(raw_data, 'date')
    """
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
    
    # Обрабатываем значения с запятыми с проверкой
    pd_data_clean[y_label] = pd_data_clean[y_label].apply(safe_convert_to_float)
    
    return (pd_data_clean, x_label, y_label, title)

def create_demo_data():
    """
    Создание демонстрационных данных для тестирования.
    
    Returns
    -------
    pandas.DataFrame
        DataFrame с демонстрационными данными о температуре за 10 часов
        
    """
    data = {'time': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
            'temperature': [15, 16, 18, 20, 22, 23, 22, 20, 19, 17]}
    return pd.DataFrame(data)

def configure_plot_settings(x_label, y_label, title, data_type):
    """
    Настройка параметров графика.
    
    Parameters
    ----------
    x_label : str
        Метка для оси X
    y_label : str
        Метка для оси Y
    title : str
        Заголовок графика
    data_type : str
        Тип данных: 'date' для форматирования дат
    """
    plt.xlabel(x_label, fontsize=12)
    
    if data_type == 'date':
        plt.ylabel(f'{y_label} (°C)', fontsize=12)
    else:
        plt.ylabel(y_label, fontsize=12)
    
    plt.title(title, fontsize=14)
    
    # Форматируем дату в нужный для построения графика формат
    if data_type == 'date':
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.xticks(rotation=45)
    else:
        plt.xticks()
    
    # Форматируем ось y для чисел
    plt.gca().yaxis.set_major_formatter('{x:.2f}')
    plt.yticks()
    
    plt.grid(True)
    plt.legend()

def plot_data(pd_data, x_label, y_label, title, data_type):
    """
    Построение графика на основе очищенных данных.
    
    Parameters
    ----------
    pd_data : pandas.DataFrame
        Очищенные данные для построения графика
    x_label : str
        Метка для оси X
    y_label : str
        Метка для оси Y
    title : str
        Заголовок графика
    data_type : str
        Тип данных: 'date' для форматирования дат, иначе числовой
        
    """
    plt.figure(figsize=(10, 6))
    
    # Строим график
    plt.plot(
        pd_data[x_label], 
        pd_data[y_label], 
        label=y_label
    )
    
    # Настраиваем параметры графика
    configure_plot_settings(x_label, y_label, title, data_type)

def plot_demo_data():
    """
    Построение демонстрационного графика температуры.
    
    Использует данные из create_demo_data() для построения простого графика.
    Полезно для тестирования и демонстрации функциональности.
    
    Examples
    --------
    >>> plot_demo_data()
    >>> plt.show()  # для отображения графика
    """
    data_frame = create_demo_data()
    
    plt.figure(figsize=(10, 6))
    plt.plot(data_frame['time'], data_frame['temperature'], label='Температура')
    
    # Настраиваем параметры графика
    configure_plot_settings('Время (часы)', 'Температура (°C)', 'Температура за день', 'num')

def main():
    """
    Основная функция для запуска скрипта из командной строки.
    
    Обрабатывает аргументы командной строки и запускает соответствующий режим:
    - С файлом данных: построение графика из файла
    - Без аргументов: демонстрационный режим
    
    Examples
    --------
    >>> # Запуск из командной строки:
    >>> # python plotter.py temperature_data.csv --data-type date
    >>> # python plotter.py  # для демо-режима
    """
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
