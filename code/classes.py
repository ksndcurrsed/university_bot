import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3
import json
import time

url = 'https://org.fa.ru/'

class univer:
    def __init__(self, course:str):
        """
        Инициализация

        @param course: str. Переменная получаемая из общения с пользователем, равна от 1 до 4
        @param url: str. Константа, переменная, хранящая ссылку сайта
        @param conn: sqlite. Инициализация подключения к базе данных
        @param cur: sqlite. Инициализация курсора базы данных
        
        
        """
        self.course = course
        self.url = url
        self.conn = sqlite3.connect('./database/datebase.db')
        self.cur = self.conn.cursor()


    def __connection(self):
        """
        Подключение к базе данных. Приватная функция, обращение только внутри класса
        Используя курсор делает обращение к базе данных, обращаясь к переменной password_rn
        Создает таблицу users_login_data, если такой нет, состоящую из столбцов chat_id (INTEGER), username (TEXT), password (TEXT) для последующего хранения данных учетных записей пользователей
        """

        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS users_login_data (
        chat_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL
        )
        ''')

    def __setup(self):
        """
        Запуск браузера. Приватная функция, обращение только внутри класса.
        @param o: options object. Хранит настройки для запуска браузера, а именно detach, отвечающий за то, чтобы браузер не закрывался сразу, как только выполнил код
        @param driver: webdriver. Инициализация браузера
        Браузер выбирается последней строкой, в нашем случае обычный хром
        """
        self.driver = webdriver.Chrome()

    def __login(self, username, password):
        """
        Функция авторизации на сайт посредствам данных username password из базы данных. Приватная функция, обращение только внутри класса.
        @param username: str. Переменная, хранящая логин пользователя
        @param password: str. Переменная, хранящая пароль пользователя
        @param url: str. Константа, переменная, хранящая ссылку сайта

        driver.get(url) - открытие ссылки
        driver.find_element(By.NAME, 'USER_LOGIN').send_keys(username) - поиск поля input по имени 'USER_LOGIN' и отправка ключей с помощью send_keys, а именно переменной username
        driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(password) - поиск поля input по имени 'USER_PASSWORD' и отправка ключей с помощью send_keys, а именно переменной password
        driver.find_element(By.CLASS_NAME, 'login-btn').click() - поиск кнопки по имени 'login-btn' и нажатие на нее
        """
        self.driver.get(url)
        self.driver.find_element(By.NAME, 'USER_LOGIN').send_keys(username)
        self.driver.find_element(By.NAME, 'USER_PASSWORD').send_keys(password)
        self.driver.find_element(By.CLASS_NAME, 'login-btn').click()

    
    def schedule(self):
        """
        Функция получения расписания как PDF-файла и отправка его пользователю в чат
        @param linkresp: str. Ссылка на сайт, которая собирается из готовой ссылки и вставки переменной course
        @param response: requests.get. Инициализация запроса к сайту
        
        Создается, либо перезаписывается файл расписание.pdf после get-запроса на сайт из переменной linkresp, и полученные данные записывают в файл

        """
        linkresp = 'http://www.fa.ru/fil/kaluga/student/Documents/%d0%a0%d0%b0%d1%81%d0%bf%d0%b8%d1%81%d0%b0%d0%bd%d0%b8%d0%b5/'+ self.course + '%20%d0%ba%d1%83%d1%80%d1%81.pdf'
        response = requests.get(linkresp)
        path = './bot_output/расписание.pdf'
        with open(path, 'wb') as file:
            file.write(response.content)
            return path
    

    def parsing(self, logdata):
        """
        Функция парсинга расписания.
        @param logdata: list. Переменная, хранящая логин и пароль пользователя
        @param url: str. Константа, переменная, хранящая ссылку сайта
        @param table: webdriver.find_element. Инициализация таблицы
        @param rows: webdriver.find_elements. Инициализация строк таблицы
        @param table_data: list. Переменная, хранящая данные из таблицы
        @param cells: webdriver.find_elements. Переменная хранящая ячейки с данными
        @param row_data: list. Массив, хранящий все значения из строки внутри таблицы table
        @param json_data: str. Переменная, хранящая данные из таблицы в формате json
        @param book: list. Переменная, хранящая данные из таблицы в формате json
        @param text_output: str. Переменная, хранящая итоговый формат сообщения для отправки пользователю
        
        Функция вызывает функции __setup и __login(передавая в нее данные массива logdata ввиде [username, password]), впоследствии открытие сайта с зачетной книжкой, time.sleep(5) используется для
        загрузки сайта до конца. Драйвер ищет таблицу по CSS_SELECTOR, внутри ищет строки по TAG_NAME, и по всем ячейкам найденным по TAG_NAME добавляет в массив row_data данные. Затем открывается файл
        Json и туда записываются данные из полученного массив table_data. Дальше открывается этот же json файл, и данные читаются в переменную book, затем в пустую переменную text_output формируется вывод

        """
        self.__setup()
        self.__login(logdata[0], logdata[1])
        self.driver.get('https://org.fa.ru/app/profile;mode=edu/marks')
        time.sleep(5)
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.table-hover.table-sm')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        table_data = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            row_data = [cell.text for cell in cells]
            table_data.append(row_data)
        json_data = json.dumps(table_data, ensure_ascii=False)
        with open('./bot_output/table_data.json', 'w', encoding='utf-8') as f:
            f.write(f'[{json_data[5:-1]}]')
        with open('./bot_output/table_data.json', 'r', encoding='utf-8') as f:
            book = json.load(f)
        text_output = ''
        for data in range(0, len(book)):
            for cnt in range(0,9):
                if book[data][cnt] == '':
                    book[data][cnt] = 'Пусто'
            text_output = text_output + f'✅ Дисциплина: {book[data][0]}\n Вид контроля: {book[data][1]}\n Результат: {book[data][5]}\n Текущий контроль: {book[data][6]}\n Работа в семестре: {book[data][7]}\n Зачет/экзамен: {book[data][8]}\n Итого: {book[data][9]} \n \n'
        return text_output
    
    def database_auth(self, login_data, chat_id):
        """
        Функция авторизации в базу данных. 
        @param login_data: list. Данные входа на сайт для сохранении в базу данных 
        @param chat_id: int. Значения идентификационного номера чата, присваиваемого пользователю ботом от Telegram.
        @param existing_record: str

        Функция обращается к функции __connection. с помощью курсора выбирает все данные из строки в переменную existing_record. Если эта строка есть, полученные новые данные перезаписываются, а пользователь получает соответствующее сообщение
        иначе данные просто сохраняются в базу данных, с указанием этого в сообщении
        """
        self.__connection()
        self.cur.execute("SELECT * FROM users_login_data WHERE chat_id=?", (chat_id,))
        existing_record = self.cur.fetchone()
        if existing_record:
            self.cur.execute("UPDATE users_login_data SET username=?, password=? WHERE chat_id=?", (login_data[0],login_data[1],chat_id))
            self.conn.commit()
            self.conn.close()
            return 'Ваша запись уже была в базе данных!\nДанные изменены ✅'

        else:
            self.cur.execute("""INSERT INTO users_login_data (username, password, chat_id) VALUES (?, ?, ?)""", (login_data[0],login_data[1],chat_id))
            self.conn.commit()
            self.conn.close()
            return 'Вашей записи не было в базе данных!\nДанные сохранены ✅'
    
    def check_user_id_to_parsing(self, chat_id):
        """
        Функция проверки наличия данных о пользователе в базе данных.
        @param chat_id. int. Значение идентификационного номера чата, присваиваемого пользователю ботом от Telegram.
        @param result. list. Переменная равная строке в базе данных по значению chat_id
        @param username. string. Переменная, хранящая значение из result по индексу [0]
        @param password. string. Переменная, хранящее значение из result по индексу [1]

        Функция вызывает __connection, после находит строку с полученным chat_id, проверяет наличие такой строки. если такой строки нет, она возвращает False, если есть, возвращает данные для авторизации на сайте
        """
        self.__connection()
        self.cur.execute("""SELECT * FROM users_login_data WHERE chat_id = ?""", (chat_id,))
        result = self.cur.fetchone()
        if result is None:
            self.conn.close()
            return False
        else:
            username = result[1] 
            password = result[2]
            logdata = [username, password]
            self.conn.close()
            return logdata

