import json

import sqlalchemy as sa

from iem import config

if __name__ == '__main__':
    base_engine_fmt = '{dialect}+{driver}://{user}:{password}@{host}'
    db_json_fp = 'conf/db.json'
    with open(db_json_fp, 'r') as fp:
        db_conf = json.load(fp)

    base_engine = sa.create_engine(base_engine_fmt.format(**db_conf))
    create_fmt = 'CREATE DATABASE IF NOT EXISTS {dbname}'
    base_engine.execute(create_fmt.format(**db_conf))

    engine_fmt = base_engine_fmt + '/{dbname}'
    engine = sa.create_engine(engine_fmt.format(**db_conf))

    metadata = sa.MetaData()
    mkt_table = config.markets_table(metadata)
    bundles_table = config.bundles_table(metadata)
    assets_table = config.assets_table(metadata)
    metadata.create_all(engine)

    mkt_conf = config.read_markets()
    # TODO: Transform into Pandas dataframes and insert?
