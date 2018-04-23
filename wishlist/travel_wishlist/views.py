from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, Place_to_visit_form

# Create your views here.

def place_list(request):

    """ If this is a POST request, the user clicked the Add button
    in the form.  check if the new place is valid, if so, save a
    new Place to the database, and redirect to this same page.

    If not a POST route, or Place is not valid, display a page with
    a list of places and a form to add a new place.
    """

    if request.method == 'POST':
        place_form = NewPlaceForm(request.POST)
        place = place_form.save(commit = False)  #create a new Place object from the form
        if place_form.is_valid():  #Checks for DB constraints violated
            place.save()     #Saves the place to the database
            return redirect('place_list')  #Redirect to a GET request for this same route

    #If not a POST, or the form is not valid, display
    # a page with a list of places and a form to add a new place IE wishlist.html.
    places = Place.objects.filter(visited=False).order_by('name')
    place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', {'places' : places, 'new_place_form': place_form })

# if place is marked as visited, take user to
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_is_visited(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        place.visited = True
        place.save()

    return redirect('place_list')

def place_to_visit(request, pk):
    place = get_object_or_404(Place, pk = pk)
    if not place.visited:
        form = Place_to_visit_form(instance=place)
        if request.method == "POST":
            form = Place_to_visit_form(request.POST, instance=place)
            if form.is_valid():
                place = form.save()
                place.visited = True
                place.save()

        return render(request, 'travel_wishlist/place_to_visit.html', {'place': place, 'form': form})
    return render(request, 'travel_wishlist/place_to_visit.html', {'place': place})
