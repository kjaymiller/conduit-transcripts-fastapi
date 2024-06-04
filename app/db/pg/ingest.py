import arrow
from app.db.pg.schema import Episode, engine
from sqlmodel import Session
import frontmatter
from pathlib import Path

FMT = r"MMMM[\s+]D[\w+,\s+]YYYY"


def episodes_from_path(directory:Path) -> None:
    """Seed the databases with episodes from a file"""
    with Session(engine) as session:
        episodes = [from_episode_from_frontmatter(path) for path in directory.iterdir()]
        session.add_all(episodes)
        session.commit()


def from_episode_from_frontmatter(filepath: Path) -> Episode:
    """Create an episode from frontmatter and content"""
    post = frontmatter.loads(filepath.read_text())
    return Episode(
            title=post['title'],
            content=post.content,
            date=arrow.get(post['pub_date'], FMT).date(),
            description=post['description'],
            url=post['url'],
    )

if __name__ == "__main__":
    episodes_from_path(Path("../transcripts"))