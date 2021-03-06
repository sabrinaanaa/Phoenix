from .sqldatabase import SqlDatabase
from .sqlTableUpdater import SqlTableUpdater

class CoreUpdater(SqlTableUpdater):

    def __init__(self, tableName: str = None, tableColumns: list = None, coreInfo: dict = None):
        if not tableColumns:
            tableColumns = []

        if not coreInfo:
            coreInfo = {}

        if not tableColumns:
            tableColumns = (
                ("UUID", "TEXT PRIMARY KEY"),
                ("display_version", "TEXT"),
                ("license", "TEXT"),
                ("authors", "TEXT"),
                ("manufacturer", "TEXT")
            )

        SqlTableUpdater.__init__(self, tableName if tableName else "", tableColumns, coreInfo)

    def updateTable(self):

        with SqlDatabase(self.dbFile, autoCommit=True) as db:
            self.updateColumns(db)

            # Get Libretro system list
            libretroSystems = self.libretroSystemList()

            # Iterate through all cores available
            for k, v in self.coreInfo['cores'].items():

                # Ignore anything that isn't an emulator
                if "categories" not in v or v["categories"] != "Emulator":
                    continue

                # Iterate through the columns, defined up above
                values = []
                for row in self.columnsDict.keys():
                    # The key contains the name of the core
                    if row == "UUID":
                        values.append(k)
                    # Directly copy data for the other columns, their keys match the libretro .info file keys exactly
                    elif row in v:
                        values.append(v[row])
                    elif row in ["UUID", "display_version", "license", "authors", "manufacturer"]:
                        values.append("")

                db.insert(self.tableName, self.columnsDict.keys(), values)

if __name__ == "__main__":

    from collections import OrderedDict

    updater = CoreUpdater("core", columns)
    updater.updateTable()
