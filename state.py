from aiogram.fsm.state import StatesGroup, State

class BuyState(StatesGroup):
  name = State()
  email = State()
  phone = State()
  address = State()
  id_ = State()
