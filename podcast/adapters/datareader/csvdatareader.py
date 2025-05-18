import os
import csv
from pathlib import Path

from podcast.adapters.memory_repository import MemoryRepository
from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, Episode, Author, Category


class CSVDataReader:
    def read_csv_file(self, filename: str):
        with open(filename, encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)

            # Read first line of the CSV file.
            headers = next(reader)

            # Read remaining rows from the CSV file.
            for row in reader:
                # Strip any leading/trailing white space from data read.
                row = [item.strip() for item in row]
                yield row  # a_list = [], a_list.append()

    def load_episodes(self, data_path: Path, repo: AbstractRepository):
        episodes_filename = str(Path(data_path) / "episodes.csv")
        for data_row in self.read_csv_file(episodes_filename):
            episode = Episode(
                id=data_row[0],
                podcast=data_row[1],
                title=data_row[2],
                link=data_row[3],
                length=data_row[4],
                description=data_row[5],
                date=data_row[6],
            )
            podcast = repo.get_podcast_by_id(int(data_row[1]))
            podcast.add_episode(episode)
            repo.add_episode(episode)

    def load_podcasts(self, data_path: Path, repo: AbstractRepository):
        podcasts_filename = str(Path(data_path) / "podcasts.csv")
        author_id, category_id = 1, 1
        for data_row in self.read_csv_file(podcasts_filename):
            podcast = Podcast(
                podcast_id=int(data_row[0]),
                title=data_row[1],
                image=data_row[2],
                description=data_row[3] if data_row[3] else "",
                language=data_row[4],
                website=data_row[6],
                author=Author(author_id, data_row[7] if data_row[7] else "Unknown"),
                itunes_id=int(data_row[8]),
            )
            for category_name in data_row[5].split(" | "):
                category_set = repo.get_categories()
                for c in category_set:
                    if c.name == category_name:
                        continue
                category = Category(category_id, category_name)
                repo.add_category(category)
                podcast.add_category(category)
                category_id += 1
            author_id += 1
            repo.add_podcast(podcast)

    def populate(self, data_path: Path, repo: AbstractRepository):
        self.load_podcasts(data_path, repo)
        self.load_episodes(data_path, repo)

