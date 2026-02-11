from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models

from django.conf import settings

from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Teams
        teams = [
            {"name": "Team Marvel"},
            {"name": "Team DC"}
        ]
        team_ids = db.teams.insert_many(teams).inserted_ids

        # Users
        users = [
            {"name": "Iron Man", "email": "ironman@marvel.com", "team": team_ids[0]},
            {"name": "Captain America", "email": "cap@marvel.com", "team": team_ids[0]},
            {"name": "Batman", "email": "batman@dc.com", "team": team_ids[1]},
            {"name": "Superman", "email": "superman@dc.com", "team": team_ids[1]},
        ]
        db.users.insert_many(users)
        db.users.create_index([("email", 1)], unique=True)

        # Activities
        activities = [
            {"user": "ironman@marvel.com", "activity": "Running", "duration": 30},
            {"user": "cap@marvel.com", "activity": "Cycling", "duration": 45},
            {"user": "batman@dc.com", "activity": "Swimming", "duration": 60},
            {"user": "superman@dc.com", "activity": "Flying", "duration": 120},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {"team": "Team Marvel", "points": 150},
            {"team": "Team DC", "points": 180},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {"user": "ironman@marvel.com", "workout": "Pushups", "reps": 50},
            {"user": "cap@marvel.com", "workout": "Situps", "reps": 60},
            {"user": "batman@dc.com", "workout": "Pullups", "reps": 40},
            {"user": "superman@dc.com", "workout": "Squats", "reps": 100},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
