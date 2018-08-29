import urllib.request
import json

bingMapsKey = 'YOUR_BING_API_KEY'
longitude1 = 30.490020
latitude1 = 59.945870

longitude2 = 30.469970
latitude2 = 59.881930

longitude2 = 59.881930
latitude2 = 30.469970


def countDistance(longitude1, latitude1, longitude2, latitude2):
    routeUrl = "http://dev.virtualearth.net/REST/V1/Routes/Driving?wp.0=" + str(latitude1) + "," + str(longitude1) + \
               "&wp.1=" + str(latitude2) + "," + str(longitude2) + "&key=" + bingMapsKey
    request = urllib.request.Request(routeUrl)

    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        error = e.read().decode(encoding="utf-8")
        result = json.loads(error)
        #print(str(result["statusCode"]) + " " + result["statusDescription"])
        itineraryItems = result["errorDetails"][0]
        return itineraryItems
    else:
        r = response.read().decode(encoding="utf-8")
        result = json.loads(r)
        #print(str(result["statusCode"]) + " " + result["statusDescription"])
        itineraryItems = result["resourceSets"][0]["resources"][0]["travelDistance"]
        return itineraryItems
        #for item in itineraryItems:
            #print(item["instruction"]["text"])

#countDistance(longitude1, latitude1, longitude2, latitude2)