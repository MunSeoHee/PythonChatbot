from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import re

section = '0'

def keyboard(request):

    return JsonResponse({
        "type": "buttons","text"
        "buttons": ["강아지 사료양"]
    })

@csrf_exempt
def answer(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']

    if datacontent == "강아지 사료양":
        global section
        section = '사료1'

        return JsonResponse({
            'message': {
                'text': "강아지의 몸무게를 알려주세요!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

    elif section == '사료1' :

        global weight
        k = datacontent
        weight = re.findall("\.\d+", k)
        section = '사료2'
        return JsonResponse({
            'message': {
                'text': "멍뭉이 나이는?! %f"%(weight[0])
            },
            'keyboard': {
                'type': 'text'
            }
        })

    elif section == '사료2' :
        global age
        k = datacontent
        age = re.findall("\d+", k)
        section = '사료3'
        return JsonResponse({
            'message': {
                'text': "멍뭉이의 예외사항 (임신, 비만, 해당없음)"
            },
            'keyboard': {
                'type': 'text'
            }
        })

    elif section == '사료3' :
        if datacontent == '임신':
            food = ((weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })
        elif datacontent=='비만':
            food = ((weight[0]) * 30 + 70) * 1.5 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })
        elif datacontent=='해당없음':
            food = ((weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })
