from django.shortcuts import render

def infinite_grid_view(request):
    return render(request, 'grid/infinite_grid.html')
