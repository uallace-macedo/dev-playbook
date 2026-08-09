from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = 'customer'
    RESTAURANT_OWNER = 'restaurant_owner'
