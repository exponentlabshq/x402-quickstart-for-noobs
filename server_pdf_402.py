#!/usr/bin/env python3
"""HTTP server that serves x402-payload.pdf only after payment verification."""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PDF_FILE = "x402-payload.pdf"

class PDFPaymentHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Check if payment header is present
        payment_token = self.headers.get('X-Payment-Token')
        
        if payment_token == 'paid':
            # User has paid, serve the PDF
            if not os.path.exists(PDF_FILE):
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_response = {
                    "error": "File not found",
                    "message": f"{PDF_FILE} does not exist"
                }
                self.wfile.write(json.dumps(error_response).encode())
                return
            
            try:
                # Read the PDF file
                with open(PDF_FILE, 'rb') as pdf_file:
                    pdf_content = pdf_file.read()
                
                # Send successful response with PDF
                self.send_response(200)
                self.send_header("Content-type", "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="{PDF_FILE}"')
                self.send_header("Content-Length", str(len(pdf_content)))
                self.end_headers()
                self.wfile.write(pdf_content)
                
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                error_response = {
                    "error": "Server error",
                    "message": str(e)
                }
                self.wfile.write(json.dumps(error_response).encode())
        else:
            # Payment required
            self.send_response(402)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {
                "error": "Payment Required",
                "message": f"This endpoint requires payment to access {PDF_FILE}",
                "payment_url": "http://localhost:8001/pay",
                "amount": "0.01",
                "instructions": "Send a request with header: X-Payment-Token: paid",
                "file": PDF_FILE
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        """Override to show cleaner logs."""
        print(f"{args[0]} - {args[1]}")

if __name__ == "__main__":
    if not os.path.exists(PDF_FILE):
        print(f"⚠️  Warning: {PDF_FILE} not found in current directory")
        print(f"   Make sure {PDF_FILE} exists before running the server\n")
    
    print("402 Payment Required PDF Server running at http://localhost:8001")
    print(f"\nTry these commands:")
    print(f"  curl -i http://localhost:8001")
    print(f"  curl -H 'X-Payment-Token: paid' http://localhost:8001 -o downloaded.pdf")
    print(f"\nPress Ctrl+C to stop\n")
    HTTPServer(("", 8001), PDFPaymentHandler).serve_forever()

