from rest_framework.response import Response


def SuccessResponse(response, status=None, direct_results=False):
    """
    @summary: Success response is a utility function to output the final JSON response


    @param res: dict
    @return: Response object

    """

    if direct_results is False:
        response_dict = {}
        response_dict["result"] = True
        response_dict["data"] = response

        return Response(response_dict, status=status)
    return Response(response, status=status)


def UnauthorizedResponse():
    """
    @summary: Unauthorized response is a utility function to output the final JSON response
            when user is not authentciated

    @param status: int
    @return: Response object
    """

    response_dict = {}
    response_dict["status"] = "unauthorized"

    return Response(response_dict)


def ErrorResponse(message, status=None):
    """
    @summary: Error response is a utility function to output the final JSON response
            when we need send error message

    @param res: message
    @param status: int
    @return: Response object
    """

    response_dict = {}
    response_dict["status"] = "error"
    response_dict["message"] = message

    return Response(response_dict, status=status)


def NotFoundResponse(message, status=None):
    response_dict = {}
    response_dict["status"] = status
    response_dict["message"] = message
    return Response(response_dict)