from threading import Lock
from django.db import connections

from .logging_helper import Logger

logger = Logger(__name__)


class Singleton(type):
    """Singleton class based on singleton design pattern"""
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super(Singleton, cls).__call__(
                    *args, **kwargs
                )
        return cls._instances[cls]


def check_mysql_connection():
    """Check if a MySQL connection is available for read"""
    conn = connections["slave"]

    try:
        conn.ensure_connection()
        return True
    except Exception:
        return False

def convert_to_int_list(str_list):
    """Convert a comma-separated string into a list of integers."""
    return [int(item) for item in str_list.split(',')] if str_list else []

def createPaginationURL(request, page, total_page_count):
		"""Create URLs for pagination based on the current page and total page count."""
		if page == "":
			page = 1

		currentPage = int(page) if int(page) else 1
		
		if currentPage == 1:
			prevPage = None
		else:
			prevPage = f"{request.build_absolute_uri().split('page=')[0]}page={str(currentPage - 1)}"
		
		if currentPage < total_page_count:
			nextPage = f"{request.build_absolute_uri().split('page=')[0]}page={str(currentPage + 1)}"
		else:
			nextPage = None
		
		response = {
			"prev_page": prevPage,
			"current_page": currentPage,
			"next_page": nextPage,
		}
		return response