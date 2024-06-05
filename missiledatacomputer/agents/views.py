from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.http import HttpResponse, JsonResponse
from .models import Agent, LocationRecord
import json

# index as the entry url
def index(request):
    return HttpResponse("Agents application is online. Route is accessible")

# create a new agent and save to db
@require_POST
def create_agent(request):
    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)

        # Id will be automatically generated, only model_type is compulsory field
        model_type = data.get('model_type')
        name = data.get('name', None)
        owner = data.get('owner', None)
        hostility = data.get('hostility', None)
        stationary = data.get('stationary', None)

        #create the object
        try:
            new_agent = Agent.objects.create(
                model_type=model_type,
                name=name, owner=owner,
                hostility=hostility,
                stationary=stationary,
                )
        except ValueError:
            return JsonResponse({'error': 'Invalid Field'}, status=400)

        return JsonResponse({'message': 'New Agent Created.', 'id':new_agent.id }, status=201)

    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Erro'}, status=500)

# get an agent's info
@require_GET
def get_agent(request, id):
    try:
        agent = get_object_or_404(Agent, pk=id)
        agent_info = {
            'id': agent.id,
            'model_type': agent.model_type,
            'name': agent.name,
            'owner': agent.owner,
            'hostility': agent.hostility,
            'stationary': agent.stationary
        }
        return JsonResponse(agent_info, status=200)

    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Erro'}, status=500)

# delete an agent
@require_http_methods
def del_agent(request, id):
    try:
        agent = get_object_or_404(Agent, pk=id)
        agent.delete()
        return JsonResponse({"message":f"Agent {id} has been removed from database"}, status=200)
    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Erro'}, status=500)
