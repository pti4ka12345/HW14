import sqlite3
from collections import Counter


def get_movie_by_id(db, query):

    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result


def get_rating(rating):
    response = []
    if len(rating) > 1:
        str_rating = "','".join(rating)
    else:
        str_rating = "".join(rating)
    print(str_rating)
    query = f""" 
        select title, country, release_year, listed_in, description, rating
               from netflix
               where rating in ('{str_rating}')
               limit 100
               """
    result = get_movie_by_id('netflix.db', query)
    for line in result:
        line_dict = {
            "title": line[0],
            "rating": line[1],
            "description": line[2],
        }
        response.append(line_dict)
    return response


def search_pair(actor1, actor2):
    query = f"select \"cast\" from netflix " \
            f"where \"cast\" like '%{actor1}%' and \"cast\" like '%{actor2}%' "
    result = get_movie_by_id('netflix.db', query)
    result_list = []
    for line in result:
        line_list = line[0].split(',')
        result_list += line_list
        counter = Counter(result_list)
        print(counter)
        actors_list = []
        for key, value in counter.items():
            if value > 2 and key.strip() not in [actor1, actor2]:
                actors_list.append(key)
        return actors_list

print(search_pair('Rose McIver','Ben Lamb'))



