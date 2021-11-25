from bg_backend.bitglitter.config.config import session
from bg_backend.bitglitter.config.readmodels.readmodels import StreamFrame


def flush_inactive_frames():
    session.query(StreamFrame).filter(StreamFrame.is_complete == False).delete()
    session.commit()