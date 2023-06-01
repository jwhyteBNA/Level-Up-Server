"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all


class UserGameList(View):
    def get(self, request):
        """Django reports"""
        with connection.cursor() as db_cursor:

            # Query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT
                id,
                title,
                maker,
                game_type_id,
                number_of_players,
                skill_level,
                user_id,
                full_name
            FROM
                GAMES_BY_USER
            """)
            # Pass db_cursor to dict_fetch_all function to turn fetch_all() response into dictionary
            dataset = dict_fetch_all(db_cursor)

            # Take the flat data from the dataset, and build the
            # following data structure for each gamer.
            # This will be the structure of the games_by_user list:
            #
            # [
            #   {
            #     "id": 1,
            #     "full_name": "Admina Straytor",
            #     "games": [
            #       {
            #         "id": 1,
            #         "title": "Foo",
            #         "maker": "Bar Games",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       },
            #       {
            #         "id": 2,
            #         "title": "Foo 2",
            #         "maker": "Bar Games 2",
            #         "skill_level": 3,
            #         "number_of_players": 4,
            #         "game_type_id": 2
            #       }
            #     ]
            #   },
            # ]

            games_by_user = []

            for row in dataset:

                # Create a dictionary called game that includes
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                game = {
                    "title": row['title'],
                    "maker": row['maker'],
                    "skill_level": row['skill_level'],
                    "number_of_players": row['number_of_players'],
                    "game_type_id": row['game_type_id']
                }

                # See if the gamer has been added to the games_by_user list already
                user_dict = None
                for user_game in games_by_user:
                    if user_game['user_id'] == row['user_id']:
                        user_dict = user_game

                if user_dict:
                    # If user_dict is already in games_by_user list, append game to games list
                    user_dict['games'].append(game)
                else:
                    # If user is not on the games_by_user list, create + add user to list
                    games_by_user.append({
                        "user_id": row['user_id'],
                        "full_name": row['full_name'],
                        "games": [game]
                    })

        # The template string must match the file name of the html template
        template = 'users/list_with_games.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "usergame_list": games_by_user
        }

        return render(request, template, context)
