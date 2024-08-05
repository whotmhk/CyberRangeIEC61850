######################################################################################################
# This is for MSSD Project Student ID 1007386
# Titled : Cyber Range of Critical Infrastructure for Cybersecurity Experiment
# Reference : Mitre Caldera OT- IEC61850
######################################################################################################



import subprocess
import datetime

# Prompt the user for the command part (e.g., SIED2CTRL/XCBR1.Pos)
command_part = input("Please enter the command part (e.g., SIED2CTRL/XCBR1.Pos): ")

# Prompt the user for the parameters (e.g., --bool=false)
parameters = input("Please enter the parameters (e.g., --bool=false): ")

# Prompt the user for an IP address
ip_address = input("Please enter the IP address: ")

# Construct the command with the user's inputs
command = ['.\iec61850_actions.exe', 'control', command_part, parameters, ip_address]

# Show the command to the user and ask for confirmation to proceed
print(f"Command to be executed: {' '.join(command)}")
confirm = input("Do you want to continue with this command? (yes/no): ")

if confirm.lower() in ['yes', 'y']:  # Accept both 'yes' and 'y' as affirmative responses
    # Run the command if the user confirms
    result = subprocess.run(command, capture_output=True, text=True)

    # Check if the process was successful
    if result.returncode == 0:
        print("Execution successful")
        print("Output:", result.stdout)

        # Get the current datetime to use as the filename
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mms_Contol_output_{timestamp}.txt"
        
        # Write the output to the file
        with open(filename, 'w') as file:
            file.write(result.stdout)

        print(f"Output saved to {filename}")
    else:
        print("Execution failed")
        print("Error:", result.stderr)
else:
    print("Command execution cancelled by user.")
