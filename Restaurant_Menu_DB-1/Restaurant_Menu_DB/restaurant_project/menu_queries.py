from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, Avg, Max, Min, F, Count
from restaurant_app.models import Restaurant, Menu, MenuVersion, MenuSection, MenuItem, DietaryRestriction, MenuItemDietaryRestriction, ProcessingLog
from django.db.models.functions import Coalesce
from decimal import Decimal

def get_restaurant_sections(restaurant_id):
    """
    Retrieves all menu sections for a specific restaurant, including version information.
    
    This function uses the Prefetch API to eagerly load the related data, which can improve performance
    when dealing with large amounts of data.
    
    Parameters:
    restaurant_id (int): The ID of the restaurant to retrieve the menu sections for.
    
    Returns:
    list: A list of dictionaries, where each dictionary represents the menu sections for a specific menu version.
    """
    try:
        # Get the restaurant with all related data preloaded
        restaurant = Restaurant.objects.prefetch_related(
            Prefetch(
                'menu_set',
                queryset=Menu.objects.prefetch_related(
                    Prefetch(
                        'menuversion_set',
                        queryset=MenuVersion.objects.prefetch_related(
                            'sections'
                        )
                    )
                )
            )
        ).get(id=restaurant_id)

        # Organize the data
        menu_sections = []
        for menu in restaurant.menu_set.all():
            for version in menu.menuversion_set.all():
                sections = version.sections.all()
                menu_sections.append({
                    'menu_name': menu.name,
                    'version_number': version.version_number,
                    'is_active': version.is_active,
                    'sections': list(sections)
                })

        return menu_sections
    except Restaurant.DoesNotExist:
        return None

def get_active_menu_sections(restaurant_id):
    """
    Retrieves only the sections from active menu versions for a specific restaurant.
    
    This function also uses the Prefetch API to eagerly load the related data, which can improve performance.
    
    Parameters:
    restaurant_id (int): The ID of the restaurant to retrieve the active menu sections for.
    
    Returns:
    list: A list of MenuSection objects, representing the active menu sections for the specified restaurant.
    """
    try:
        # Get the restaurant with only active versions
        restaurant = Restaurant.objects.prefetch_related(
            Prefetch(
                'menu_set',
                queryset=Menu.objects.prefetch_related(
                    Prefetch(
                        'menuversion_set',
                        queryset=MenuVersion.objects.filter(
                            is_active=True
                        ).prefetch_related('sections')
                    )
                )
            )
        ).get(id=restaurant_id)

        # Organize the data
        active_sections = []
        for menu in restaurant.menu_set.all():
            for version in menu.menuversion_set.all():
                sections = version.sections.all()
                active_sections.extend(sections)

        return active_sections
    except Restaurant.DoesNotExist:
        return None
    
def get_menu_versions(restaurant_id, menu_id):
    """
    Retrieves all MenuVersion objects for the specified Restaurant and Menu.

    This function allows you to fetch a list of all the menu versions associated with a particular
    restaurant and menu. This can be useful for scenarios where you need to access information about
    the different versions of a menu, such as the version number, creation date, and whether the version is
    currently active.

    Parameters:
    restaurant_id (int): The ID of the Restaurant to retrieve the menu versions for.
    menu_id (int): The ID of the Menu to retrieve the menu versions for.

    Returns:
    list: A list of dictionaries, where each dictionary represents the data for a single MenuVersion object.
    """
    try:
        # Fetch the Restaurant and Menu objects
        restaurant = Restaurant.objects.get(id=restaurant_id)
        menu = Menu.objects.get(id=menu_id, restaurant=restaurant)

        # Retrieve all the MenuVersion objects associated with the specified Menu
        menu_versions = MenuVersion.objects.filter(menu=menu)

        # Organize the data into a list of dictionaries
        version_data = [
            {
                'version_number': version.version_number,
            }
            for version in menu_versions
        ]

        return version_data
    except (Restaurant.DoesNotExist, Menu.DoesNotExist):
        # If the requested Restaurant or Menu does not exist, return None
        return None
    
def get_menu_items_by_version(restaurant_id, menu_id, version_number=None):
    """
    Retrieves menu items organized by sections for a specific restaurant, menu, and optionally a version.
    If no version is specified, returns the active version.
    
    Args:
        restaurant_id (int): Restaurant ID
        menu_id (int): Menu ID
        version_number (int, optional): Specific version number. Defaults to None (active version).
    
    Returns:
        dict: Hierarchical structure of menu sections and items
    """
    # Get the restaurant and menu
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    menu = get_object_or_404(Menu, id=menu_id, restaurant=restaurant)
    
    # Get the appropriate version
    if version_number:
        menu_version = get_object_or_404(MenuVersion, 
                                       menu=menu, 
                                       version_number=version_number)
    else:
        menu_version = get_object_or_404(MenuVersion, 
                                       menu=menu, 
                                       is_active=True)
    
    # Get sections with related items
    sections = MenuSection.objects.filter(
        menu_version=menu_version
    ).prefetch_related('items')
    
    # Organize the data
    menu_data = {
        'restaurant_name': restaurant.name,
        'menu_name': menu.name,
        'version': menu_version.version_number,
        'sections': []
    }
    
    for section in sections:
        section_data = {
            'section_name': section.name,
            'items': [
                {
                    'name': item.name,
                    'description': item.description,
                    'price': str(item.price)
                } for item in section.items.all()
            ]
        }
        menu_data['sections'].append(section_data)
    
    return menu_data

def get_menu_items_by_dietary_restrictions(restaurant_id, menu_id, version_number=None, 
                                         dietary_restrictions=None):
    """
    Retrieves menu items filtered by dietary restrictions.
    
    Args:
        restaurant_id (int): Restaurant ID
        menu_id (int): Menu ID
        version_number (int, optional): Specific version number
        dietary_restrictions (list): List of dietary restriction names
    
    Returns:
        dict: Filtered menu items organized by sections
    """
    # Get the base menu structure
    menu_data = get_menu_items_by_version(restaurant_id, menu_id, version_number)
    
    # If no dietary restrictions specified, return all items
    if not dietary_restrictions:
        return menu_data
    
    # Filter items by dietary restrictions
    menu_version = get_object_or_404(
        MenuVersion,
        menu_id=menu_id,
        version_number=version_number if version_number else F('is_active')
    )
    
    filtered_items = MenuItem.objects.filter(
        section__menu_version=menu_version,
        menuitemdietaryrestriction__restriction__name__in=dietary_restrictions
    ).distinct()
    
    # Update menu_data to include only filtered items
    for section in menu_data['sections']:
        section['items'] = [
            item for item in section['items']
            if any(filtered_item.name == item['name'] 
                  for filtered_item in filtered_items)
        ]
    
    return menu_data

def get_restaurant_price_analytics(n=3):
    """
    Analyzes restaurant prices and returns both highest and lowest average price restaurants.
    
    For both groups (top N and bottom N by average price), provides:
    1. Restaurant details and average prices
    2. Most and least expensive dishes for each restaurant
    3. Total number of items on their menu
    
    Args:
        n (int): Number of restaurants to return for each group (default 3)
        
    Returns:
        dict: Complete analysis including both expensive and affordable restaurants
    """
    try:
        # First get all restaurants with their average prices
        restaurants_with_stats = Restaurant.objects.annotate(
            total_items=Count('menu__menuversion__sections__items', distinct=True),
            avg_price=Coalesce(
                Avg('menu__menuversion__sections__items__price'),
                Decimal('0.00')
            )
        ).filter(
            total_items__gt=0  # Only include restaurants that have menu items
        )
        
        # Get top N most expensive restaurants
        most_expensive = restaurants_with_stats.order_by('-avg_price')[:n]
        
        # Get top N least expensive restaurants
        least_expensive = restaurants_with_stats.order_by('avg_price')[:n]
        
        def get_restaurant_details(restaurant_queryset, category_name):
            """
            Helper function to process restaurant details and their price extremes.
            """
            detailed_results = []
            
            for restaurant in restaurant_queryset:
                # Get all items for this restaurant
                restaurant_items = MenuItem.objects.filter(
                    section__menu_version__menu__restaurant=restaurant
                ).select_related(
                    'section',
                    'section__menu_version',
                    'section__menu_version__menu'
                )
                
                # Calculate price extremes for this restaurant
                price_extremes = restaurant_items.aggregate(
                    max_price=Max('price'),
                    min_price=Min('price')
                )
                
                # Get the specific items with extreme prices
                most_expensive_item = restaurant_items.filter(
                    price=price_extremes['max_price']
                ).first()
                
                least_expensive_item = restaurant_items.filter(
                    price=price_extremes['min_price']
                ).first()
                
                # Compile restaurant data
                restaurant_data = {
                    'restaurant_name': restaurant.name,
                    'average_price': float(restaurant.avg_price),
                    'total_items': restaurant.total_items,
                    'address': restaurant.address or 'Address not available',
                    'price_extremes': {
                        'most_expensive': {
                            'name': most_expensive_item.name,
                            'price': float(most_expensive_item.price),
                            'section': most_expensive_item.section.name,
                            'menu': most_expensive_item.section.menu_version.menu.name
                        },
                        'least_expensive': {
                            'name': least_expensive_item.name,
                            'price': float(least_expensive_item.price),
                            'section': least_expensive_item.section.name,
                            'menu': least_expensive_item.section.menu_version.menu.name
                        }
                    }
                }
                detailed_results.append(restaurant_data)
            
            return {
                f"{category_name}_restaurants": detailed_results
            }
        
        # Process both groups of restaurants
        high_price_data = get_restaurant_details(most_expensive, "highest_average")
        low_price_data = get_restaurant_details(least_expensive, "lowest_average")
        
        # Combine the results
        return {
            **high_price_data,
            **low_price_data,
        }

    except Exception as e:
        print(f"Error in get_restaurant_price_analytics: {str(e)}")
        return None

def get_specific_restaurant_analytics(restaurant_id):
    """
    Gets detailed price analytics for a specific restaurant.
    
    Returns complete price analysis including:
    1. Overall average price
    2. Total number of items
    3. Most and least expensive dishes with their details
    """
    try:
        restaurant = Restaurant.objects.annotate(
            total_items=Count('menu__menuversion__sections__items', distinct=True),
            avg_price=Coalesce(
                Avg('menu__menuversion__sections__items__price'),
                Decimal('0.00')
            )
        ).get(id=restaurant_id)

        items = MenuItem.objects.filter(
            section__menu_version__menu__restaurant_id=restaurant_id
        ).select_related(
            'section',
            'section__menu_version',
            'section__menu_version__menu'
        )

        price_extremes = items.aggregate(
            max_price=Max('price'),
            min_price=Min('price')
        )

        most_expensive = items.filter(
            price=price_extremes['max_price']
        ).first()

        least_expensive = items.filter(
            price=price_extremes['min_price']
        ).first()

        return {
            'restaurant_name': restaurant.name,
            'average_price': float(restaurant.avg_price),
            'total_items': restaurant.total_items,
            'price_extremes': {
                'most_expensive': {
                    'name': most_expensive.name,
                    'price': float(most_expensive.price),
                    'section': most_expensive.section.name,
                    'menu': most_expensive.section.menu_version.menu.name
                },
                'least_expensive': {
                    'name': least_expensive.name,
                    'price': float(least_expensive.price),
                    'section': least_expensive.section.name,
                    'menu': least_expensive.section.menu_version.menu.name
                }
            }
        }

    except Exception as e:
        print(f"Error in get_specific_restaurant_analytics: {str(e)}")
        return None