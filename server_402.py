#!/usr/bin/env python3
"""Simple HTTP server that demonstrates HTTP 402 Payment Required."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class PaymentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if payment header is present
        payment_token = self.headers.get('X-Payment-Token')
        
        if payment_token == 'paid':
            # User has paid, return the content
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "message": "Welcome! Here's your premium content.",
                "data": "This is the secret data you paid for!"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            # Payment required
            self.send_response(402)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "error": "Payment Required",
                "message": "This endpoint requires payment to access",
                "payment_url": "http://localhost:8000/pay",
                "amount": "0.01",
                "instructions": "Send a request with header: X-Payment-Token: paid"
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        """Override to show cleaner logs."""
        print(f"{args[0]} - {args[1]}")

if __name__ == "__main__":
    print("402 Payment Required Server running at http://localhost:8000")
    print("\nTry these commands:")
    print("  curl http://localhost:8000")
    print("  curl -H 'X-Payment-Token: paid' http://localhost:8000")
    print("\nPress Ctrl+C to stop\n")
    HTTPServer(("", 8000), PaymentHandler).serve_forever()

