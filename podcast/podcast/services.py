from podcast.adapters.repository import AbstractRepository


def get_all_podcasts(repo: AbstractRepository, page):
    podcasts = sorted(repo.get_podcasts(), key=lambda podcast: podcast.title)
    res = podcasts[(page - 1) * 10: (page - 1) * 10 + 10]
    return res, res == podcasts[-len(res):]


def get_podcasts_by_title(repo: AbstractRepository, condition:str, page):
    podcasts = repo.get_podcasts()
    res = []
    for podcast in podcasts:
        if condition.lower() in podcast.title.lower():
            res.append(podcast)
    podcasts = sorted(res, key=lambda podcast: podcast.title)
    res = podcasts[(page - 1) * 10: (page - 1) * 10 + 10]
    return res, res == podcasts[-len(res):]


def get_podcasts_by_language(repo: AbstractRepository, condition, page):
    podcasts = repo.get_podcasts()
    res = []
    for podcast in podcasts:
        if condition.lower() in podcast.language.lower():
            res.append(podcast)
    podcasts = sorted(res, key=lambda podcast: podcast.title)
    res = podcasts[(page - 1) * 10: (page - 1) * 10 + 10]
    return res, res == podcasts[-len(res):]


def get_podcasts_by_author(repo: AbstractRepository, condition, page):
    podcasts = repo.get_podcasts()
    res = []
    for podcast in podcasts:
        if condition.lower() in podcast.author.name.lower():
            res.append(podcast)
    podcasts = sorted(res, key=lambda podcast: podcast.title)
    res = podcasts[(page - 1) * 10: (page - 1) * 10 + 10]
    return res, res == podcasts[-len(res):]


def get_podcasts_by_categories(repo: AbstractRepository, condition, page):
    podcasts = repo.get_podcasts()
    res = []
    for podcast in podcasts:
        for c in podcast.categories:
            if condition.lower() in c.name.lower():
                res.append(podcast)
    podcasts = sorted(res, key=lambda podcast: podcast.title)
    res = podcasts[(page - 1) * 10: (page - 1) * 10 + 10]
    return res, res == podcasts[-len(res):]


def get_category_podcasts(repo: AbstractRepository, podcasts):
    category_list1 = []
    for podcast in podcasts:
        category_list2 = []
        for category in podcast.categories:
            category_list2.append(category.name)
        category_list1.append(" | ".join(category_list2))
    return category_list1
