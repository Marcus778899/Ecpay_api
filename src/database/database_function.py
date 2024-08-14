import logging
from .cassandra_init import CassadnraDB

def select_item_price(item: str):
    db_driver = CassadnraDB()
    query = f"SELECT * FROM level_payment WHERE level = '{item}';"
    logging.debug(query)
    try:
        rows = db_driver.session.execute(query)
        return rows.current_rows[0]
    except Exception as e:
        logging.error(e)
        return None
    finally:
        db_driver.close_driver()
