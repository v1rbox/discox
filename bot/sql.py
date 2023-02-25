import asyncio
from typing import Any, Dict, List, Optional, Tuple

import aiomysql
from .config import Config

class SQLParser:
    def __init__(self, file: str, create_statemets: List[str]) -> None:
        self.file = file
        self.create_statemets = create_statemets

    @staticmethod
    def connect(func):
        """Connection declorator to initialise the db when it is called"""

        async def wrapper(self, *args, **kwargs):
            # If we already have a connection to the database we wont need to reopen it
            if len(args) > 0 and isinstance(args[0], aiomysql.connection.Connection):
                res = await func(self, *args, **kwargs)
            else:
                pool = await aiomysql.create_pool(
                    host=Config.mysql_host,
                    port=Config.mysql_port,
                    user=Config.mysql_user,
                    password=Config.mysql_password,
                    db=Config.mysql_database,
                    autocommit=True,
                )
                async with pool.acquire() as db:
                    async with db.cursor() as cur:
                        res = await func(self, db, cur, *args, **kwargs)

            return res

        return wrapper

    @connect
    async def raw_exec_select(
        self,
        db: aiomysql.connection.Connection,
        cur: aiomysql.cursors.Cursor,
        sql: str,
        vals: Tuple = (),
    ) -> List[Tuple]:
        """Get a result(s) from the database"""
        sql = sql.replace("?", "%s")
        await cur.execute(sql, vals)
        res = await cur.fetchall()

        return res

    @connect
    async def raw_exec_commit(
        self,
        db: aiomysql.connection.Connection,
        cur: aiomysql.cursors.Cursor,
        sql: str,
        vals: Tuple = (),
    ) -> None:
        """Execute an sql statement and commit it to the database"""
        sql = sql.replace("?", "%s")
        await cur.execute(sql, vals)

    # Add custom db methods here if you need more control

    @connect
    async def initialise(
        self, db: aiomysql.connection.Connection, cur: aiomysql.cursors.Cursor
    ):
        """Execute all the create statements on load"""
        for sql in self.create_statemets:
            await self.raw_exec_commit(db, cur, sql)

    # In practise this was not very pratical, might be implemented in the futre
    # async def SELECT(self, table: str, rows: Tuple[str], where: Optional[Dict] = None):
    #     # Base SQL qurey
    #     sql = f"SELECT {', '.join(rows)} FROM {table}"
    #
    #     if where is not None:
    #         sql += f" WHERE {', '.join(where.keys())} "
    #
    #     res = await self.raw_exec(sql)
    #
    #     print(res)
    #     print(sql)
