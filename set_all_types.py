from data import db_session
from data.types import Type

def main():
    db_session.global_init("db/plan_maker.db")
    db_sess = db_session.create_session()
    file = open('types.txt','r',encoding='utf-8').readlines()
    file = list(map(lambda x:x.rstrip('\n'),file))
    for i in file:
        type = Type(title=i)
        db_sess.add(type)
    # db_sess.add(Type(title='попить пива'))
    db_sess.commit()

if __name__ == '__main__':
    main()
