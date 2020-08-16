import db
import utils
sql = db.DBManager()
sql.setup()
for x in range(1,4):
    print(x)
    utils.init()