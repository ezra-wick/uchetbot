from aiogram.utils.helper import Helper, HelperMode, ListItem, Item
from aiogram.dispatcher.filters.state import State, StatesGroup

class ProductState(StatesGroup):
    PRODUCT_NAME = State()
    PRODUCT_QUANTITY = State()
    PRODUCT_DIMENSION = State()
    PRODUCT_PRICE = State()
    PRODUCT_COST_PRICE = State()


class WorkerState(StatesGroup):
    WORKER_NAME = State()
    WORKER_PHONE = State()
    WORKER_ROLE = State()
    WORKER_TG_ID = State()
    WORKER_SALARY = State()


class DeliveryState(StatesGroup):
    DELIVERY_NAME = State()
    DELIVERY_COST_PRICE = State()
    DELIVERY_QUANTITY = State()

