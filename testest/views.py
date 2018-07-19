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
        section = '사료양1'

        return JsonResponse({
            'message': {
                'text': "강아지의 몸무게를 알려주세요!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

#강아지 몸무게 받음
    elif section == '사료양1' :

        global weight
        k = datacontent
        weight = re.findall("\d+", k)
        section = '사료양2'
        return JsonResponse({
            'message': {
                'text': "멍뭉이 나이는?!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

#강아지 나이 받음
    elif section == '사료양2' :
        global age
        global month
        k = datacontent
        if k.find("개월") > -1 or k.find("달") > -1 :
            month = re.findall("\d+", k)
            age = -1
        else:
            age = re.findall("\d+", k)
            month = -1

        section = '사료양3'
        return JsonResponse({
            'message': {
                'text': "멍뭉이의 예외사항 (임신, 비만, 해당없음)"
            },
            'keyboard': {
                'type': 'text'
            }
        })

# 특이 사항 따라 필요 사료양 계산 및 제공
    elif section == '사료양3' :
        if datacontent == '임신':
            food = (int(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })
        elif datacontent=='비만':
            food = (int(weight[0]) * 30 + 70) * 1.5 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })

        # 1살
        elif datacontent=='해당없음':
            if age[0] == 1 :
                food = (int(weight[0]) * 30 + 70) * 1.5 * 2 / 4.5
                return JsonResponse({
                    'message': {
                        'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!\n%d살은 하루 2~3회로 나눠주면 좋아요!" % (food, food / 78, age[0])
                    },
                    'keyboard': {
                        'type': 'text'
                    }
                })

            #성견
            elif age[0] > 1 or month[0] > 12 :
                food = (int(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                return JsonResponse({
                    'message': {
                        'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!\n%d살은 하루 2~3회로 나눠주면 좋아요!" % (food, food / 78, age[0])
                    },
                    'keyboard': {
                        'type': 'text'
                    }
                })

            #4개월 미만
            elif month[0] < 4 :
                food = (int(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                return JsonResponse({
                    'message': {
                        'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!\n%d개월은 하루 4~5회로 나눠주면 좋아요!" % (food, food / 78, month[0])
                    },
                    'keyboard': {
                        'type': 'text'
                    }
                })

            #4개월 ~ 12개월
            elif month[0] >= 4 and month <=12 :
                food = (int(weight[0]) * 30 + 70) * 1.5 * 2 / 4.5
                
                #4개월~9개월
                if month[0] < 9:
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!\n%d개월은 하루 3~4회로 나눠주면 좋아요!" % (food, food / 78, month[0])
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })
                
                #9개월 이상
                elif month[0] > 9 :
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!\n%d개월은 하루 2~3회로 나눠주면 좋아요!" % (food, food / 78, month[0])
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })

