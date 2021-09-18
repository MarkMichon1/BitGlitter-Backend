from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.configmodels import Config


def has_one_time_page_ran():
    config = session.query(Config).first()
    return config.write_one_time_warning_ran


def one_time_page_has_ran_set():
    config = session.query(Config).first()
    config.write_one_time_warning_ran = True
    config.save()
