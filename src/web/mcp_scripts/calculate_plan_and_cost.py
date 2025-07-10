import re
import math

def calculate_plan_and_cost(query=""):
    try:
        # Plan details
        plans = {
            "Standard": {"storage_limit_tb": 2, "price_per_month": 9.99},
            "Plus": {"storage_limit_tb": 10, "price_per_month": 19.99},
            "Premium": {"storage_limit_tb": 50, "price_per_month": 39.99}
        }

        # Current plan
        current_plan = "Standard"
        current_storage_limit_tb = plans[current_plan]["storage_limit_tb"]
        current_price_per_month = plans[current_plan]["price_per_month"]

        # Extract query details
        overage_match = re.search(r"(\d+)GB over the limit", query)
        uploaded_files_match = re.search(r"uploaded (\d+) equally sized files", query)
        remaining_files_match = re.search(r"(\d+) more files", query)

        if not (overage_match and uploaded_files_match and remaining_files_match):
            return "Error: Could not extract necessary information from the query."

        overage_gb = int(overage_match.group(1))
        uploaded_files = int(uploaded_files_match.group(1))
        remaining_files = int(remaining_files_match.group(1))

        # Calculate file size and total required storage
        file_size_gb = overage_gb / uploaded_files
        total_files = uploaded_files + remaining_files
        total_storage_gb = total_files * file_size_gb
        total_storage_tb = total_storage_gb / 1024

        # Determine the minimum plan to accommodate storage
        for plan_name, plan_details in plans.items():
            if total_storage_tb <= plan_details["storage_limit_tb"]:
                upgrade_plan = plan_name
                upgrade_price_per_month = plan_details["price_per_month"]
                break
        else:
            return "Error: Storage exceeds all available plans."

        # Calculate the additional cost per file
        additional_cost_per_month = upgrade_price_per_month - current_price_per_month
        average_additional_cost_per_file = additional_cost_per_month / total_files

        # Return the result rounded to two decimal places
        return f"{average_additional_cost_per_file:.2f}"

    except Exception as e:
        return f"Error: {str(e)}"

# Example usage
query = "I have the Standard plan in the image below, and I just uploaded 60 equally sized files and got a message that I'm 100GB over the limit. I have 980 more files of the same size to upload."
print(calculate_plan_and_cost(query))