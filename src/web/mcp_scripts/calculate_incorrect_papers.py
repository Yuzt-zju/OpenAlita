import re
import math

def calculate_incorrect_papers(query=""):
    """Calculates the number of incorrect papers based on p-value and total number of papers.

    Arguments:
        query (str): The query containing p-value and total number of papers.

    Returns:
        int or str: Number of incorrect papers rounded to the next integer, or an error message."""
    try:
        # Extract the p-value and total number of papers from the query
        p_value_match = re.search(r"p-value of (\d+\.\d+)", query)
        total_papers_match = re.search(r"articles published by Nature in (\d+)", query)

        if not p_value_match or not total_papers_match:
            return "Error: Invalid query format. Could not extract p-value or total number of papers."

        # Parse the extracted values
        p_value = float(p_value_match.group(1))
        total_papers = int(total_papers_match.group(1))

        # Calculate the number of incorrect papers
        incorrect_papers = p_value * total_papers

        # Round up to the next integer
        return math.ceil(incorrect_papers)
    except Exception as e:
        return f"Error: {str(e)}"
