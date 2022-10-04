 # Общие рекомендаци - добавить везде docstrings, type hinting. 
 # Все строки вынести как константы наверх модуля и в местах, где их используем, просто подставлять значения.



# Рекомендовал бы оптимизировать импортm импортируя datetime из datetime
import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        
        # Сделал бы более читаемым, используя бы классическое if/else, причем отталкиваясь от if,  а не if not
        self.date = (
            dt.datetime.now().date() if
            not
            
            # сделал бы константу date format на уровне модуля
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        
        # Итерироваться надо используя не название класса, а объект
        for Record in self.records:
            
            # используется в двух местах, можно напимер сделать @property today
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        
        # используется в двух местах, можно например сделать @property today
        today = dt.datetime.now().date()
        for record in self.records:
            
            # Сравнение можно уложить в одну строчку
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                
                
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    
    # Зачем оставлен комментарий? В продакшн коде этого надо избегать, для документации есть docstring
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        
        # Х это очень плохой нейминг - не понятно, что значит переменная
        x = self.limit - self.get_today_stats()
        
        # Использован бэкслеш для переноса строки, надо исправить
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        
        # От else можно избавиться и просто делать return (уменьшаем вложенность)
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    
    # Я бы вынес константы наверх модуля, либо название перменных в классе сделал в lower case
    # Комментарии явно лишние, все понятно по переменным что они значат
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    def get_today_cash_remained(self, currency,
                                
                                # Константы можно использовать, не передавая в функцию, считаю параметры лишними
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        
        # Я бы использовал два словаря: для получения type в нужном формте из currency и для получения convertaion rate исходя из кода валюты
        # Это позволило бы избежать такого ветвления по if, просто дважды бы вызывали метод get словарей
        currency_type = currency
        
        
        cash_remained = self.limit - self.get_today_stats()
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
            
        # Беползеный elif блок. 
        # Если мы уверены, что на вход придет 100% один из трех заранее обозначенных типов валюты, то просто делаем currency_type = 'руб' без elif
        # Если не уверены, то надо обрабатывать ситуацию получения неправильного кода валюты.
        elif currency_type == 'rub':
            
            # Почему остаток денег становится 1.00?
            cash_remained == 1.00
        
            currency_type = 'руб'
         
        if cash_remained > 0:
            return (
                   
                # Я бы упростил строчку вынеся округление куда-нибудь выше по коду
                # Таким образом не пришлось бы проводить округление в двух местах, а также не пришлось бы разбивать строчку на две
                # А ещё ее консистентно: используем format или f строку?
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
                
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        
        # Можно просто делать return без использования elif
        elif cash_remained < 0:
            
            return 'Денег нет, держись:' \
                   
                   # Я бы упростил строчку вынеся округление куда-нибудь выше по коду
                   # Таким образом не пришлось бы дважды проводить округление в двух местах, не пришлось бы разбивать строчку на две
                   # Не консистентно: используем format или f строку?
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    
    # Зачем переопредлелять родительский метод, не изменяя его поведение? Нет необходимости в этой функции
    # Таже уфнкция просто не будет работать, так как ничего не возвращает
    def get_week_stats(self):
        super().get_week_stats()
