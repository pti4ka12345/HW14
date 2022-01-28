from flask import Flask, request
import json
from functions import *


app = Flask(__name__)



@app.route('/movie/title')
def page_movies():
   if request.method == 'GET':
       response = {}
       title = request.args.get('title')
       if title:
           query = f"""
           select 
               title,
               country,
               release_year,
               listed_in,
               description
           from netflix
           where title = '{title}'
           order by release_year desc
           limit 1
           """
           result = get_movie_by_id('netflix.db', query)
           if len(result):
               response = {
                   "title": result[0][0],
                   "country": result[0][1],
                   "release_year": result[0][2],
                   "listed_in": result[0][3],
                   "description": result[0][4],
               }
       return json.dumps(response)


@app.route('/movie/year')
def search_year():
    if request.method == 'GET':
        response = []
        start_year = request.args.get('start_year')
        end_year = request.args.get('end_year')
        if start_year and end_year:
            query = f"""
            select title,
            release_year,
            from netflix
            where release_year between {start_year} and {end_year}
            limit 100
            """
            result = get_movie_by_id('netflix.db', query)
            for line in result:
                line_dict = {
                    "title": line[0],
                    "release_year": line[1],
                     }
                response.append(line_dict)
        return json.dumps(response)


@app.route('/rating/children')
def rating_children():
    response = get_rating(['G'])
    return json.dumps(response)


@app.route('/rating/family')
def rating_family():
    response = get_rating(['PG', 'PG-13'])
    return json.dumps(response)


@app.route('/rating/adult')
def rating_adult():
    response = get_rating(['R', 'NC-17'])
    return json.dumps(response)


@app.route('/genre/<genre>')
def search_genre(genre):
    query = f"""
               select title,
               description
               from netflix
               where listed_in like '%{genre}%'
               order by release_year DESC 
               limit 10
               """
    result = get_movie_by_id('netflix.db', query)
    response = []
    for line in result:
        line_dict = {
            "title": line[0],
            "description": line[1],
        }
        response.append(line_dict)

    return json.dumps(response)


app.run()