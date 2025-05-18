import pytest

from podcast import MemoryRepository, CSVDataReader
from podcast.adapters import memory_repository
from utils import get_project_root

# the csv files in the test folder are different from the csv files in the covid/adapters/data folder!
# tests are written against the csv files in tests, this data path is used to override default path for testing
TEST_DATA_PATH = get_project_root() / "tests" / "data"


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    CSVDataReader().populate(TEST_DATA_PATH, repo)
    return repo

