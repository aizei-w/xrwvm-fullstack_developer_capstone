from __future__ import annotations

import json
from typing import Any

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import CarModel
from .populate import initiate
from .restapis import analyze_review_sentiments, get_request, post_review


def _request_data(request) -> dict[str, Any]:
    if request.body:
        try:
            return json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    return request.POST.dict()


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    data = _request_data(request)
    username = str(data.get("userName") or data.get("username") or "").strip()
    password = str(data.get("password") or "")
    if not username or not password:
        return JsonResponse({"status": "Error", "message": "Username and password are required."}, status=400)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"userName": username, "status": "Unauthenticated"}, status=401)
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated", "firstName": user.first_name, "lastName": user.last_name})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def logout_user(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": username, "status": "Logged out"})


@csrf_exempt
@require_http_methods(["POST"])
def registration(request):
    data = _request_data(request)
    username = str(data.get("userName") or data.get("username") or "").strip()
    password = str(data.get("password") or "")
    first_name = str(data.get("firstName") or data.get("first_name") or "").strip()
    last_name = str(data.get("lastName") or data.get("last_name") or "").strip()
    email = str(data.get("email") or "").strip()
    if not all([username, password, first_name, last_name, email]):
        return JsonResponse({"status": "Error", "message": "All five registration fields are required."}, status=400)
    if User.objects.filter(username__iexact=username).exists():
        return JsonResponse({"userName": username, "status": "Already Registered"}, status=409)
    user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    login(request, user)
    return JsonResponse({"userName": user.username, "status": "Authenticated", "firstName": user.first_name, "lastName": user.last_name}, status=201)


@require_http_methods(["GET"])
def get_dealerships(request, state: str | None = None):
    endpoint = "fetchDealers" if not state else f"fetchDealers/{state}"
    return JsonResponse({"status": 200, "dealers": get_request(endpoint) or []})


@require_http_methods(["GET"])
def get_dealer_details(request, dealer_id: int):
    dealer = get_request(f"fetchDealer/{dealer_id}") or []
    status = 200 if dealer else 404
    return JsonResponse({"status": status, "dealer": dealer}, status=status)


@require_http_methods(["GET"])
def get_dealer_reviews(request, dealer_id: int):
    reviews = get_request(f"fetchReviews/dealer/{dealer_id}") or []
    enriched = []
    for review in reviews:
        item = dict(review)
        item["sentiment"] = analyze_review_sentiments(str(item.get("review", ""))).get("sentiment", "neutral")
        enriched.append(item)
    return JsonResponse({"status": 200, "reviews": enriched})


@csrf_exempt
@require_http_methods(["POST"])
def add_review(request):
    data = _request_data(request)
    required = ["name", "dealership", "review", "purchase", "purchase_date", "car_make", "car_model", "car_year"]
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return JsonResponse({"status": 400, "message": f"Missing fields: {', '.join(missing)}"}, status=400)
    try:
        data["dealership"] = int(data["dealership"])
        data["car_year"] = int(data["car_year"])
    except (TypeError, ValueError):
        return JsonResponse({"status": 400, "message": "Dealer ID and car year must be numbers."}, status=400)
    return JsonResponse({"status": 200, "review": post_review(data)})


@require_http_methods(["GET"])
def get_cars(request):
    if not CarModel.objects.exists():
        initiate()
    cars = [{"CarMake": car.car_make.name, "CarModel": car.name, "CarType": car.type, "CarYear": car.year} for car in CarModel.objects.select_related("car_make").all()]
    return JsonResponse({"status": 200, "CarModels": cars})


@require_http_methods(["GET"])
def analyze_review(request, text: str):
    return JsonResponse({"text": text, **analyze_review_sentiments(text)})
