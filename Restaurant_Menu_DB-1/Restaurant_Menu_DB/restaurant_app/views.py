from django.http import JsonResponse
from .services.menu_queries import get_menu_items_by_version, get_menu_items_by_dietary_restrictions, get_restaurant_sections, get_active_menu_sections, get_menu_versions, get_restaurant_price_analytics, get_specific_restaurant_analytics
from rest_framework import viewsets
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from .models import Restaurant, Menu, MenuSection, MenuItem, DietaryRestriction, MenuVersion
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    MenuSectionSerializer,
    MenuItemSerializer,
    DietaryRestrictionSerializer
)

# ViewSet for Restaurant
class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Restaurant objects.
    
    This ViewSet provides the following actions:
    - List: GET /restaurants/
    - Create: POST /restaurants/
    - Retrieve: GET /restaurants/{id}/
    - Update: PUT/PATCH /restaurants/{id}/
    - Delete: DELETE /restaurants/{id}/
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

# ViewSet for Menu
class MenuViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Menu objects.
    
    This ViewSet provides the following actions:
    - List: GET /menus/
    - Create: POST /menus/
    - Retrieve: GET /menus/{id}/
    - Update: PUT/PATCH /menus/{id}/
    - Delete: DELETE /menus/{id}/
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

# ViewSet for MenuSection
class MenuSectionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on MenuSection objects.
    
    This ViewSet provides the following actions:
    - List: GET /menu-sections/
    - Create: POST /menu-sections/
    - Retrieve: GET /menu-sections/{id}/
    - Update: PUT/PATCH /menu-sections/{id}/
    - Delete: DELETE /menu-sections/{id}/
    """
    queryset = MenuSection.objects.all()
    serializer_class = MenuSectionSerializer

# ViewSet for MenuItem
class MenuItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on MenuItem objects.
    
    This ViewSet provides the following actions:
    - List: GET /menu-items/
    - Create: POST /menu-items/
    - Retrieve: GET /menu-items/{id}/
    - Update: PUT/PATCH /menu-items/{id}/
    - Delete: DELETE /menu-items/{id}/
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# ViewSet for DietaryRestriction
class DietaryRestrictionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on DietaryRestriction objects.
    
    This ViewSet provides the following actions:
    - List: GET /dietary-restrictions/
    - Create: POST /dietary-restrictions/
    - Retrieve: GET /dietary-restrictions/{id}/
    - Update: PUT/PATCH /dietary-restrictions/{id}/
    - Delete: DELETE /dietary-restrictions/{id}/
    """
    queryset = DietaryRestriction.objects.all()
    serializer_class = DietaryRestrictionSerializer

def restaurant_sections_view(request, restaurant_id):
    """
    View to display all sections for a restaurant.
    
    This view retrieves all the menu sections for the specified restaurant, including information about the
    menu versions and which sections belong to which versions.
    
    Parameters:
    request (django.http.HttpRequest): The incoming HTTP request.
    restaurant_id (int): The ID of the restaurant to retrieve the menu sections for.
    
    Returns:
    django.http.JsonResponse: A JSON response containing the menu sections for the specified restaurant.
    """
    all_sections = get_restaurant_sections(restaurant_id)
    if all_sections is None:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)

    return JsonResponse({
        'sections': [
            {
                'menu_name': section_data['menu_name'],
                'version': section_data['version_number'],
                'is_active': section_data['is_active'],
                'sections': [
                    {'name': section.name} for section in section_data['sections']
                ]
            }
            for section_data in all_sections
        ]
    })

def active_sections_view(request, restaurant_id):
    """
    View to display only active sections for a restaurant.
    
    This view retrieves only the sections from the active menu versions for the specified restaurant.
    
    Parameters:
    request (django.http.HttpRequest): The incoming HTTP request.
    restaurant_id (int): The ID of the restaurant to retrieve the active menu sections for.
    
    Returns:
    django.http.JsonResponse: A JSON response containing the active menu sections for the specified restaurant.
    """
    active_sections = get_active_menu_sections(restaurant_id)
    if active_sections is None:
        return JsonResponse({'error': 'Restaurant not found'}, status=404)

    return JsonResponse({
        'sections': [
            {'name': section.name}
            for section in active_sections
        ]
    })
    
def get_menu_version_view(request, restaurant_id, menu_id):
    """
    Retrieves all MenuVersion objects for the specified Restaurant and Menu.

    This view function allows the user to fetch a list of all the menu versions associated with a particular
    restaurant and menu. This can be useful for scenarios where the user needs to access information about
    the different versions of a menu, such as the version number, creation date, and whether the version is
    currently active.

    Parameters:
    request (django.http.HttpRequest): The incoming HTTP request.
    restaurant_id (int): The ID of the Restaurant to retrieve the menu versions for.
    menu_id (int): The ID of the Menu to retrieve the menu versions for.

    Returns:
    django.http.JsonResponse: A JSON response containing a list of MenuVersion objects.
    """
    print("restaurant_id: ", restaurant_id)
    print("menu_id: ", menu_id)
    menu_versions = get_menu_versions(restaurant_id, menu_id)

    if menu_versions is None:
        # If the requested Restaurant or Menu does not exist, return an error response
        return JsonResponse({'error': 'Restaurant or Menu not found'}, status=404)

    # Return the menu version data as a JSON response
    return JsonResponse({'versions': menu_versions})

@require_http_methods(["GET"])
def menu_items_view(request, restaurant_id, menu_id):
    """
    Retrieves menu items organized by sections. Optionally filters by version.
    
    URL: /api/restaurants/<restaurant_id>/menus/<menu_id>/items/
    Optional query params:
    - version_number: Specific version to retrieve (defaults to active version)
    """
    try:
        version_number = request.GET.get('version_number')
        if version_number:
            version_number = int(version_number)
        
        menu_data = get_menu_items_by_version(
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            version_number=version_number
        )
        
        return JsonResponse({
            'status': 'success',
            'data': menu_data
        })
    
    except ValidationError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to retrieve menu items'
        }, status=500)

@require_http_methods(["GET"])
def menu_items_dietary_view(request, restaurant_id, menu_id):
    """
    Retrieves menu items filtered by dietary restrictions.
    
    URL: /api/restaurants/<restaurant_id>/menus/<menu_id>/dietary-items/
    Required query params:
    - restrictions: Comma-separated list of dietary restriction names
    Optional query params:
    - version_number: Specific version to retrieve
    """
    try:
        restrictions_param = request.GET.get('restrictions', '')
        dietary_restrictions = [r.strip() for r in restrictions_param.split(',') if r.strip()]
        
        version_number = request.GET.get('version_number')
        if version_number:
            version_number = int(version_number)
        
        menu_data = get_menu_items_by_dietary_restrictions(
            restaurant_id=restaurant_id,
            menu_id=menu_id,
            version_number=version_number,
            dietary_restrictions=dietary_restrictions
        )
        
        return JsonResponse({
            'status': 'success',
            'data': menu_data
        })
    
    except ValidationError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': 'Failed to retrieve filtered menu items'
        }, status=500)

@require_http_methods(["GET"])
def restaurant_analytics_view(request):
    """
    View for retrieving price analytics across all restaurants.
    
    Optional query params:
    - n: Number of restaurants to return in each group (default 3)
    """
    try:
        n = int(request.GET.get('n', 3))
        if n < 1:
            return JsonResponse({
                'status': 'error',
                'message': 'n must be a positive integer'
            }, status=400)

        analytics = get_restaurant_price_analytics(n=n)
        
        if analytics is None:
            return JsonResponse({
                'status': 'error',
                'message': 'Failed to retrieve analytics'
            }, status=500)

        return JsonResponse({
            'status': 'success',
            'data': analytics
        })
        
    except ValueError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid n parameter'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'An unexpected error occurred: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def specific_restaurant_analytics_view(request, restaurant_id):
    """
    View for retrieving detailed price analytics for a specific restaurant.
    """
    try:
        analytics = get_specific_restaurant_analytics(restaurant_id)
        return JsonResponse({
            'status': 'success',
            'data': analytics
        })
    except Restaurant.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Restaurant not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

