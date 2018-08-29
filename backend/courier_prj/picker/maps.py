import urllib.request
import json

bingMapsKey = 'YOUR_BING_KEY'

def countDistanceFromGeo(longitude1, latitude1, longitude2, latitude2):
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
        #print(itineraryItems)
        return itineraryItems

def countDistanceFromAddresses(addressFrom, addressTo):
    longitude1, latitude1 = addressFrom.split(', ')
    longitude2, latitude2 = addressTo.split(', ')
    return countDistanceFromGeo(longitude1, latitude1, longitude2, latitude2)

#countDistanceFromAddresses('31.439970, 59.881930', '30.490020, 59.945870')
