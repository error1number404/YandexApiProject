from data import db_session
from data.countries import Country

def main():
    db_session.global_init("db/plan_maker.db")
    db_sess = db_session.create_session()
    file = open('countries.txt','r',encoding='utf-8').readlines()
    file = list(map(lambda x:x.rstrip('\n'),file))
    for i in file:
        country = Country(name=i)
        db_sess.add(country)
    db_sess.commit()

if __name__ == '__main__':
    main()
