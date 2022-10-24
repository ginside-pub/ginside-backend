from ginside.core.config import cfg


def test_get_url():
    assert cfg.database.url is None
    assert cfg.database.get_url() == (
        'postgresql://ginside:ginside@'
        '127.0.0.1:5432/ginside'
    )

    cfg.database.host = 'ginside'
    assert cfg.database.get_url() == (
        'postgresql://ginside:ginside@ginside:5432/ginside'
    )

    cfg.database.url = 'postgresql://server:5432/ginside'
    assert cfg.database.get_url() == cfg.database.url

    cfg.database.host = '127.0.0.1'
    cfg.database.url = None
