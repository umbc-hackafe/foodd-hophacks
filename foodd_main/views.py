from django import http

hosted_jquery = '<script src="//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>'

def home(request):
    return http.HttpResponse('Hello World!' + hosted_jquery)
