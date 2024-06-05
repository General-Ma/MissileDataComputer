from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods, require_GET, require_POST, require_safe
from django.http import HttpResponse, JsonResponse
from .models import Agent, LocationRecord
import json
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.middleware.csrf import get_token as get_csrf_token

# index as the entry url
def index(request):
    csrf_token = get_csrf_token(request)
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
        agent_data = {key: data.get(key) for key in ['model_type', 'name', 'owner', 'hostility', 'stationary'] if data.get(key) is not None}
        if agent_data['model_type'] is None:
            return JsonResponse({'error': 'model_type must be not be empty'}, status=400)
            
        #create the object
        try:
            new_agent = Agent.objects.create(**agent_data)
        except ValueError:
            return JsonResponse({'error': 'Invalid Field'}, status=400)

        return JsonResponse({'message': 'New Agent Created.', 'id':new_agent.id }, status=201)

    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Error'}, status=500)

# get an agent's info
@csrf_exempt
@require_GET
def get_agent(request, id):
    try:
        try:
            # get_object_or_404 is not used, so the error handling logic appears more organised
            agent = Agent.objects.get(pk=id)
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Item Not Found'}, status=404)
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
        return JsonResponse({'error': 'An Unknown Error'}, status=500)

# get all agents' ids
@require_GET
def get_all_agents(request):
    try:
        agents = Agent.objects.values_list('id', flat=True)
        return JsonResponse({"agents":list(agents)}, status=200)

    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Error'}, status=500)

# delete an agent
@require_http_methods(['DELETE'])
def del_agent(request, id):
    try:
        try:
            agent = Agent.objects.get(pk=id)
            agent.delete()
        except Agent.DoesNotExist:
            # status 200 is responded on purpose, as a security feature. Maybe in future, we should add authorisation and authentication here.
            print(f"Deletion Attempted, but Item Not Found, {id}")
        return JsonResponse({"message":f"Agent {id} has been removed from database"}, status=200)
    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Error'}, status=500)

# update an agent
@require_http_methods(['PATCH', 'PUT'])
def patch_agent(request, id):
    try:
        try:
            data = json.loads(request.body.decode('utf-8'))
            agent = Agent.objects.get(pk=id)
            new_data = {key: data.get(key) for key in ['model_type', 'name', 'owner', 'hostility', 'stationary'] if data.get(key) is not None}
            for key in new_data.keys():
                # note key here are str, which cannot be used as attribute directly
                setattr(agent, key, new_data[key])
            agent.save()
            print(new_data)

        except json.JSONDecodeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Agent.DoesNotExist:
            return JsonResponse({'error': 'Item Not Found'}, status=404)

        return HttpResponse(status=204)
    except Exception as e :
        print(f'Unexpected error:{e}')
        return JsonResponse({'error': 'An Unknown Error'}, status=500)
