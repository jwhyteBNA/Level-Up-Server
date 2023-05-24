import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from levelupapi.models import Event, Gamer, Game


class EventTests(APITestCase):

    # Add any fixtures you want to run to build the test database
    fixtures = ['users', 'tokens', 'gamers', 'game_types', 'games', 'events']

    def setUp(self):
        self.gamer = Gamer.objects.first()
        self.game= Game.objects.first()
        token = Token.objects.get(user=self.gamer.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_event(self):
        """
        Ensure we can create a new event.
        """
        # Define the endpoint in the API to which
        # the request will be sent
        url = "/events"

        # Define the request body
        data = {
            "description": "A game event",
            "date": "2024-03-01",
            "time": "15:30:00",
            "organizer": 1,
            "game": 2
        }

        # Initiate request and store response
        response = self.client.post(url, data, format='json')

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Assert that the properties on the created resource are correct
        self.assertEqual(json_response["description"], "A game event")
        self.assertEqual(json_response["date"], "2024-03-01")
        self.assertEqual(json_response["time"], "15:30:00")
        self.assertEqual(json_response["organizer"]["id"], 1)
        self.assertEqual(json_response["game"]["id"], 2)

    def test_get_event(self):
        """
        Ensure we can get an existing event.
        """

        # Seed the database with a game
        event = Event()
        event.description = "A game event"
        event.date = "2024-03-01"
        event.time = "15:30:00"
        event.organizer = Gamer.objects.first()
        event.game = Game.objects.first()
        event.save()

        # Initiate request and store response
        response = self.client.get(f"/events/{event.id}")

        # Parse the JSON in the response body
        json_response = json.loads(response.content)

        # Assert that the game was retrieved
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the values are correct
        self.assertEqual(json_response["description"], "A game event")
        self.assertEqual(json_response["date"], "2024-03-01")
        self.assertEqual(json_response["time"], "15:30:00")
        self.assertEqual(json_response["organizer"]["id"], 1)
        self.assertEqual(json_response["game"]["id"], 1)

    def test_change_event(self):
        """
        Ensure we can change an existing event.
        """
        event = Event()
        event.description = "A game event"
        event.date = "2024-03-01"
        event.time = "15:30:00"
        event.organizer = Gamer.objects.first()
        event.game = Game.objects.first()
        event.save()

        # DEFINE NEW PROPERTIES FOR EVENT
        data = {
            "description": "An updated game event",
            "date": "2023-10-31",
            "time": "08:30:00",
            "organizer": 1,
            "game": 1
        }

        response = self.client.put(f"/events/{event.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET game again to verify changes were made
        response = self.client.get(f"/events/{event.id}")
        json_response = json.loads(response.content)

        # Assert that the properties are correct
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["description"], "An updated game event")
        self.assertEqual(json_response["date"], "2023-10-31")
        self.assertEqual(json_response["time"], "08:30:00")
        self.assertEqual(json_response["organizer"]["id"], 1)
        self.assertEqual(json_response["game"]["id"], 1)

    def test_delete_event(self):
        """
        Ensure we can delete an existing event.
        """
        event = Event()
        event.description = "A game event"
        event.date = "2024-03-01"
        event.time = "15:30:00"
        event.organizer = Gamer.objects.first()
        event.game = Game.objects.first()
        event.save()

        # DELETE the event you just created
        response = self.client.delete(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET the event again to verify you get a 404 response
        response = self.client.get(f"/events/{event.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
