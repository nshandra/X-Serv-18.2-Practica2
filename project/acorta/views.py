from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
from acorta.models import ShrinkedURL
import re

# Create your views here.

def URLcomplete(url):
    if re.match(r'http(s)?://*', url):
        return url
    else:
        return ("http://" + url)

def makelist():
    mirrorslist = ""
    db = ShrinkedURL.objects.all()
    for entry in db:
        mirrorslist += ("Original: <a href=" + entry.resource + ">" +
                        entry.resource + "</a> => Mirror: <a href=" +
                        entry.mirror + ">" + entry.mirror + "</a></br>")
    return mirrorslist

def NotFound(request):
    return HttpResponseNotFound("<html><body><h1>404 Not Found</h1></body></html>")

@csrf_exempt
def Shrinker(request):
    if request.method == "GET":
        mirrorslist = makelist()
        print("mirrorslist: ", mirrorslist)
        OK = ("<html><head><meta charset='utf-8'><h1 align='center'>"
              "X-Serv-18.2-Practica2</h1></head><body>"
              "<form method='POST'><p align='center'>URL a acortar: "
              "<input type='text' name='URL' ></p></form>"
              "Previous URLs:<br>" + mirrorslist + "</body></html>")
        return HttpResponse(status=200, content=OK)
    elif request.method == "POST":
        if request.POST["URL"] == "":
            return HttpResponseRedirect('/')
        else:
            url = URLcomplete(request.POST["URL"])
            try:
                mirrorID = ShrinkedURL.objects.get(resource=url).mirror
            except ShrinkedURL.DoesNotExist:
                mirrorID = "/" + str(ShrinkedURL.objects.count()+1)
                ShrinkedURL(resource=url, mirror=mirrorID).save()
            mirror = "http://localhost:8000" + mirrorID
            htmlBody = ("<html><body>Url a acortar = <a href=" + url +
                        ">" + url + "</a><br>Url Acortada = <a href=" +
                        mirror + ">" + mirror + "</a></br></body></html>")
            return HttpResponse(status=200, content=htmlBody)
    else:
        NotFound(request)

def Redirect(request):
    try:
        RedirURL = ShrinkedURL.objects.get(mirror=request.path)
        print(RedirURL)
        return HttpResponseRedirect(RedirURL.resource)
    except ShrinkedURL.DoesNotExist as e:
        return HttpResponseNotFound("<html><body><h1>404 Not Found</h1></body></html>")
