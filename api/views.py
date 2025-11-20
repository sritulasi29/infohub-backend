import requests
from django.http import JsonResponse
import random

# ----------------------------
# WEATHER VIEW
# ----------------------------
def get_weather(request):
    city = request.GET.get("city")

    if not city:
        return JsonResponse({"error": "City name required"}, status=400)

    try:
        # ---------------------------------------------------------
        # STEP 1: Convert City → Latitude & Longitude
        # ---------------------------------------------------------
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_res = requests.get(geo_url).json()

        if "results" not in geo_res or len(geo_res["results"]) == 0:
            return JsonResponse({"error": "City not found"}, status=404)

        lat = geo_res["results"][0]["latitude"]
        lon = geo_res["results"][0]["longitude"]
        resolved_city = geo_res["results"][0]["name"]

        # ---------------------------------------------------------
        # STEP 2: Fetch actual weather (no API key needed)
        # ---------------------------------------------------------
        weather_url = (
            "https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            "&current=temperature_2m,windspeed_10m,winddirection_10m,weathercode,is_day"
        )

        weather_res = requests.get(weather_url).json()

        if "current" not in weather_res:
            return JsonResponse({"error": "Weather data unavailable"}, status=500)

        current = weather_res["current"]

        # ---------------------------------------------------------
        # STEP 3: Prepare response
        # ---------------------------------------------------------
        data = {
            "city": resolved_city,
            "temperature": current["temperature_2m"],
            "windspeed": current["windspeed_10m"],
            "winddirection": current["winddirection_10m"],
            "weathercode": current["weathercode"],
            "is_day": current["is_day"],  # ⭐ VERY IMPORTANT (sun/moon)
        }

        return JsonResponse(data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ----------------------------
# CURRENCY CONVERTER VIEW
# ----------------------------
def currency_convert(request):
    from_curr = request.GET.get("from")
    to_curr = request.GET.get("to")
    amount = request.GET.get("amount")

    if not from_curr or not to_curr or not amount:
        return JsonResponse({"error": "Missing parameters"}, status=400)

    url = f"https://api.exchangerate-api.com/v4/latest/{from_curr.upper()}"

    try:
        res = requests.get(url).json()
        rate = res["rates"].get(to_curr.upper())

        if not rate:
            return JsonResponse({"error": "Invalid currency"}, status=400)

        converted = float(amount) * rate

        return JsonResponse({
            "from": from_curr,
            "to": to_curr,
            "amount": amount,
            "converted_amount": converted
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ----------------------------
# RANDOM QUOTE VIEW (Dynamic)
# ----------------------------
def get_quotes(request):
    try:
        url = "https://zenquotes.io/api/random"
        response = requests.get(url)

        if response.status_code != 200:
            return JsonResponse({"error": "API response error"}, status=500)

        data = response.json()   # returns list
        quote_item = data[0]

        return JsonResponse({
            "quote": quote_item["q"],
            "author": quote_item["a"]
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)