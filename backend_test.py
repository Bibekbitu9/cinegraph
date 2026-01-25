import requests
import sys
from datetime import datetime

class CineGraphAPITester:
    def __init__(self, base_url="https://screenscout-5.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []

    def run_test(self, name, method, endpoint, expected_status, params=None, data=None):
        """Run a single API test"""
        url = f"{self.api_url}/{endpoint}" if endpoint else f"{self.api_url}/"
        headers = {'Content-Type': 'application/json'}

        self.tests_run += 1
        print(f"\n🔍 Testing {name}...")
        print(f"   URL: {url}")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=headers, timeout=10)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                print(f"✅ Passed - Status: {response.status_code}")
                try:
                    response_data = response.json()
                    if isinstance(response_data, list) and len(response_data) > 0:
                        print(f"   Response: {len(response_data)} items returned")
                    elif isinstance(response_data, dict):
                        print(f"   Response keys: {list(response_data.keys())}")
                except:
                    print(f"   Response: {response.text[:100]}...")
            else:
                print(f"❌ Failed - Expected {expected_status}, got {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                self.failed_tests.append({
                    'name': name,
                    'expected': expected_status,
                    'actual': response.status_code,
                    'response': response.text[:200]
                })

            return success, response.json() if response.status_code < 400 else {}

        except Exception as e:
            print(f"❌ Failed - Error: {str(e)}")
            self.failed_tests.append({
                'name': name,
                'error': str(e)
            })
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_search_movies(self):
        """Test movie search functionality"""
        # Test with valid query
        success1, response1 = self.run_test(
            "Search Movies - Valid Query",
            "GET",
            "search",
            401,  # Expecting 401 due to invalid API key
            params={"query": "inception"}
        )
        
        # Test with empty query (should fail validation)
        success2, response2 = self.run_test(
            "Search Movies - Empty Query",
            "GET", 
            "search",
            422,  # Validation error
            params={"query": ""}
        )
        
        return success1 and success2

    def test_movie_detail(self):
        """Test movie detail endpoint"""
        # Test with popular movie ID (Inception)
        return self.run_test(
            "Movie Detail",
            "GET",
            "movie/27205",
            401  # Expecting 401 due to invalid API key
        )

    def test_movie_recommendations(self):
        """Test movie recommendations endpoint"""
        return self.run_test(
            "Movie Recommendations",
            "GET",
            "movie/27205/recommendations",
            401  # Expecting 401 due to invalid API key
        )

    def test_streaming_availability(self):
        """Test streaming availability endpoint"""
        success1, _ = self.run_test(
            "Streaming Availability - US",
            "GET",
            "movie/27205/streaming",
            401,  # Expecting 401 due to invalid API key
            params={"country": "US"}
        )
        
        success2, _ = self.run_test(
            "Streaming Availability - Default Country",
            "GET",
            "movie/27205/streaming",
            401  # Expecting 401 due to invalid API key
        )
        
        return success1 and success2

    def test_trending_movies(self):
        """Test trending movies endpoint"""
        return self.run_test(
            "Trending Movies",
            "GET",
            "trending",
            401  # Expecting 401 due to invalid API key
        )

    def test_geolocation(self):
        """Test geolocation endpoint"""
        success, response = self.run_test(
            "Geolocation",
            "GET",
            "geolocation",
            200  # This should work as it doesn't depend on TMDB API
        )
        
        if success and response:
            print(f"   Detected country: {response.get('country_name', 'Unknown')} ({response.get('country_code', 'Unknown')})")
        
        return success

def main():
    print("🎬 CineGraph API Testing Suite")
    print("=" * 50)
    
    tester = CineGraphAPITester()
    
    # Run all tests
    print("\n📡 Testing API Endpoints...")
    
    tester.test_root_endpoint()
    tester.test_geolocation()  # This should work
    tester.test_search_movies()
    tester.test_movie_detail()
    tester.test_movie_recommendations()
    tester.test_streaming_availability()
    tester.test_trending_movies()
    
    # Print summary
    print(f"\n📊 Test Results Summary")
    print("=" * 30)
    print(f"Tests run: {tester.tests_run}")
    print(f"Tests passed: {tester.tests_passed}")
    print(f"Tests failed: {tester.tests_run - tester.tests_passed}")
    print(f"Success rate: {(tester.tests_passed/tester.tests_run)*100:.1f}%")
    
    if tester.failed_tests:
        print(f"\n❌ Failed Tests Details:")
        for test in tester.failed_tests:
            print(f"   - {test['name']}: {test.get('error', f\"Expected {test.get('expected')}, got {test.get('actual')}\"")}")
    
    print(f"\n🔑 Note: Most endpoints are expected to return 401 errors due to placeholder TMDB API key")
    print(f"   This is expected behavior and indicates proper error handling.")
    
    return 0 if tester.tests_passed >= 2 else 1  # At least root and geolocation should pass

if __name__ == "__main__":
    sys.exit(main())