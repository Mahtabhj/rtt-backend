from django.db import connection


class QueryAndTimeCount:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        sqltime = 0
        queries = connection.queries
        for query in queries:
            sqltime += float(query["time"])
        print(
            "-:*****Page render: " + str(sqltime) + "sec for " + str(len(connection.queries)) + " queries :-*****")
        return response
