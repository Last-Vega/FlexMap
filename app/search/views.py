from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.conf import settings
from django.views.decorators.http import require_http_methods
from . import forms
from src import spots
import json
# Create your views here.


def return_route(request):
    # if request.method == "POST":
         form = forms.User_Inputs(request.POST)
         if form.is_valid():
            import googlemaps
            # formの入力を取得
            department = form.data['department']
            destination = form.data['destination']
            priority = form.data['priority']
            staying_time = form.data['staying_time']

            # department とdestinationの座標を取得
            gmaps = googlemaps.Client(key=settings.GOOGLEMAPS_API_KEY)
            dep_coordinate = gmaps.geocode(address=department)[0]["geometry"]["location"]
            des_coordinate = gmaps.geocode(address=destination)[0]["geometry"]["location"]
            # データベースからすべてのレンタルサービスのステーションの座標を取得する。
            list_stations = []
            for spot in spots.spots:
                address = spot['candidates'][0]['formatted_address']
                x = spot['candidates'][0]['geometry']['location']['lat']
                y = spot['candidates'][0]['geometry']['location']['lng']
                station = {
                    "address" : address,
                    "x": x,
                    "y": y
                }
                list_stations.append(station)

            # 全てのステーションの座標についてfor文でブンブン回す
            list_stations_ok = []
            for station in list_stations:
                # has_rental_spotを実行して適合するステーションの座標or住所を配列を代入
                list_stations_ok.append(has_rental_spot(dep_coordinate["lat"],dep_coordinate["lng"],des_coordinate["lat"],des_coordinate["lng"], station))

            list_stations_ok = list(filter(None, list_stations_ok))
            # route_sortを実行
            del list_stations_ok[3:]

            print(len(list_stations_ok))
            #
            route_list = route_sort(department, destination, list_stations_ok, staying_time)
            params = {
                "route_list" : route_list
            }
            print(len(route_list))
            return route_list
    # else:
    #     form = forms.User_Inputs()
    #     params = {
    #         "form":form
    #     }
    #     return render(request, 'test_route_return.html',params)


def index(request):
    result = route_search("東京駅", "新宿駅", "driving")
    params = {
        'word': 'hello world',
        'result': result
    }
    return render(request, 'index.html', params)


def user_input(request):
    distance = ""
    duration = ""
    dummyResult = []

    if request.method == 'POST':
        form = forms.User_Inputs(request.POST)
        if form.is_valid(): # formの値が正当な時(バリデーションチェックを走らせる)
            department = form.data['department']
            destination = form.data['destination']
            # travel_mode = form.data['travel_mode']
            result = route_search(department, destination, "driving")
            dummyResult = return_route(request)
            print(len(dummyResult))
            distance = result['routes'][0]['legs'][0]['distance']['text']
            duration = result['routes'][0]['legs'][0]['duration']['text']


    elif request.method == 'GET':
        form = forms.User_Inputs()
        department = ""
        destination = ""
        result = []
        dummyResult = []

    params = {
        'form':form,
        'department':department,
        'destination':destination,
        # 'travel_mode':travel_mode,
        'result':result,
        'distance':distance,
        'duration':duration,
        'dummy':dummyResult,
    }

    return render(request, 'index.html', params)


def route_search(department, destination, travel_mode):
    # import googlemaps
    # gmaps = googlemaps.Client(key=settings.GOOGLEMAPS_API_KEY)

    # directions_result = gmaps.directions(department,
    #                                      destination,
    #                                      mode=travel_mode)
    import requests
    API_KEY = settings.GOOGLEMAPS_API_KEY
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin={0}&destination={1}&mode={2}&key={3}'.format(department, destination, travel_mode, API_KEY)
    result = requests.get(url)
    directions_result = result.json()
    # print(directions_result)
    for step in directions_result['routes'][0]['legs'][0]['steps']:
        step['travelMode'] = step['travel_mode']
        step = step.pop('travel_mode')

    return directions_result


def objective(cost, minutes, lambda_cost=1, lambda_minutes=1):
    return (cost*lambda_cost) + (minutes*lambda_minutes)


def calculate_cost(department, destination, staying_time):
    import googlemaps
    from datetime import datetime
    import json
    # 初期設定
    fee_start = 100  # dbから取得
    fee = 150  # dbから取得
    gmaps = googlemaps.Client(key=settings.GOOGLEMAPS_API_KEY)
    now = datetime.now()

    # distance_matrix apiで距離を取得
    distance_result = gmaps.distance_matrix(department,
                                            destination,
                                            mode="walking",
                                            departure_time=now)
    # jsonから距離を取得
    distance_result = distance_result["rows"][0]["elements"][0]["distance"]["value"]
    # kmに変換
    distance_result = distance_result/1000
    # 乗り物のスピード
    viechle_speed = 15  # dbから取得
    # 移動時間を計算
    distance_result = distance_result / viechle_speed
    minutes = distance_result
    # コスト計算
    distance_result = fee_start + (distance_result * 2 + int(staying_time)) * fee
    return_list = []
    return_list.append(distance_result)
    return_list.append(minutes)
    return return_list
# @require_http_methods(['POST'])


def has_rental_spot(departureX, departureY, destinationX, destinationY, rental_spot):
    # Xはlatitude, Yはlongitude
    coreX = (departureX + destinationX)/2
    coreY = (departureY + destinationY)/2
    radius = (departureX-coreX)**2 + (departureY-coreY)**2

    address = rental_spot["address"]
    rental_spotX = rental_spot["x"]
    rental_spotY = rental_spot["y"]
    distance = (rental_spotX-coreX)**2 + (rental_spotY-coreY)**2

    if distance <= radius:
        params = {
            'address': address,
            'x': rental_spotX,
            'y': rental_spotY
        }
        return params
    else:
        return None


def route_sort(department, destination, waypoint, staying_time=0):
    # dep_to_desでのtravelmodeでgoogle apiを叩いてreturn
    route_dep_to_des_driving = route_search(department, destination, "driving")
    route_dep_to_des_bicycling = route_search(department, destination, "bicycling")
    route_dep_to_des_walking = route_search(department, destination, "walking")

    # 移動時間と値段を取得
    # dep_to_desのコスト
    minutes = route_dep_to_des_driving['routes'][0]['legs'][0]['duration']['value'] / 60
    cost_dep_to_des_driving = objective(cost=0, minutes=minutes)
    minutes = route_dep_to_des_bicycling['routes'][0]['legs'][0]['duration']['value'] / 60
    cost_dep_to_des_bicycling = objective(cost=0, minutes=minutes)
    minutes = route_dep_to_des_walking['routes'][0]['legs'][0]['duration']['value'] / 60
    cost_dep_to_des_walking = objective(cost=0, minutes=minutes)

    dic = {cost_dep_to_des_driving: [route_dep_to_des_driving],
           cost_dep_to_des_bicycling: [route_dep_to_des_bicycling],
           cost_dep_to_des_walking: [route_dep_to_des_walking]}

    for station in waypoint:
        # dep_to_wayでのtravelmodeでのgoogle apiを叩く
        route_dep_to_way_walking = route_search(department, station["address"], "walking")
        # way_to_desのgoogle api
        route_way_to_des_walking = route_search(station["address"], destination, "walking")

        # dep_to_wayのwalkingのコスト
        minutes = route_dep_to_way_walking['routes'][0]['legs'][0]['duration']['value'] / 60
        # way_to_desのrental serviceでのコスト
        cost_list = calculate_cost(station["address"], destination, staying_time)
        #dep_to_way, way_to_desitinationのコスト
        cost_dep_to_des_rental = objective(cost=cost_list[0], minutes=(cost_list[1]+minutes))

        dic[cost_dep_to_des_rental] = [route_dep_to_way_walking, route_way_to_des_walking]

    # ソート
    dic = sorted(dic.items())

    return_list = []
    for key, value in dic:
        return_list.append(value)

    # a = len(return_list)
    #raise ValueError("stopped!")
    print("sort:"+str(len(return_list)))
    # return_json = json.dumps(return_list, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
    print(return_json[0])
    print(return_json[1])
    print("json:"+str(len(return_json)))
    return return_json
