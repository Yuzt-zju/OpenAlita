import re
import math

def calculate_additional_cost_per_file(query=""):
    try:
        # Extract relevant details from query using regex
        overage_match = re.search(r"(\d+)GB over the limit", query)
        uploaded_files_match = re.search(r"uploaded (\d+) equally sized files", query)
        remaining_files_match = re.search(r"(\d+) more files", query)

        if not (overage_match and uploaded_files_match and remaining_files_match):
            return "Error: Query must contain 'X uploaded files', 'Y GB over the limit', and 'Z more files'."

        overage_gb = int(overage_match.group(1))
        uploaded_files = int(uploaded_files_match.group(1))
        remaining_files = int(remaining_files_match.group(1))

        # Plan details
        plans = {"Standard": {"limit_tb": 2, "price": 9.99}, "Plus": {"limit_tb": 10, "price": 19.99}, "Premium": {"limit_tb": 50, "price": 39.99}}
        current_plan = "Standard"  # Assume Standard plan for baseline

        # Calculate file size and total storage requirements
        file_size_gb = overage_gb / uploaded_files
        total_files = uploaded_files + remaining_files
        total_storage_gb = total_files * file_size_gb
        total_storage_tb = total_storage_gb / 1024

        # Find required plan
        for plan_name, plan_details in plans.items():
            if total_storage_tb <= plan_details["limit_tb"]:
                upgrade_cost = plan_details["price"] - plans[current_plan]["price"]
                break
        else:
            return "Error: No plan can accommodate the total storage."

        # Calculate and return average additional cost per file
        additional_cost_per_file = upgrade_cost / total_files
        return f"{additional_cost_per_file:.2f}"

    except Exception as e:
        return f"Error: {str(e)}"
