import json

def load_workflow(filename):
    """
    Load the workflow JSON file.
    """
    with open(filename, "r") as file:
        data = json.load(file)
    # The responses are stored under a top-level key "responses"
    return data.get("responses", {})

def find_next_options(current_path, workflow):
    """
    Determine the next available options based on the current_path.
    The function finds keys in the workflow that start with current_path 
    plus a separator ('/') and extracts the immediate next segment.
    """
    options = set()
    prefix = current_path + "/" if current_path else ""
    for key in workflow:
        if key.startswith(prefix):
            segments = key[len(prefix):].split("/")
            if segments and segments[0]:
                options.add(segments[0])
    return sorted(list(options))

def is_final_node(current_path, workflow):
    """
    Check if the current_path directly amatches a key in workflow.
    A final node is reached if current_path is directly a key and
    there are no additional segments (options) available.
    """
    direct_match = current_path in workflow
    further_options = len(find_next_options(current_path, workflow)) > 0
    return direct_match and not further_options

def display_buttons(options):
    """
    Display available options as numbered buttons.
    """
    print("\nAvailable options:")
    for idx, option in enumerate(options, start=1):
        # Convert underscores to spaces and title-case for user-friendly display.
        print(f"  {idx}. {option.replace('_', ' ').title()}")

def get_user_choice(options):
    """
    Prompt the user to select one of the available options.
    """
    while True:
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print("Please enter a valid number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_bot(workflow):
    """
    Main loop to interact with the user and navigate through the workflow.
    Starts from an empty path so that the top-level categories are shown.
    """
    current_path = ""  # Start with an empty path to show top-level categories.
    print("Welcome to the Bank Alfalah Bot!")
    
    while True:
        options = find_next_options(current_path, workflow)
        if not options:
            break  # No further options available.
        
        # If a final node is reached, exit the loop.
        if is_final_node(current_path, workflow):
            break
        
        display_buttons(options)
        selected = get_user_choice(options)
        
        # Append the selected option to current_path.
        current_path = current_path + ("" if current_path == "" else "/") + selected
        print(f"\nYou selected: {selected.replace('_', ' ').title()}")
        
        if is_final_node(current_path, workflow):
            break
    
    # Lookup and display the final response.
    if current_path in workflow:
        print("\nFinal Response:")
        print(workflow[current_path])
    else:
        print("Sorry, we couldn't find a final response for your selection.")

if __name__ == "__main__":
    workflow_file = "workflow.json"  # Ensure this file contains your complete JSON.
    workflow_data = load_workflow(workflow_file)
    run_bot(workflow_data)
