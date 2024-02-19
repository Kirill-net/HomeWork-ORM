import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale

DSN = "postgresql://postgres:admin@localhost:5432/netology_db2"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)                  # создаем таблицы

Session = sessionmaker(bind=engine)    # открываем сессию
session = Session()

publisher1 = Publisher(name='Пушкин')
publisher2 = Publisher(name='Пелевин')
session.add_all([publisher1, publisher2])

book1 = Book(title='Капитанская дочка', publisher=publisher1)
book2 = Book(title='Руслан и Людмила', publisher=publisher1)
book3 = Book(title='Евгений Онегин', publisher=publisher1)
book4 = Book(title='Чапаев и пустота', publisher=publisher2)
book5 = Book(title='SNUFF', publisher=publisher2)
book6 = Book(title='Числа', publisher=publisher2)
session.add_all([book1, book2, book3, book4, book5, book6])

shop1 = Shop(name='Буквоед')
shop2 = Shop(name='Лабиринт')
shop3 = Shop(name='Книжный дом')
session.add_all([shop1, shop2, shop3])

stock1 = Stock(book=book1, shop=shop2, count=6)
stock2 = Stock(book=book2, shop=shop3, count=4)
stock3 = Stock(book=book3, shop=shop1, count=8)
stock4 = Stock(book=book4, shop=shop2, count=12)
stock5 = Stock(book=book5, shop=shop3, count=2)
stock6 = Stock(book=book6, shop=shop1, count=10)
session.add_all([stock1, stock2, stock3, stock4, stock5, stock6])

sale1 = Sale(price=350, date_sale=('2022-10-10'), count=5, stock=stock3)
sale2 = Sale(price=400, date_sale=('2022-10-12'), count=8, stock=stock5)
sale3 = Sale(price=900, date_sale=('2022-04-03'), count=6, stock=stock4)
sale4 = Sale(price=700, date_sale=('2022-01-10'), count=2, stock=stock6)
sale5 = Sale(price=800, date_sale=('2022-02-18'), count=3, stock=stock5)
sale6 = Sale(price=350, date_sale=('2022-03-24'), count=4, stock=stock1)
sale7 = Sale(price=500, date_sale=('2022-05-20'), count=4, stock=stock1)
sale8 = Sale(price=500, date_sale=('2022-11-11'), count=5, stock=stock2)
session.add_all([sale1, sale2, sale3, sale4, sale5, sale6, sale7, sale8])
session.commit()

def get_shops(name):
    result = (session.query(Book.title, Shop.name, Sale.price, Sale.date_sale)
              .join(Publisher).join(Stock).join(Shop).join(Sale))
    if name.isdigit():
        result = result.filter(Publisher.id == name)
    else:
        result = result.filter(Publisher.name == name)
    for r in result.all():
        print(f'{r[0]:<30} | {r[1]:<15} | {r[2]:<8} | {r[3]}')

if __name__ == '__main__':
    name = input('Автор - ')
    get_shops(name)
    session.close()

