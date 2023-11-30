from controllers.lms_controller import LMSController
from services.lms_service import LMSService

lms_service = LMSService()
lms_controller = LMSController(lms_service)

while True:
    user_input = input()
    if user_input.lower() == 'exit':
        break
    lms_controller.process_command(user_input)