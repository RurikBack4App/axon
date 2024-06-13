from django.shortcuts import render, redirect

def redirect_to_swagger(request):
    # Option 1: Redirect immediately
    return redirect('/swagger/')

    # Option 2: Render the template and redirect after a delay
    # return render(request, 'redirect.html')