from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if response is not None:
        customized_response = {}
        customized_response["validations"] = {}
        for key, value in response.data.items():
            if key == "detail":
                # Return 'no_auth_error' if is authentication error
                if (
                    str(value)
                    == "Authentication credentials were not provided."
                ):
                    customized_response["detail"] = "no_auth_error"
                else:
                    customized_response["detail"] = value
            else:
                if type(value) is dict:
                    for k, v in value.items():
                        customized_response["validations"][key][k] = v
                elif type(value) is list:
                    for inner_val in value:
                        customized_response["validations"][key] = {}
                        if type(inner_val) is dict:
                            for k, v in inner_val.items():
                                customized_response["validations"][key][k] = v
                        else:
                            error = "".join(value)
                            customized_response["validations"][key] = error
                else:
                    error = "".join(value)
                    customized_response["validations"][key] = error

        response.data = customized_response

    return response
