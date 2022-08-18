from flask import Flask, request, jsonify

from backend.helpers import get_db_connection

APP = Flask(__name__)

def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:4200'
    return response

APP.after_request(after_request)

# API = Api(APP)

@APP.route('/data', methods=['GET'])    
def MainRoute():
    symbol = request.args['metric']
    conn, cur = get_db_connection()
    results = cur.execute(f"SELECT * FROM price_in_usdt where symbol = '{symbol}' and timestamp >= datetime('now','-24 hours')").fetchall()
    return [
        dict(timestamp=row[0],
             symbol=row[1],
             price=row[2])
        for row in results
    ]

@APP.route('/metric-options', methods=['GET'])    
def MetricOptionsRoute():
    conn, cur = get_db_connection()
    results = cur.execute(f"WITH metric_average as ("
                          f"SELECT "
                          f"symbol, "
                          f"AVG(price) as avg_price "
                          f"FROM price_in_usdt "
                          f"WHERE timestamp >= datetime('now','-24 hours') "
                          f"GROUP BY symbol "
                          f"),"
                          f"metric_variance as ("
                          f"SELECT "
                          f"piu.symbol, "
                          f"SUM(pow(price - avg_price,2)) / count(piu.symbol) as variance "
                          f"FROM price_in_usdt piu "
                          f"JOIN metric_average ma "
                          f"    ON ma.symbol=piu.symbol "
                          f"GROUP BY piu.symbol "
                          f")"
                          f"select "
                          f"symbol, "
                          f"ROW_NUMBER() OVER (ORDER BY variance desc) rank "
                          f"from metric_variance "
                          f"order by symbol").fetchall()
    return [
        dict(symbol=row[0],
             rank=f'{row[1]}/{len(results)}',
             )
        for row in results
    ]


if __name__ == "__main__":
    APP.run(host='0.0.0.0', port=5000, debug=True)