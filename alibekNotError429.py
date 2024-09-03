import requests
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# List of User Agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    # Add more user agents as needed
]

# List of Proxy Servers (if available)
PROXIES = [
    # "http://username:password@proxy_ip:proxy_port",  # Format for proxy with authentication
    # "http://proxy_ip:proxy_port",                   # Format for proxy without authentication
    # Add more proxies if available
]

# Target API endpoint
API_ENDPOINT = "https://example.com/api/endpoint"

# Function to send a single GET request
def send_request(session, user_agent, proxy=None):
    headers = {
        "User-Agent": user_agent,
    }
    try:
        # Use proxy if available
        response = session.get(API_ENDPOINT, headers=headers, proxies={"http": proxy, "https": proxy} if proxy else None)
        print(f"Status Code: {response.status_code}, Response: {response.text[:50]}")  # Print partial response for brevity
        return response.status_code
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Function to handle multiple requests
def send_requests_concurrently(total_requests, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        with requests.Session() as session:
            futures = []
            for _ in range(total_requests):
                user_agent = random.choice(USER_AGENTS)
                proxy = random.choice(PROXIES) if PROXIES else None

                # Schedule the request with random delay
                futures.append(executor.submit(send_request, session, user_agent, proxy))
                time.sleep(random.uniform(0.1, 2))  # Random delay between 0.1 to 2 seconds

            # Wait for all futures to complete
            for future in as_completed(futures):
                if future.result() is not None:
                    print(f"Request completed with status: {future.result()}")

# Main function to run the script
if __name__ == "__main__":
    TOTAL_REQUESTS = 1000  # Number of requests to send
    MAX_WORKERS = 5  # Number of concurrent threads (adjust based on server's rate limit and network capacity)
    
    send_requests_concurrently(TOTAL_REQUESTS, MAX_WORKERS)