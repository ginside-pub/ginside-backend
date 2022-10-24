from ginside.core.config import cfg


def test_get_url():
    db_name = cfg.database.database

    assert cfg.database.url is None
    assert cfg.database.get_url() == (
        'postgresql://ginside:ginside@'
        f'127.0.0.1:5432/{db_name}'
    )

    cfg.database.host = 'ginside'
    assert cfg.database.get_url() == (
        f'postgresql://ginside:ginside@ginside:5432/{db_name}'
    )

    cfg.database.url = f'postgresql://server:5432/{db_name}'
    assert cfg.database.get_url() == cfg.database.url

    cfg.database.host = '127.0.0.1'
    cfg.database.url = None
