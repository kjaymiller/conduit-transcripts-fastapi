from sqlmodel import Session, select
from .schema import Episode, engine

def all_episodes() -> list[Episode]:
    """Get all episode titles from the database"""
    with Session(engine) as session:
        return session.exec(select(Episode.title)).all()

def get_episode_by_title(title: str) -> Episode:
    """Get an episode by title"""
    with Session(engine) as session:
        return session.exec(select(Episode).where(Episode.title == title)).first()