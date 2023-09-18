from rest_framework.views import APIView, Request, Response, status
from django.forms import model_to_dict
from .models import Team
from utils import data_processing
from exceptions import (
    ImpossibleTitlesError,
    InvalidYearCupError,
    NegativeTitlesError
)


class TeamView(APIView):
    def post(self, request: Request) -> Response:
        try:
            data_processing(request.data)
            team = Team.objects.create(**request.data)
            converted_team = model_to_dict(team)
            return Response(converted_team, status.HTTP_201_CREATED)
        except (
            ImpossibleTitlesError,
            InvalidYearCupError,
            NegativeTitlesError
        ) as err:
            return Response(
                {"error": err.message},
                status.HTTP_400_BAD_REQUEST
                )

    def get(self, request: Request) -> Response:
        teams = Team.objects.all()
        converted_teams = [model_to_dict(team) for team in teams]
        return Response(converted_teams, status.HTTP_200_OK)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id: int) -> Response:
        try:
            team = model_to_dict(Team.objects.get(id=team_id))
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )
        return Response(team, status.HTTP_200_OK)

    def patch(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )

        for key, value in request.data.items():
            setattr(team, key, value)

        team.save()
        converted_team = model_to_dict(team)
        return Response(converted_team, status.HTTP_200_OK)

    def delete(self, request: Request, team_id: int) -> Response:
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response(
                {"message": "Team not found"}, status.HTTP_404_NOT_FOUND
            )
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
