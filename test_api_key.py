#!/usr/bin/env python3
"""Test script for OpenAI API key stored in .env file."""

import os
from dotenv import load_dotenv
from openai import OpenAI

def test_api_key():
    """Load and test the OpenAI API key from .env file."""
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the API key from environment
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: OPENAI_API_KEY not found in .env file")
        print("   Make sure your .env file contains: OPENAI_API_KEY=your-key-here")
        return False
    
    if api_key.strip() == "":
        print("❌ ERROR: OPENAI_API_KEY is empty in .env file")
        return False
    
    print(f"✓ Found API key: {api_key[:10]}...{api_key[-4:]}")
    print("Testing API key...")
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Make a simple API call to test the key
        response = client.models.list()
        
        print("✓ API key is valid!")
        print(f"✓ Successfully connected to OpenAI API")
        print(f"✓ Available models: {len(response.data)} models found")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: API key test failed")
        print(f"   Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_api_key()

