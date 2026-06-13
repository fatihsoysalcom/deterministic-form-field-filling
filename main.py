import json
from datetime import datetime

def fill_form_deterministically(input_data: dict) -> dict:
    """
    Simulates deterministic form filling by processing input data against a predefined schema.
    Ensures consistent output for the same input, handling defaults and formatting.
    This logic would typically precede the actual PDF field population.
    """
    filled_form = {}

    # Define the expected fields, their types, default values, and transformation rules.
    # This explicit definition is crucial for achieving determinism, ensuring predictable
    # processing regardless of minor input variations or missing data.
    field_definitions = {
        "name": {"type": str, "default": "N/A"},
        "email": {"type": str, "default": "no_email@example.com"},
        "age": {
            "type": int,
            "default": 0,
            "transform": lambda x: int(x) if isinstance(x, (int, float)) or (isinstance(x, str) and str(x).isdigit()) else 0
        },
        "submission_date": {
            "type": str,
            "default": "2023-01-01 12:00:00", # A fixed default ensures determinism if no date is provided.
            "transform": lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y-%m-%d %H:%M:%S")
                                   if isinstance(x, str) and len(x) == 10 and x.count('-') == 2
                                   else "2023-01-01 12:00:00" # Fallback for invalid date strings.
        }
    }

    for field_name, definition in field_definitions.items():
        value = input_data.get(field_name)

        if value is None:
            # If input is missing, apply the consistent default value.
            # This ensures predictability even with incomplete input data.
            filled_form[field_name] = definition["default"]
        else:
            # Apply transformation/type conversion for consistency.
            # This handles variations in input format (e.g., '30' vs 30 for age).
            if "transform" in definition:
                filled_form[field_name] = definition["transform"](value)
            else:
                # Ensure type consistency, falling back to default on error.
                try:
                    filled_form[field_name] = definition["type"](value)
                except (ValueError, TypeError):
                    filled_form[field_name] = definition["default"]

    return filled_form

# --- Demonstration of Deterministic Behavior ---

# Example Input Data 1
input_data_1 = {
    "name": "Alice Smith",
    "email": "alice.smith@example.com",
    "age": "30", # Age as string, will be deterministically converted to int
    "submission_date": "2023-10-26" # Date string, will be deterministically formatted
}

# Example Input Data 2 (semantically similar to 1, but 'age' is int)
input_data_2 = {
    "name": "Alice Smith",
    "email": "alice.smith@example.com",
    "age": 30, # Age as int
    "submission_date": "2023-10-26"
}

# Example Input Data 3 (incomplete and with invalid data)
input_data_3_incomplete = {
    "name": "Bob Johnson",
    "age": "twenty-five", # Invalid age, will fall back to default
    "submission_date": "invalid-date" # Invalid date, will fall back to default
}

print("--- Run 1 with input_data_1 ---")
result_1 = fill_form_deterministically(input_data_1)
print(json.dumps(result_1, indent=2))

print("\n--- Run 2 with input_data_1 (should be identical to Run 1) ---")
result_1_again = fill_form_deterministically(input_data_1)
print(json.dumps(result_1_again, indent=2))
# This explicitly demonstrates determinism: the same input always yields the exact same output.

print("\n--- Run 3 with input_data_2 (semantically same as input_data_1, different type for age) ---")
result_2 = fill_form_deterministically(input_data_2)
print(json.dumps(result_2, indent=2))
# This shows how robust processing (e.g., type conversion) contributes to determinism,
# ensuring consistent output even with slight input variations that resolve to the same value.

print("\n--- Run 4 with incomplete input_data_3 ---")
result_3 = fill_form_deterministically(input_data_3_incomplete)
print(json.dumps(result_3, indent=2))
# This demonstrates consistent handling of missing fields and invalid data,
# applying predefined defaults predictably.

# Programmatic assertion to confirm determinism for identical inputs
assert result_1 == result_1_again, "Deterministic filling failed: Same input yielded different output!"
print("\nAssertion passed: Same input always yields the same output.")
