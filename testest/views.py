from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import re

section = '0'

def keyboard(request):

    return JsonResponse({
        "type": "text",
        
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
                'text': "강아지의 몸무게(kg)를 알려주세요!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

#강아지 몸무게
    elif section == '사료1' :
        global weight
        for x in datacontent:
            if is_digit(x):
                if datacontent.find("kg") != -1 or datacontent.find("KG") != -1 or datacontent.find("Kg") != -1 or datacontent.find("키로") != -1:

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
                elif is_digit(datacontent):
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

        return JsonResponse({
            'message': {
                'text': "입력이 옳지 않습니다;ㅁ;\n\n강아지의 몸무게를 알려주세요!"
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

        for x in datacontent:
            if x.isdigit():
                if datacontent.find("개월") != -1 or datacontent.find("달") != -1 :
                    x = re.findall("\d+", k)
                    age = -1
                    month = int(x[0])
                    section = '사료3'
                    return JsonResponse({
                        'message': {
                            'text': "멍뭉이의 예외사항 (임신, 비만, 해당없음)"
                        },
                        'keyboard': {
                            'type': 'text'
                        }
                    })
                elif datacontent.find("살") != -1 or datacontent.find("년") != -1 :
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

                elif is_digit(datacontent):
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


        return JsonResponse({
            'message': {
                'text': "입력이 옳지 않습니다;ㅁ;\n\n강아지의 나이를 알려주세요!"
            },
            'keyboard': {
                'type': 'text'
            }
        })

#예외사항 및 계산
    elif section == '사료3' :

        if datacontent.find("임신") != -1:
            food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
            section = '0'
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'buttons'
                }
            })
        elif datacontent.find("비만") != -1 or datacontent.find("돼지") != -1 or (datacontent.find("살") != -1 and datacontent.find("쪘") != -1):
            section = '0'
            food = (float(weight[0]) * 30 + 70) * 1.5 / 4.5
            return JsonResponse({
                'message': {
                    'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!"%(food,food/78)
                },
                'keyboard': {
                    'type': 'buttons'
                }
            })
        elif datacontent.find("없") != -1 :
            section = '0'
            #개월 수로 받았을 때
            if age == -1:
                #4개월 미만
                if month < 4 :
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n종이컵으로 약 %.1f 컵 정도예요!\n\n하루에 4~5번으로 나눠서 주는 걸 권장해요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'buttons'
                        }
                    })
                #4개월 ~ 9개월
                elif month >=4 and month <9:
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 2 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!\n\n하루에 3~4번으로 나눠서 주는 걸 권장해요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'buttons'
                        }
                    })

                #9개월 ~ 12개월
                elif month >=9 and month<12 :
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 2 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!\n\n하루에 2~3번으로 나눠서 주는 걸 권장해요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'buttons'
                        }
                    })

                #12개월 이상
                else :
                    food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                    return JsonResponse({
                        'message': {
                            'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!\n\n하루에 2~3번으로 나눠서 주는 걸 권장해요!" % (food, food / 78)
                        },
                        'keyboard': {
                            'type': 'buttons'
                        }
                    })

             #N살로 받았을 때
            else :
                food = (float(weight[0]) * 30 + 70) * 1.5 * 3 / 4.5
                return JsonResponse({
                    'message': {
                        'text': "%d g의 사료가 필요합니다! \n 종이컵으로 약 %.1f 컵 정도예요!\n\n하루에 2~3번으로 나눠서 주는 걸 권장해요!" % (food, food / 78)
                    },
                    'keyboard': {
                        'type': 'buttons'
                    }
                })

        else:
            return JsonResponse({
                'message': {
                    'text': "입력이 옳지 않습니다;ㅁ;\n\n강아지의 예외사항을 알려주세요 (임신, 비만, 해당없음)"
                },
                'keyboard': {
                    'type': 'text'
                }
            })

    else :
        return JsonResponse({
            'message': {
                'text': "입력이 옳지 않습니다;ㅁ;"
            },
            'keyboard': {
                'type': 'buttons'
            }
        })



def is_digit(str):
    try:
        tmp = float(str)
        return True
    except ValueError:
        return False
