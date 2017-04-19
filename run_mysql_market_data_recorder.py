import json

import sqlalchemy as sa

if __name__ == '__main__':
    engine_fmt = '{dialect}{driver}://{user}:{password}@{host}/{dbname}'
    db_json_fp = 'conf/db.json'
    with open(db_json_fp, 'r') as fp:
        db_conf = json.load(fp)

    engine_arg = engine_fmt.format(**db_conf)
    engine = sa.create_engine(engine_arg)
