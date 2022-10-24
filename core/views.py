from django.shortcuts import render



# Error Pages
def server_error(request):
    print("ERORR 500")
    return render(request, '500.html', status=500)

def not_found(request, exception):
    print("ERORR 404")
    return render(request, '404.html', status=404)

def permission_denied(request, exception):
    return render(request, '403.html', status=403)

def bad_request(request, exception):
    print("ERORR 400")
    return render(request, '400.html', status=400)