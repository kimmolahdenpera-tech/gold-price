from http.server import BaseHTTPRequestHandler
import json
import urllib.request
from datetime import datetime, timezone

YAHOO_URL = 'https://query1.finance.yahoo.com/v8/finance/chart/GC%3DF?interval=1m&range=1d'


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            req = urllib.request.Request(
                YAHOO_URL,
                headers={
                    'Accept': 'application/json',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
                }
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())

            price = data['chart']['result'][0]['meta']['regularMarketPrice']

            body = json.dumps({
                'price': float(price),
                'currency': 'USD',
                'unit': 'troy oz',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }).encode()

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(body)

        except Exception as e:
            body = json.dumps({'error': str(e)}).encode()
            self.send_response(502)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(body)
