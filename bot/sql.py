import aiosqlite

from typing import Tuple, List, Dict, Optional, Any

class SQLParser:
    def __init__(self, file: str, create_statemets: List[str]) -> None:
        self.file = file
        self.create_statemets = create_statemets

    @staticmethod
    def connect(func):
        """Connection declorator to initialise the db when it is called"""
        async def wrapper(self, *args, **kwargs):
            # If we already have a connection to the database we wont need to reopen it
            if len(args) > 0 and isinstance(args[0], aiosqlite.Connection):
                res = await func(self, *args, **kwargs)
            else:
                async with aiosqlite.connect(self.file) as db:
                    res = await func(self, db, *args, **kwargs)

            return res
        return wrapper

    @connect
    async def raw_exec_select(self, db: aiosqlite.Connection, sql: str, vals: Tuple = ()) -> List[Tuple]: 
        """Get a result(s) from the database"""
        async with db.execute(sql, vals) as cursor:
            res = [row async for row in cursor]

        return res

    @connect
    async def raw_exec_commit(self, db: aiosqlite.Connection, sql: str, vals: Tuple = ()) -> None: 
        """Execute an sql statement and commit it to the database"""
        await db.execute(sql, vals)
        await db.commit()

    # Add custom db methods here if you need more control

    @connect
    async def initialise(self, db: aiosqlite.Connection):
        """Execute all the create statements on load"""
        for sql in self.create_statemets:
            await self.raw_exec_commit(db, sql)


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


