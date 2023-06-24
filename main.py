import sys
from PyQt5.QtWidgets import QApplication, QTextEdit, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QComboBox
from datetime import date
import sqlite3

class InsuranceApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Страховая компания")
        self.setGeometry(70, 100, 1200, 600)

        # Создаем базу данных
        self.conn = sqlite3.connect('insurance.db')
        self.cursor = self.conn.cursor()
        #таблица клиентов СК
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS clients
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            address TEXT,
                            phone TEXT,
                            email TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS contracts
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            client_id INTEGER,
                            type TEXT,
                            sum TEXT,
                            start_date TEXT,
                            end_date TEXT,
                            FOREIGN KEY (client_id) REFERENCES clients(id))''')
        self.conn.commit()

        # Создаем виджеты
        self.client_name_label = QLabel("Имя клиента:")
        self.client_name_edit = QLineEdit()
        self.client_address_label = QLabel("Адрес:")
        self.client_address_edit = QLineEdit()
        self.client_phone_label = QLabel("Телефон:")
        self.client_phone_edit = QLineEdit()
        self.client_email_label = QLabel("Email:")
        self.client_email_edit = QLineEdit()
        #кнопка
        self.add_client_button = QPushButton("Добавить клиента")
        self.add_client_button.clicked.connect(self.add_client)

        self.sort_clients_button = QPushButton('Отсортировать клиентов')
        self.sort_clients_button.clicked.connect(self.load_sort_clients)

        #таблица пользователей
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(5)#устанавливаем количество столбцов
        self.client_table.setHorizontalHeaderLabels(['ID', 'Имя', 'Адрес', 'Телефон', 'Email'])
        self.load_clients()


        #выпадающи список клиентов для контрактов
        self.contract_client_label = QLabel("Клиент:")
        self.contract_client_combo = QComboBox(self)
        self.load_contract_client_combo()

        # выпадающий список для клиентов
        self.client_combo = QComboBox(self)
        self.load_client_combo()

        self.del_client_button = QPushButton("Удалить клиента")
        self.del_client_button.clicked.connect(self.del_client)

        self.contract_type_label = QLabel("Тип договора:")
        self.contract_type_edit = QLineEdit()

        self.contract_start_date_label = QLabel("Дата начала:")
        cur_date = date.today()
        self.contract_start_date_edit = QLineEdit(f'{cur_date}')#по умолчанию текущая дата(можем изменить)

        self.contract_sum_label = QLabel("Сумма страхования")
        self.contract_sum_edit = QLineEdit()

        self.contract_end_date_label = QLabel("Дата окончания:")
        self.contract_end_date_edit = QLineEdit()

        self.add_contract_button = QPushButton("Добавить договор")
        self.add_contract_button.clicked.connect(self.add_contract)

        self.sort_contracts_button = QPushButton('Отсортировать договоры по пользователям')
        self.sort_contracts_button.clicked.connect(self.sort_contracts)

        self.del_contract_button = QPushButton("Удалить договор")
        self.del_contract_button.clicked.connect(self.del_contract)

        #выпадающий список контрактов
        self.contracts_combo = QComboBox()
        self.load_contracts_combo()

        #таблица контрактов
        self.contract_table = QTableWidget()
        self.contract_table.setColumnCount(7)
        self.contract_table.setHorizontalHeaderLabels(['ID', 'Клиент', 'Тип', 'Дата начала', 'Дата окончания', 'Сумма договора', 'Клиент ID'])
        self.load_contracts()

        #поля выводов
        self.output_client = QTextEdit(self)
        self.output_contracts = QTextEdit(self)

        # Создаем главный виджет и размещаем на нем все остальные виджеты
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.client_name_label)
        hbox1.addWidget(self.client_name_edit)
        hbox1.addWidget(self.client_address_label)
        hbox1.addWidget(self.client_address_edit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.client_phone_label)
        hbox2.addWidget(self.client_phone_edit)
        hbox2.addWidget(self.client_email_label)
        hbox2.addWidget(self.client_email_edit)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.add_client_button)
        hbox3.addWidget(self.sort_clients_button)


        hbox9 = QHBoxLayout()
        hbox9.addWidget(self.del_client_button)
        hbox9.addWidget(self.client_combo)

        vbox_client = QVBoxLayout()
        vbox_client.addLayout(hbox1)
        vbox_client.addLayout(hbox2)
        vbox_client.addLayout(hbox3)
        vbox_client.addLayout(hbox9)
        vbox_client.addWidget(self.client_table)
        vbox_client.addWidget(self.output_client)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.contract_client_label)
        hbox4.addWidget(self.contract_client_combo)
        hbox4.addWidget(self.contract_type_label)
        hbox4.addWidget(self.contract_type_edit)

        hbox5 = QHBoxLayout()
        hbox5.addWidget(self.contract_start_date_label)
        hbox5.addWidget(self.contract_start_date_edit)
        hbox5.addWidget(self.contract_end_date_label)
        hbox5.addWidget(self.contract_end_date_edit)

        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.add_contract_button)
        hbox6.addWidget(self.sort_contracts_button)

        hbox8 = QHBoxLayout()
        hbox8.addWidget(self.contract_sum_label)
        hbox8.addWidget(self.contract_sum_edit)

        hbox10 = QHBoxLayout()
        hbox10.addWidget(self.del_contract_button)
        hbox10.addWidget(self.contracts_combo)

        vbox_contract = QVBoxLayout()
        vbox_contract.addLayout(hbox4)
        vbox_contract.addLayout(hbox5)
        vbox_contract.addLayout(hbox8)
        vbox_contract.addLayout(hbox6)
        vbox_contract.addLayout(hbox10)
        vbox_contract.addWidget(self.contract_table)
        vbox_contract.addWidget(self.output_contracts)

        hbox7 = QHBoxLayout()
        hbox7.addLayout(vbox_client)
        hbox7.addLayout(vbox_contract)
        central_widget.setLayout(hbox7)

    def add_client(self):
        # Добавляем нового клиента в базу данных(для кнопки)
        name = self.client_name_edit.text()
        address = self.client_address_edit.text()
        phone = self.client_phone_edit.text()
        email = self.client_email_edit.text()
        #############ПРОВЕРКИ##################
        if name == '':
            self.output_client.clear()
            return self.output_client.append(f'Введите имя клиента!')
        if any(map(str.isdigit, name)):#тольок буквы
            self.output_client.clear()
            return self.output_client.append(f'Имя пользователя введено не корректно! Оно должно содержать только буквы!')
        if address == '':
            self.output_client.clear()
            return self.output_client.append(f'Введите адрес клиента!')
        if phone == '':
            self.output_client.clear()
            return self.output_client.append(f'Введите телефон клиента!')
        if not phone.isnumeric():
            self.output_client.clear()
            return self.output_client.append(f'Телефон пользователя введен не корректно! Номер телефона должен содержать только числа! Попробуйте еще раз!')
        if len(phone)!=11:
            self.output_client.clear()
            return self.output_client.append('Такого номера не существует! Номер телефона должен содержать 11 цифр! Попробуйте еще раз!')
        if email == '':
            self.output_client.clear()
            return self.output_client.append(f"Введите email клиента!")

        self.cursor.execute("INSERT INTO clients (name, address, phone, email) VALUES (?, ?, ?, ?)",
                            (name, address, phone, email))
        self.conn.commit()
        #очищаем поля
        self.client_name_edit.setText('')
        self.client_address_edit.setText('')
        self.client_phone_edit.setText('')
        self.client_email_edit.setText('')
        self.output_client.clear()
        self.output_client.append(f'Клиент {name} успешно добавлен!')
        #обновляем таблицы и боксы
        self.load_clients()
        self.load_client_combo()
        self.load_contract_client_combo()

    def load_clients(self):
        # Загружаем клиентов из базы данных и отображаем их в таблице
        self.client_table.setRowCount(0)
        self.cursor.execute("SELECT * FROM clients")
        clients = self.cursor.fetchall()
        for row_number, row_data in enumerate(clients):#clients - это список кортежей. т е сначала проходим по списку[clients], а затем по кортежу(row_data)
            self.client_table.insertRow(row_number)#enumerate - возвращает (счетчик, кортеж данных) row_number количсетво строк в табл
            for column_number, data in enumerate(row_data):
                self.client_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))#строка, столбец, данный/ data - это как данные кортежа (row_data)

    def load_sort_clients(self):
        # Загружаем клиентов из базы данных и отображаем их в таблице
        self.client_table.setRowCount(0)
        self.cursor.execute("SELECT * FROM clients ORDER BY name ASC")
        clients = self.cursor.fetchall()
        for row_number, row_data in enumerate(
                clients):  # clients - это список кортежей. т е сначала проходим по списку[clients], а затем по кортежу(row_data)
            self.client_table.insertRow(
                row_number)  # enumerate - возвращает (счетчик, кортеж данных) row_number количсетво строк в табл
            for column_number, data in enumerate(row_data):
                self.client_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def load_contract_client_combo(self):
        # Загружаем клиентов из базы данных и отображаем их в выпадающем списке
        self.contract_client_combo.clear()
        self.cursor.execute("SELECT * FROM clients")
        clients = self.cursor.fetchall()
        for client in clients:
            temp_str = f"id-{client[0]}, {client[1]}"
            self.contract_client_combo.addItem(temp_str, client[0])#имя и id#(self, text:str, data:any)

    def load_client_combo(self):
        # Загружаем клиентов из базы данных и отображаем их в выпадающем списке
        self.client_combo.clear()
        self.cursor.execute("SELECT * FROM clients")
        clients = self.cursor.fetchall()
        for client in clients:
            temp_str = f"id-{client[0]}, {client[1]}"
            self.client_combo.addItem(temp_str, client[0])  # имя и id

    def load_contracts_combo(self):
        # Загружаем контракты из базы данных и отображаем их в выпадающем списке
        self.contracts_combo.clear()
        self.cursor.execute("SELECT * FROM contracts")
        contracts = self.cursor.fetchall()
        for cur_contract in contracts:
            temp_str = f'id_contract-{cur_contract[0]}, id_client-{cur_contract[1]},  {cur_contract[2]},  {cur_contract[3]},  {cur_contract[4]}, {cur_contract[5]}'
            self.contracts_combo.addItem(temp_str, cur_contract[0])# текст и id по которому обращаемся

    def add_contract(self):
        # Добавляем новый договор в базу данных
        client_id = self.contract_client_combo.currentData()
        type_contract = self.contract_type_edit.text()
        start_date = self.contract_start_date_edit.text()
        end_date = self.contract_end_date_edit.text()
        sum_contract = self.contract_sum_edit.text()
        if type_contract == '':
            self.output_contracts.clear()
            return self.output_contracts.append(f'Введите тип страхового договора!')
        if any(map(str.isdigit, type_contract)):
            self.output_contracts.clear()
            return self.output_contracts.append(f"Проверьте корректность ввода типа страховки! Тип не должен содержать числа")
        if start_date == '':
            start_date = date.today()
        if end_date == '':
            self.output_contracts.clear()
            return self.output_contracts.append(f'Укажите дату окончания страхового договора!')
        if sum_contract == '':
            self.output_contracts.clear()
            return self.output_contracts.append(f"Укажите сумму страховой выплаты!")
        if not sum_contract.isnumeric():
            self.output_contracts.clear()
            return self.output_contracts.append(f"Проверьте корректность ввода суммы страхования! Она не должна содержать буквы")

        self.cursor.execute("INSERT INTO contracts (client_id, type, start_date, end_date, sum) VALUES (?, ?, ?, ?, ?)",
                            (client_id, type_contract, start_date, end_date, sum_contract))
        self.conn.commit()
        #очищаем поля ввода
        self.contract_type_edit.setText('')
        self.contract_end_date_edit.setText('')
        self.contract_sum_edit.setText('')
        self.output_contracts.clear()
        self.output_contracts.append(f"Страховой договор({type_contract}) клиента с id-{client_id} на сумму {sum_contract} руб. успешно зарегистрирован!")
        #обновляем боксы и таблицы вывода
        self.load_contracts()
        self.load_contracts_combo()

    def sort_contracts(self):
        """
        Сортировка договоров по данным клиента
        """
        # Загружаем договоры из базы данных и отображаем их в таблице
        self.contract_table.setRowCount(0)
        #объединяем таблицы клиенты и договоры по id клиента
        self.cursor.execute(
            "SELECT contracts.id, clients.name, contracts.type, contracts.start_date, contracts.end_date, contracts.sum, \
            contracts.client_id FROM contracts JOIN clients ON contracts.client_id = clients.id ORDER BY clients.name ASC")
        contracts = self.cursor.fetchall()
        for row_number, row_data in enumerate(contracts):
            self.contract_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.contract_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    def load_contracts(self):
        # Загружаем договоры из базы данных и отображаем их в таблице
        self.contract_table.setRowCount(0)
        #объединяем таблицы склиенты и договоры по id клиента
        self.cursor.execute(
            "SELECT contracts.id, clients.name, contracts.type, contracts.start_date, contracts.end_date, contracts.sum, \
            contracts.client_id FROM contracts JOIN clients ON contracts.client_id = clients.id")
        contracts = self.cursor.fetchall()
        for row_number, row_data in enumerate(contracts):
            self.contract_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.contract_table.setItem(row_number, column_number, QTableWidgetItem(str(data)))


    #удаление клиента
    def del_client(self):
        id_client = self.client_combo.currentData()
        self.cursor.execute("DELETE FROM clients WHERE id = ?", (id_client,))
        self.conn.commit()
        self.output_client.clear()

        self.output_client.append(f'Клиент(id-{id_client}) успешно удален!')
        self.load_clients()
        self.load_contract_client_combo()
        self.load_client_combo()

    def del_contract(self):
        """
        Удаление страхового договора по id договора
        """
        id_contract = self.contracts_combo.currentData()
        self.cursor.execute("DELETE FROM contracts WHERE id = ?", (id_contract,))
        self.output_contracts.clear()
        self.output_contracts.append(f'Выбранный договор(id-{id_contract}) успешно удалён')
        self.load_contracts()
        self.load_contracts_combo()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    insurance_app = InsuranceApp()
    insurance_app.show()
    sys.exit(app.exec_())