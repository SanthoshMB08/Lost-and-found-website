from fuzzywuzzy import fuzz, process

def fuzzy_match(query, choices, threshold=75, limit=5):
    """
    Returns list of top matches with scores
    """
    try:
        results = process.extract(
            query,
            choices,
            scorer=fuzz.partial_ratio
        )
        return [(match, score) for match, score in results if score >= threshold][:limit]
    except Exception as e:
        print(f"Fuzzy match error: {str(e)}")
        return []