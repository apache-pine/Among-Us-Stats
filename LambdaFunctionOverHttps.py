import sys
import logging
import rds_config
import pymysql
# rds settings
rds_host = "among-us-stats.coj0kcdco6tl.us-west-2.rds.amazonaws.com"
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name,
                           passwd=password, db=db_name, connect_timeout=5)
except pymysql.MySQLError as e:
    logger.error(
        "ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

item_count = 0

with conn.cursor() as cur:
    cur.execute("select * from match_summary")
    for row in cur:
        item_count += 1
        logger.info(row)
        # print(row)
conn.commit()

# def handler(event, context):
#     """
#     This function fetches content from MySQL RDS instance
#     """

#     item_count = 0

#     with conn.cursor() as cur:
#         cur.execute("select * from match_summary")
#         for row in cur:
#             item_count += 1
#             logger.info(row)
#             # print(row)
#     conn.commit()

print(f"Added {item_count} items from RDS MySQL table")
