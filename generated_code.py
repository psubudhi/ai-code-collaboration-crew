def add_number_two(num: int) -> int:
    """
    Returns the sum of input number and 2.

    Args:
        num (int): Input number.

    Returns:
        int: Sum of input number and 2.

    Raises:
        TypeError: If input is not an integer.
        ValueError: If input is NaN (Not a Number) or infinite.
    """
    
    # Check if input is an integer
    if not isinstance(num, int):
        raise TypeError("Input must be an integer.")
    
    # Check if input is NaN or infinite
    if num != num:  # NaN is the only value that is not equal to itself
        raise ValueError("Input cannot be NaN (Not a Number) or infinite.")
    
    # Attempt to add 2 to the input number
    try:
        result = num + 2
        return result
    
    # Catch and raise any exceptions that occur during the calculation
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    # Test the function with valid input
    print(add_number_two(5))  # Output: 7
    
    # Test the function with invalid input type
    try:
        print(add_number_two("five"))
    except TypeError as e:
        print(e)  # Output: Input must be an integer.
    
    # Test the function with NaN input
    try:
        print(add_number_two(float('nan')))
    except ValueError as e:
        print(e)  # Output: Input cannot be NaN (Not a Number) or infinite.
    
    # Test the function with infinite input
    try:
        print(add_number_two(float('inf')))
    except ValueError as e:
        print(e)  # Output: Input cannot be NaN (Not a Number) or infinite.