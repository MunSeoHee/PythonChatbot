from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import re

section = '0'

def keyboard(request):

    return JsonResponse({
        "type": "buttons",
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

#강아지 몸무게
    elif section == '사료1' :

        global weight
        k = datacontent
        weight = re.findall("\d+.\d+|\d", k)
        section = '사료2'
        return JsonResponse({
            'message': {
                'text': "멍뭉이 나이는?!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

#강아지 나이
    elif section == '사료2' :
        global age
        global month
        k = datacontent

        if k.find("개월"):
            x = re.findall("\d+", k)
            age = -1
            month = int(x[0])
        else:
            x = re.findall("\d+", k)
            month = -1
            age = int(x[0])

        section = '사료3'
        return JsonResponse({
            'message': {
                'text': "멍뭉이의 예외사항 (임신, 비만, 해당없음)"
            },
            'keyboard': {
                'type': 'text'
            }
        })

#예외사항 및 계산
    elif section == '사료3' :
        if datacontent == '임신':
            food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })
        elif datacontent=='비만':
            food = (float(weight[0]) * 30 + 70) * 1.5 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'text'
                }
            })
        elif datacontent=='해당없음':
            #개월 수로 받았을 때
            if age == -1:
                #4개월 미만
                if month < 4 :
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })
                #4개월 ~ 9개월
                elif month >=4 and month <9:
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 2 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })

                #9개월 ~ 12개월
                elif month >=9 and month<12 :
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 2 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })

                #12개월 이상
                else :
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })

             #N살로 받았을 때
            else :
                food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                return JsonResponse({
                    'message': {
                        'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!" % (food, food / 78)
                    },
                    'keyboard': {
                        'type': 'text'
                    }
                })

    else :
        return JsonResponse({
            'message': {
                'text': "입력이 잘못되었습니다"
            },
            'keyboard': {
                'type': 'button'
            }
        })
