def my_function():
    print("Function executed successfully!")
    return True  # Indicating success

# Calling the function and checking execution
try:
    result = my_function()
    #if result == True:
    print("Success:", result)
except Exception as e:
    print("Error:", e)
