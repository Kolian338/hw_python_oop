import datetime as dt

# TODO Проверить на соответствие PEP8
# TODO Сделать проверку констант через typing
# TODO Документацию в гите
class Calculator:
    now = dt.datetime.now().date()

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_balance(self):
        return self.limit - self.get_today_stats()

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        amount_used_today = 0
        for record in self.records:
            if record.date == Calculator.now:
                amount_used_today += record.amount
        return amount_used_today

    def get_week_stats(self):
        amount_used_week = 0
        seven_days_ago_date = Calculator.now - dt.timedelta(days=7)

        for record in self.records:
            if Calculator.now >= record.date > seven_days_ago_date:
                amount_used_week += record.amount
        return amount_used_week


class Record:
    date_format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment

        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, Record.date_format).date()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_available = self.get_balance()
        if self.limit >= calories_available > 0:
            return f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_available} кКал"
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    USD_RATE = 74.29
    EURO_RATE = 84.07
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        currencies = {
            "rub": ("руб", CashCalculator.RUB_RATE),
            "usd": ("USD", CashCalculator.USD_RATE),
            "eur": ("Euro", CashCalculator.EURO_RATE)
        }
        if currency in currencies:
            name, rate = currencies.get(currency)
            balance = round(self.get_balance() / rate, 2)

            if self.limit >= balance > 0:
                return f"На сегодня осталось {abs(balance)} {name}"
            elif balance == 0:
                return "Денег нет, держись"
            else:
                return f"Денег нет, держись: твой долг - {abs(balance)} {name}"


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment="кофе"))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(
    Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))

print(cash_calculator.get_today_cash_remained("rub"))
# должно напечататься
# На сегодня осталось 555 руб