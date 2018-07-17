from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

global section = '0'

def keyboard(request):

    return JsonResponse({
        'message':{
            'text' : "방가방가"
        },
        'keyboard': {
            'type': 'text'
        }
    })

@csrf_exempt
def answer(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']

    if datacontent == "강아지 사료양":
        today = "오늘 급식"
        section = '1'

        return JsonResponse({
            'message': {
                'text': "강아지의 몸무게를 알려주세요!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

    elif section == '1' :
        return JsonResponse({
            'message': {
                'text': "멍뭉이 나이는?!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

