import sqlalchemy as sa
from sqlalchemy import Table, create_engine, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import DeclarativeBase, Session
import os


class Base(DeclarativeBase):
    pass


# engine1 = create_engine("sqlite:///"+os.path.join(os.getcwd(), "fifa_rankings.bak.sqlite"))
engine2 = create_engine("sqlite:///"+os.path.join(os.getcwd(), "fifa_rankings.sqlite"))

# table1 = Table("men_ranking", Base.metadata, autoload_with=engine1)
table2 = Table("fifa_country", Base.metadata, autoload_with=engine2)
table3 = Table("men_ranking", Base.metadata, autoload_with=engine2)

# with Session(engine1) as ss1:
#     select_stmt = sa.select(table1.c["country_code"], table1.c["name"], table1.c["zone"]).select_from(table1).order_by(sa.asc(table1.c["name"]))
#     results = ss1.execute(select_stmt).all()
#     with Session(engine2) as ss2:
#         for result in results:
#             print(result)
#             insert_stmt = insert(table2).values(result)
#             on_conflict_stmt = insert_stmt.on_conflict_do_nothing()
#             ss2.execute(on_conflict_stmt)
#             ss2.commit()
#         ss2.close()
#     ss1.close()


with Session(engine2) as ss:
    select_stmt = select(table2.c.country_code, table2.c.country_name, table3.c.current_points).select_from(table2).\
        join(table3, onclause=table2.c.country_code).where(table2.c.country_name.like("%saint%"))
    
    results = ss.execute(select_stmt).all()
    print(results)
