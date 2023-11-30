from constants.constants import StatusConstants


class LMSController:
    def __init__(self, lms_service):
        self.lms_service = lms_service

    def process_command(self, command):
        command_parts = command.split()

        if not command_parts:
            return

        try:
            if command_parts[0] == StatusConstants.ADD_COURSE_OFFERING:
                result = self.lms_service.add_course_offering(*command_parts[1:])
                print(result)
            elif command_parts[0] == StatusConstants.REGISTER:
                result, status = self.lms_service.register_for_course(*command_parts[1:])
                if result:
                    print(f"{result} {status}")
                else:
                    print(f"{status}")

            elif command_parts[0] == StatusConstants.CANCEL:
                result, status = self.lms_service.cancel_registration(*command_parts[1:])
                if result:
                    print(f"{result} {status}")
            elif command_parts[0] == StatusConstants.ALLOT_COURSE:
                result, status = self.lms_service.allot_course(*command_parts[1:])
                if result:
                    for registration in result:
                        print(f"{registration} {status}")
        except Exception as e:
            print(StatusConstants.INPUT_DATA_ERROR)