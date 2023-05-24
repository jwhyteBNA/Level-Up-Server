"""Module for generating games by user report"""
from django.shortcuts import render
from django.db import connection
from django.views import View

from levelupreports.views.helpers import dict_fetch_all

class UserEventList(View):
    def get(self, request):
        """Django reports"""
        with connection.cursor() as db_cursor:

            # Query to get all games along with the gamer first name, last name, and id
            db_cursor.execute("""
            SELECT
                gr.id AS gamer_id,
                u.first_name || ' ' || u.last_name AS full_name,
                g.title AS game,
                e.*
            FROM levelupapi_event e
            JOIN levelupapi_event_attendees ea 
                ON ea.event_id = e.id
            JOIN levelupapi_gamer gr
                ON ea.gamer_id = gr.id
            JOIN auth_user u
                ON gr.user_id = u.id
            JOIN levelupapi_game g 
                ON e.game_id = g.id
            ORDER BY gamer_id
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

            events_by_user = []

            for row in dataset:


                # Create a dictionary called game that includes
                # the name, description, number_of_players, maker,
                # game_type_id, and skill_level from the row dictionary
                event = {
                    "description": row['description'],
                    "date": row['date'],
                    "time": row['time'],
                    "game": row['game']
                }

                # See if the gamer has been added to the games_by_user list already
                user_dict = None
                for user_event in events_by_user:
                    if user_event['gamer_id'] == row['gamer_id']:
                        user_dict = user_event

                if user_dict:
                    # If user_dict is already in games_by_user list, append game to games list
                    user_dict['events'].append(event)
                else:
                    # If user is not on the games_by_user list, create + add user to list
                    events_by_user.append({
                        "gamer_id": row['gamer_id'],
                        "full_name": row['full_name'],
                        "events": [event]
                    })

        # The template string must match the file name of the html template
        template = 'users/list_with_events.html'

        # The context will be a dictionary that the template can access to show data
        context = {
            "userevent_list": events_by_user
        }

        return render(request, template, context)
