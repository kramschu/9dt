from flask import Response


class ErrorHandlers:

    def _400_error(message):
        return Response(
                message,
                status=400,
            )

    def _404_error(message):
        return Response(
                message,
                status=404,
            )

    def _409_error(message):
        return Response(
                message,
                status=409,
            )

    def _410_error(message):
        return Response(
                message,
                status=410,
            )
