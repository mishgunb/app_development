from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import User, Address, Product, Order

connect_url = "postgresql://postgres:postgres@localhost:5432/test_db"
engine = create_engine(connect_url, echo=False)
session_factory = sessionmaker(engine)


def fill_db_with_data():
    with session_factory() as session:
        user1 = User(username="John Doe", email="jdoe@example.com")
        user2 = User(username="John Wick", email="john@wick.com")
        user3 = User(username="John Silver", email="john@silver.com")
        user4 = User(username="John Bronze", email="john@bronze.com")
        user5 = User(username="John Gold", email="john@gold.com")


        address1 = Address(country="Belarus", city="Minsk", street="Wall Street")
        address2 = Address(country="Russia", city="Podolsk", street="Pushkina")
        address3 = Address(country="Canada", city="Ontario", street="Avenu 1")
        address4 = Address(country="Germany", city="Berlin", street="Avenu 2")
        address5 = Address(country="France", city="Paris", street="Avenu 3")
        

        user1.addresses = [address1]
        user2.addresses = [address2]
        user3.addresses = [address3]
        user4.addresses = [address4]
        user5.addresses = [address5]
    
        
        product1 = Product(name="Airpods")
        product2 = Product(name="BoomBox")
        product3 = Product(name="Cola")
        product4 = Product(name="Doritos")
        product5 = Product(name="Espresso")

        order1 = Order()
        order1.user = user1
        order1.address = address1
        order1.product = product1

        order2 = Order()
        order2.user = user2
        order2.address = address2
        order2.product = product2

        order3 = Order()
        order3.user = user3
        order3.address = address3
        order3.product = product3

        order4 = Order()
        order4.user = user4
        order4.address = address4
        order4.product = product4

        order5 = Order()
        order5.user = user5
        order5.address = address5
        order5.product = product5

        session.add(order1)
        session.add(order2)
        session.add(order3)
        session.add(order4)
        session.add(order5)

        session.commit()

fill_db_with_data()

