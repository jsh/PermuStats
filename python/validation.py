import math
import requests
import json
import os

def validate_results(n, distribution):
    """Verifies combinatorial identities: Sum(freq) = n! and E[X] = 1."""
    n_factorial = math.factorial(n)
    total_count = sum(distribution.values())
    weighted_sum = sum(val * freq for val, freq in distribution.items())
    return total_count == n_factorial and weighted_sum == n_factorial

class OEISLookup:
    _cache_file = "oeis_cache.json"

    @staticmethod
    def format_sequence(n, distribution):
        """Converts distribution to "val0,val1,val2..." string."""
        return ",".join(str(distribution.get(i, 0)) for i in range(n + 1))

    @classmethod
    def search(cls, sequence_str):
        """
        Queries OEIS with a local JSON cache to prevent redundant API hits.
        Returns a dict with 'id' and 'name' or None.
        """
        # 1. Check local cache first
        cache = cls._load_cache()
        if sequence_str in cache:
            return cache[sequence_str]

        # 2. Perform live search
        url = f"https://oeis.org/search?q={sequence_str}&fmt=json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get("results"):
                result = {
                    "id": f"A{data['results'][0]['number']:06d}",
                    "name": data["results"][0]["name"]
                }
                # 3. Save to cache
                cache[sequence_str] = result
                cls._save_cache(cache)
                return result
                
        except Exception as e:
            return {"error": f"Connection failed: {e}"}
        
        return None

    @classmethod
    def _load_cache(cls):
        if os.path.exists(cls._cache_file):
            with open(cls._cache_file, 'r') as f:
                return json.load(f)
        return {}

    @classmethod
    def _save_cache(cls, cache):
        with open(cls._cache_file, 'w') as f:
            json.dump(cache, f, indent=4)
