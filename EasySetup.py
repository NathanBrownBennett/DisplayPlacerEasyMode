import subprocess
import os 

def run_displayplacer_list():
    try:
        result = subprocess.check_output(['displayplacer', 'list'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError:
        return 'Install DisplayPlacer via Homebrew with brew install displayplacer'

def parse_displayplacer_output(result):
    displays = []
    display = {}  # Initialize the dictionary outside the loop
    for line in result.splitlines():
        if "Persistent screen id:" in line:
            if display:  # Check if the display dictionary is not empty
                displays.append(display)  # Append the previous display before starting a new one
            display = {'Persistent screen id': line.split(": ")[1]}  # Start a new display dictionary
        elif "Contextual screen id:" in line:
            display['Contextual screen id'] = line.split(": ")[1]
        elif "Serial screen id:" in line:
            display['Serial screen id'] = line.split(": ")[1]
        elif "Type:" in line:
            display['Type'] = line.split(": ")[1]
        elif "Resolution:" in line:
            display['Resolution'] = line.split(": ")[1]
        elif "Hertz:" in line:
            display['Hertz'] = line.split(": ")[1]
        elif "Color Depth:" in line:
            display['Color Depth'] = line.split(": ")[1]
        elif "Scaling:" in line:
            display['Scaling'] = line.split(": ")[1]
        elif "Origin:" in line:
            display['Origin'] = line.split(": ")[1]
        elif "Rotation:" in line:
            display['Rotation'] = line.split(": ")[1]
            # No need to assume Rotation is the last item anymore
    if display:  # Check and append the last display dictionary if not empty
        displays.append(display)
    return displays

def generate_displayplacer_command(display):
    for display in display:
        command = f'displayplacer "id:{display["Persistent screen id"]} res:{display["Resolution"]} color_depth:{display["Color Depth"]} enabled:true scaling:{display["Scaling"]} origin:{display["Origin"]} degree:{display["Rotation"]}"'
    return command

def display_settings_shell(displays):

    def print_menu(options):
        os.system('clear')
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")

    def get_user_choice(prompt, num_options):
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= num_options:
                    os.system('clear')
                    return choice
                else:
                    os.system('clear')
                    print("Invalid selection. Please choose a valid option.")
            except ValueError:
                os.system('clear')
                print("Please enter a number.")
                
    def print_current_modifications(display):
        modifications = ", ".join([f"{key} = {value}" for key, value in display.items() if key not in ["Type"]])
        print("- " * 70)
        print("Current Modifications:")
        print(modifications if modifications else "None")
        print("- " * 70)

    def modify_display_settings(display):
        os.system('clear')
        print("\nModify settings for the selected display:")
        settings = ["Resolution", "Color Depth", "Scaling", "Rotation", "Origin", "Exit"]
        resolutions = ["1024x640", "1152x720", "1440x900", "1920x1080", "2560x1440", "3840x2160", "4096x2160","Custom"]
        color_depths = ["4", "8", "10","Custom"]
        while True:
            print_menu(settings)
            print_current_modifications(display)
            choice = int(input("Choose a setting to modify: "))
            if choice == len(settings):  # Exit option
                break
            setting = settings[choice - 1]
            
            if setting == "Resolution":
                print("Available Resolutions:")
                for i, res in enumerate(resolutions, 1):
                    print(f"{i}. {res}")
                res_choice = int(input("Choose a resolution: "))
                if res_choice != len(resolutions):
                    new_value = resolutions[res_choice - 1]
                    os.system('clear')
                else:
                    new_value = input("Enter new custom value for Resolution (e.g., 1920x1080): ").lower()
                    os.system('clear')
                    
            elif setting == "Color Depth":
                print("Available Color Depths:")
                for i, depth in enumerate(color_depths, 1):
                    print(f"{i}. {depth}")
                depth_choice = int(input("Choose a color depth: "))
                if depth_choice != len(color_depths):
                    new_value = color_depths[depth_choice - 1]
                    os.system('clear')
                else:
                    new_value = input("Enter new custom value for Color Depth (e.g., 10): ")
                    os.system('clear')

            elif setting == "Scaling":
                scaling_input = input("Enter new value for Scaling (on/off): ").lower()
                new_value = "on" if scaling_input == "on" else "off"
                os.system('clear')
            else:
                new_value = input(f"Enter new value for {setting}: ")
                os.system('clear')

            display[setting] = new_value
            print(f"{setting} updated to {new_value}.")

    if not displays:
        os.system('clear')
        print("No displays found.")
        return

    while True:
        os.system('clear')
        print("\nAvailable Displays:")
        for i, display in enumerate(displays, start=1):
            print(f"{i}. Display Type: {display['Type']}")
        print_current_modifications(displays[choice - 1] if 'choice' in locals() and choice > 0 and choice <= len(displays) else {})

        def adjust_another_display(display):
            os.system('clear')
            print("Would you like to adjust another display?")
            choice = input("Enter 'y' for yes or 'n' for no: ").lower()
            if choice == 'y':
                modify_display_settings(display)
            else:
                return
        
        choice = int(input("Select a display to modify (Use '-1' to generate and run current modifications script or 0 to exit): "))
        if choice == -1:
            os.system('clear')
            command = generate_displayplacer_command(displays)
            print("Modifications script generated:", command)
            apply_modifications = input("Would you like to apply the modifications? (y/n): ").lower()
            if apply_modifications == "y":
                os.system('clear')
                print("Applying modifications...")
                try:
                    subprocess.call(command, shell=True)
                    print("Modifications applied successfully.")
                except Exception as e:
                    print(f"Failed to apply Modifications: {e}")
                break
            else:
                os.system('clear')
                print("Modifications not applied.")
                adjust_another_display(displays)
                break
            
        if choice == 0:
            os.system('clear')
            break
        else:
            if choice > len(displays):
                os.system('clear')
                print("Invalid selection. Please choose a valid display.")
                continue
            

        selected_display = displays[choice - 1]
        modify_display_settings(selected_display)

    print("Exiting settings shell...")

def main():
    # Run the displayplacer list command and get the output
    display_output = run_displayplacer_list()

    #Parse the display information from the output
    display_info = parse_displayplacer_output(display_output)

    #Display the settings shell to modify the display settings
    display_settings_shell(display_info)

    # Generate the displayplacer command based on the modified display settings
    displayplacer_command = generate_displayplacer_command(display_info)

    # Print the customised command
    print(displayplacer_command)
    
if __name__ == "__main__":
    main()