import re
import math

def calculate_false_positive_rate(query=""):
    """Calculates the false positive rate using p-value threshold and number of articles.

    Arguments:
        query (str): The query containing the year and p-value.

    Returns:
        int or str: The calculated false positive rate or an error message."""
    try:
        # Extract the p-value threshold and the number of articles from the query
        p_value_match = re.search(r"p-value of (\d+\.\d+)", query)
        articles_match = re.search(r"all articles published by Nature in (\d+)", query)

        if not p_value_match or not articles_match:
            return "Error: Could not extract p-value or number of articles from the query."

        p_value = float(p_value_match.group(1))
        num_articles = int(articles_match.group(1))

        # Calculate the false positive rate
        false_positives = math.ceil(p_value * num_articles)

        return false_positives
    except Exception as e:
        return f"Error: {str(e)}"
