import logging

def get_page(self):
    """
    A function which will be monkeypatched onto the request to get the current
    integer representing the current page.
    """
    try:
        page = int(self.GET['page'])
        return page if page > 0 else 1
    except (KeyError, ValueError, TypeError):
        return 1


class PaginationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """
    def process_request(self, request):
        request.__class__.page = property(get_page)
