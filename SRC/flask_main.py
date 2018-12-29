from flask import Flask, request
import json
import queries
import DBconnection

app = Flask(__name__)


@app.route('/')
def main_page():
    return 'Hello World!'


@app.route('/ingredients')
def get_ingredients():
    query = queries.temp1

    x = DBConnection.execute_query(query, 7)
    # t = DBConnection.rowsToJson(x)
    """
    :return: A json representing all the ingredients exist in the DB.
    """
    # here should come a db query
    # return json.dumps("THE_QUERY_RESULT1")
    return x


@app.route('/filters')
def get_available_filters():
    """
    :return: A json representing all the filters we support
    """
    # here should come a db query


    #                            Converting MySQL query to JSON:
    # row_headers = [x[0] for x in cur.description]  # this will extract row headers
    # rv = cur.fetchall()
    # json_data = []
    # for result in rv:
    #     json_data.append(dict(zip(row_headers, result)))
    #
    return json.dumps("THE_FILTERS")


@app.route('/cocktails')
def get_cocktails():
    """
    The url is of the form: "/cocktails?ingredients=LIST_OF_INGREDIENTS&filters=LIST_OF_FILTERS"
    :return: json representing all matching cocktails
    """
    try:
        ingredients = request.args.get('ingredients')
        filters = request.args.get('filters')
    except Exception as e:
        return "Error: wrong arguments were given."

    # here should come a db query
    return json.dumps("THE_COCKTAILS")


if __name__ == '__main__':
    app.run(debug=True, port="8000")
    app.run(threaded=True) # GOOD YUVAL
