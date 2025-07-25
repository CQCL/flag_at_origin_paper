import numpy as np
from pytket import Circuit, Qubit
from pytket.circuit.display import render_circuit_as_html
from pytket.circuit import UnitID, OpType, Op
from pytket._tket.circuit import Command
from pytket.unit_id import QubitRegister, BitRegister
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pytket import Circuit
import webbrowser
import os # for the folder path
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def save_circuit(circ: Circuit, folder_path: str, filename=None) -> None:
    if filename is None:
        filename = datetime.now().strftime("%Y%m%d_%H%M%S") + '.html'
    html = render_circuit_as_html(circ)
    with open(folder_path + filename, 'w') as f:
        f.write(html)

def generate_FT_plaq_notebook(distance, qubits):

    folder_path = os.path.dirname(os.path.abspath(__file__)) + '/' 

    # Construct the filename using the provided values
    filename = f"{distance}_{qubits}_X_ft_plaquette.txt"

    # Read circuit from text file
    file_path = os.path.join(folder_path, "Notebook_2", filename)
    with open(file_path, "r") as file:
        circuit_dict_str = file.read()

    # Convert string back to dictionary
    circuit_dict = eval(circuit_dict_str)

    # Create a circuit object from the dictionary
    loaded_circuit = Circuit.from_dict(circuit_dict)

    # Test: Print the circuit to verify it's loaded correctly
    print(loaded_circuit)

    # Save the circuit to an HTML file
    save_circuit(loaded_circuit, folder_path, filename=f'IMPORTED_circ_found.html')

    # Open the HTML file in the default web browser
    print("Opening file in browser...")
    full_file_url = f'file://{os.path.abspath(os.path.join(folder_path, "IMPORTED_circ_found.html"))}'
    webbrowser.open(full_file_url)

    return


def choose_code(user_key):

    folder_path = os.path.dirname(os.path.abspath(__file__)) + '/'

    # Sample dictionary with pre-populated keys and values
    circuit_info_dict = {
        "[[7,1,3]]": {
            "entire_circuit": "SteaneCode.json", 
            "number_CNOTs": 15, 
            "number_simQUBITS": 8, 
            "number_ANC": 3
        },
        "[[17,1,5]]": {
            "entire_circuit": "SeventeenColorCode.json", 
            "number_CNOTs": 74, 
            "number_simQUBITS": 23, 
            "number_ANC": 21
        },
        "[[20,2,6]]": {
            "entire_circuit": "TwentyDist6Code.json", 
            "number_CNOTs": 145, 
            "number_simQUBITS": 36, 
            "number_ANC": 47
        },
        "[[23,1,7]]": {
            "entire_circuit": "GolayCode.json", 
            "number_CNOTs": 237, 
            "number_simQUBITS": 44, 
            "number_ANC": 80
        },
        "[[49,1,5]]": {
            "entire_circuit": "Code_[[49,1,5]]F.json", 
            "number_CNOTs": 361, 
            "number_simQUBITS": 95, 
            "number_ANC": 105
        },
        "[[49,1,9]]": {
            "entire_circuit": "Code_[[49,1,9]].json", 
            "number_CNOTs": 408, 
            "number_simQUBITS": 93, 
            "number_ANC": 136
        },
        "[[9,1,3]]": {
            "entire_circuit": "Code_[[9,1,3]].json", 
            "number_CNOTs": 26, 
            "number_simQUBITS": 12, 
            "number_ANC": 9
        },
        "[[25,1,5]]": {
            "entire_circuit": "Code_[[25,1,5]]F.json", 
            "number_CNOTs": 92, 
            "number_simQUBITS": 32, 
            "number_ANC": 28
        },
        "[[31,1,7]]": {
            "entire_circuit": "Code_[[31,1,7]].json", 
            "number_CNOTs": 211, 
            "number_simQUBITS": 55, 
            "number_ANC": 69
        },
        "[[49,1,7]]": {
            "entire_circuit": "Code_[[49,1,7]].json", 
            "number_CNOTs": 262, 
            "number_simQUBITS": 64, 
            "number_ANC": 85
        },
        "[[95,1,7]]": {
            "entire_circuit": "Code_[[95,1,7]]+.json", 
            "number_CNOTs": 1175, 
            "number_simQUBITS": 258, 
            "number_ANC": 380
        },
        "[[49,1,9]]": {
            "entire_circuit": "Code_[[49,1,9]].json", 
            "number_CNOTs": 408, 
            "number_simQUBITS": 93, 
            "number_ANC": 136
        },
        "[[81,1,9]]": {
            "entire_circuit": "Code_[[81,1,9]].json", 
            "number_CNOTs": 614, 
            "number_simQUBITS": 141, 
            "number_ANC": 206
        },
        "[[47,1,11]]": {
            "entire_circuit": "Code_[[47,1,11]].json", 
            "number_CNOTs": 1033, 
            "number_simQUBITS": 186, 
            "number_ANC": 388
        },
        "[[71,1,11]]": {
            "entire_circuit": "Code_[[71,1,11]].json", 
            "number_CNOTs": 829, 
            "number_simQUBITS": 177, 
            "number_ANC": 268
        }
    }

    # Function to allow the user to input a key and print corresponding values
   # """Retrieve and display circuit information based on the provided key."""
    # Check if the key exists in the dictionary
    if user_key in circuit_info_dict:
        # Print the corresponding values
        print("\nCircuit Information for key:", user_key)
        circuit_data = circuit_info_dict[user_key]
        print(circuit_data)

        # Open and load the circuit from the specified file (entire_circuit)
        circuit_filename = circuit_data["entire_circuit"]
        json_path = os.path.join(folder_path, "Notebook_1", circuit_filename)
        with open(json_path, 'r') as f:
            circuit_json = json.load(f)

        # Convert the loaded JSON into a pytket Circuit object
        entire_circuit = Circuit.from_dict(circuit_json)
        print("Entire Circuit Data:")

        # Save the circuit to an HTML file
        save_circuit(entire_circuit, folder_path, filename='ENTIRE_ft_circ_found.html')

        # Open the HTML file in the default web browser
        print("Opening file in browser...")
        full_file_url = f'file://{os.path.abspath(os.path.join(folder_path, "ENTIRE_ft_circ_found.html"))}'
        webbrowser.open(full_file_url)

        # Print the circuit's additional information
        print("Number of CNOTs:", circuit_data["number_CNOTs"])
        print("Number of Sim Qubits:", circuit_data["number_simQUBITS"])
        print("Number of Ancillas:", circuit_data["number_ANC"])
    else:
        print("Invalid key! Please try again.")

    return

def evaluate_logical_error_rate(media_key):

    # Sample second dictionary with possible image or string values
    media_dict = {
        "depolarizing": ["Notebook_1/state_prep.png"],  # Two images
       # "emulator": 'emulator.txt',  # Example string
        "hardware": "Notebook_1/hardware.txt"  # Example string
    }

    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        # If the value is a list (multiple images)
        if isinstance(media_value, list):
            # Plot the images side by side
            print(f"Displaying {len(media_value)} images.")
            fig, axes = plt.subplots(1, len(media_value), figsize=(10, 5))  # Create a subplot grid
            
            # Ensure axes is a list even if there is only one image
            if len(media_value) == 1:
                axes = [axes]
            
            # Loop through the images and plot each one
            for i, img_path in enumerate(media_value):
                # Debugging: Check if the file exists
                print(f"Checking file path: {img_path}")
                if not os.path.exists(img_path):
                    print(f"ERROR: {img_path} not found!")
                    return

                img = mpimg.imread(img_path)  # This line now uses the full path
                axes[i].imshow(img)
                axes[i].axis('off')  # Turn off axis for better presentation
            
            plt.show()  # Show the images
            
        # If it's a single image (not a list)
        elif media_value.endswith(".jpg"):
            # Plot the single image
            print(f"Displaying image: {media_value}")
            # Debugging: Check if the file exists
            if not os.path.exists(media_value):
                print(f"ERROR: {media_value} not found!")
                return

            img = mpimg.imread(media_value)  # This line now uses the full path
            plt.imshow(img)
            plt.axis('off')  # Turn off axis for better presentation
            plt.show()
        else:
            # If it's a text file, read the content
            if media_value.endswith(".txt"):
                print(f"Displaying string from file: {media_value}")
                # Read and display the string from the file
                with open(media_value, 'r') as f:
                    print(f.read())
            else:
                # If it's just a plain string, display it
                print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return


def show_hardware_shots(media_key):

    # Sample second dictionary with possible image or string values
    media_dict = {
        "hardware_exp1": 'Notebook_1/errors_vectors_CX.txt',  
        "hardware_exp2": 'Notebook_1/errors_vectors_CX_DD.txt',  
        "hardware_exp3": 'Notebook_1/errors_vectors_CZ.txt',  
        "hardware_exp4": 'Notebook_1/errors_vectors_CZ_DD.txt',  
        "hardware_exp5": 'Notebook_1/errors_vectors_CZ_customDD.txt',  
        "hardware_exp6": 'Notebook_1/errors_vectors_CZ_DD_H21.txt',  
        "hardware_exp7": 'Notebook_1/errors_vectors_CZ_DD_H22.txt',  

    }

    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        # If the value is a list (multiple images)
        if isinstance(media_value, list):
            # Plot the images side by side
            print(f"Displaying {len(media_value)} images.")
            fig, axes = plt.subplots(1, len(media_value), figsize=(10, 5))  # Create a subplot grid
            
            # Ensure axes is a list even if there is only one image
            if len(media_value) == 1:
                axes = [axes]
            
            # Loop through the images and plot each one
            for i, img_path in enumerate(media_value):
                img = mpimg.imread(img_path)
                axes[i].imshow(img)
                axes[i].axis('off')  # Turn off axis for better presentation
            
            plt.show()  # Show the images
        # If it's a single image (not a list)
        elif media_value.endswith(".jpg"):
            # Plot the single image
            print(f"Displaying image: {media_value}")
            img = mpimg.imread(media_value)
            plt.imshow(img)
            plt.axis('off')  # Turn off axis for better presentation
            plt.show()
        else:
            # If it's a text file, read the content
            if media_value.endswith(".txt"):
                print(f"Displaying string from file: {media_value}")
                # Read and display the string from the file
                with open(media_value, 'r') as f:
                    print(f.read())
            else:
                # If it's just a plain string, display it
                print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")


    return


def param_analysis():

    # Sample second dictionary with possible image or string values
    media_dict = {
        "depolarizing": ["log_err2.jpg", "acc_rat2.jpg"],  # Two images
    }

    # Function to allow the user to input a key and display corresponding media
    def display_media():
        while True:
            # Ask the user to input a key for media (depolarizing, emulator, simulator)
            media_key = "depolarizing"

            # Check if the key exists in the media dictionary
            if media_key in media_dict:
                media_value = media_dict[media_key]
                
                # If the value is a list (multiple images)
                if isinstance(media_value, list):
                    # Plot the images side by side
                    print(f"Displaying {len(media_value)} images.")
                    fig, axes = plt.subplots(1, len(media_value), figsize=(10, 5))  # Create a subplot grid
                    
                    # Ensure axes is a list even if there is only one image
                    if len(media_value) == 1:
                        axes = [axes]
                    
                    # Loop through the images and plot each one
                    for i, img_path in enumerate(media_value):
                        img = mpimg.imread(img_path)
                        axes[i].imshow(img)
                        axes[i].axis('off')  # Turn off axis for better presentation
                    
                    plt.show()  # Show the images
                # If it's a single image (not a list)
                elif media_value.endswith(".jpg"):
                    # Plot the single image
                    print(f"Displaying image: {media_value}")
                    img = mpimg.imread(media_value)
                    plt.imshow(img)
                    plt.axis('off')  # Turn off axis for better presentation
                    plt.show()
            else:
                print("Invalid media key! Please try again.")

            # Ask if they want to look up another media
           # another = input("\nDo you want to search for another media? (yes/no): ").strip().lower()
           # if another != "yes":
            break

    # Run the function to display media
    display_media()


    return


def Steane_analysis(media_key):

    # Sample second dictionary with possible image or string values
    media_dict = {
        "depolarizing": ["Notebook_1/steane.png"],  # Two images
    }

    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        # If the value is a list (multiple images)
        if isinstance(media_value, list):
            # Plot the images side by side
            print(f"Displaying {len(media_value)} images.")
            fig, axes = plt.subplots(1, len(media_value), figsize=(10, 5))  # Create a subplot grid
            
            # Ensure axes is a list even if there is only one image
            if len(media_value) == 1:
                axes = [axes]
            
            # Loop through the images and plot each one
            for i, img_path in enumerate(media_value):
                img = mpimg.imread(img_path)
                axes[i].imshow(img)
                axes[i].axis('off')  # Turn off axis for better presentation
            
            plt.show()  # Show the images
        # If it's a single image (not a list)
        elif media_value.endswith(".jpg"):
            # Plot the single image
            print(f"Displaying image: {media_value}")
            img = mpimg.imread(media_value)
            plt.imshow(img)
            plt.axis('off')  # Turn off axis for better presentation
            plt.show()
        else:
            # If it's a text file, read the content
            if media_value.endswith(".txt"):
                print(f"Displaying string from file: {media_value}")
                # Read and display the string from the file
                with open(media_value, 'r') as f:
                    print(f.read())
            else:
                # If it's just a plain string, display it
                print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return


def Steane_analysis_onlyX(media_key):

    # Sample second dictionary with possible image or string values
    media_dict = {
        "depolarizing": ["Notebook_1/onlyX.png"],  # Two images
    }

    # Function to allow the user to input a key and display corresponding media
    def display_media():
        while True:
            # Ask the user to input a key for media (depolarizing, emulator, simulator)
            media_key = "depolarizing"

            # Check if the key exists in the media dictionary
            if media_key in media_dict:
                media_value = media_dict[media_key]
                
                # If the value is a list (multiple images)
                if isinstance(media_value, list):
                    # Plot the images side by side
                    print(f"Displaying {len(media_value)} images.")
                    fig, axes = plt.subplots(1, len(media_value), figsize=(10, 5))  # Create a subplot grid
                    
                    # Ensure axes is a list even if there is only one image
                    if len(media_value) == 1:
                        axes = [axes]
                    
                    # Loop through the images and plot each one
                    for i, img_path in enumerate(media_value):
                        img = mpimg.imread(img_path)
                        axes[i].imshow(img)
                        axes[i].axis('off')  # Turn off axis for better presentation
                    
                    plt.show()  # Show the images
                # If it's a single image (not a list)
                elif media_value.endswith(".jpg"):
                    # Plot the single image
                    print(f"Displaying image: {media_value}")
                    img = mpimg.imread(media_value)
                    plt.imshow(img)
                    plt.axis('off')  # Turn off axis for better presentation
                    plt.show()
            else:
                print("Invalid media key! Please try again.")

            # Ask if they want to look up another media
           # another = input("\nDo you want to search for another media? (yes/no): ").strip().lower()
           # if another != "yes":
            break

    # Run the function to display media
    display_media()


    return


def evaluate_lUT(media_key):

    # Sample second dictionary with possible image or string values
    media_dict = {
        "[[7,1,3]]_0.01": ['Notebook_1/syndromes_S7_0.01F.txt', 'Notebook_1/logical_operators_S7_0.01F.txt'],  
        "[[7,1,3]]_0.005": ['Notebook_1/syndromes_S7_0.005F.txt', 'Notebook_1/logical_operators_S7_0.005F.txt'],
        "[[7,1,3]]_0.0025": ['Notebook_1/syndromes_S7_0.0025F.txt', 'Notebook_1/logical_operators_S7_0.0025F.txt'],
        "[[7,1,3]]_0.001": ['Notebook_1/syndromes_S7_0.001F.txt', 'Notebook_1/logical_operators_S7_0.001F.txt'],
        "[[7,1,3]]_0.00075": ['Notebook_1/syndromes_S7_0.00075F.txt', 'Notebook_1/logical_operators_S7_0.00075F.txt'],
        "[[7,1,3]]_0.0005": ['Notebook_1/syndromes_S7_0.0005F.txt', 'Notebook_1/logical_operators_S7_0.0005F.txt'],
        "[[17,1,5]]_0.01": ['Notebook_1/syndromes_S17_0.01F.txt', 'Notebook_1/logical_operators_S17_0.01F.txt'],  
        "[[17,1,5]]_0.005": ['Notebook_1/syndromes_S17_0.005F.txt', 'Notebook_1/logical_operators_S17_0.005F.txt'],
        "[[17,1,5]]_0.0025": ['Notebook_1/syndromes_S17_0.0025F.txt', 'Notebook_1/logical_operators_S17_0.0025F.txt'],
        "[[17,1,5]]_0.001": ['Notebook_1/syndromes_S17_0.001F.txt', 'Notebook_1/logical_operators_S17_0.001F.txt'],
        "[[17,1,5]]_0.00075": ['Notebook_1/syndromes_S17_0.00075F.txt', 'Notebook_1/logical_operators_S17_0.00075F.txt'],
        "[[17,1,5]]_0.0005": ['Notebook_1/syndromes_S17_0.0005F.txt', 'Notebook_1/logical_operators_S17_0.0005F.txt'],
        "[[20,2,6]]_0.01": ['Notebook_1/syndromes_D20_0.1_0.01F.txt', 'Notebook_1/logical_operators_D20_0.1_0.01F.txt', 'Notebook_1/logical_operators_D20_0.1_2_0.01F.txt'],  
        "[[20,2,6]]_0.005": ['Notebook_1/syndromes_D20_0.1_0.005F.txt', 'Notebook_1/logical_operators_D20_0.1_0.005F.txt', 'Notebook_1/logical_operators_D20_0.1_2_0.005F.txt'],
        "[[20,2,6]]_0.0025": ['Notebook_1/syndromes_D20_0.1_0.0025F.txt', 'Notebook_1/logical_operators_D20_0.1_0.0025F.txt', 'Notebook_1/logical_operators_D20_0.1_2_0.0025F.txt'],
        "[[20,2,6]]_0.001": ['Notebook_1/syndromes_D20_0.1_0.001F.txt', 'Notebook_1/logical_operators_D20_0.1_0.001F.txt', 'Notebook_1/logical_operators_D20_0.1_2_0.001F.txt'],
        "[[20,2,6]]_0.00075": ['Notebook_1/syndromes_D20_0.1_0.00075F.txt', 'Notebook_1/logical_operators_D20_0.1_0.00075F.txt', 'Notebook_1/logical_operators_D20_0.1_2_0.00075F.txt'],
        "[[20,2,6]]_0.0005": ['Notebook_1/Notebook_1/syndromes_D20_0.1_0.0005F.txt', 'Notebook_1/logical_operators_D20_0.1_0.0005F.txt', 'Notebook_1/logical_operators_D20_0.1_2_0.0005F.txt'],
        "[[23,1,7]]_0.01": ['Notebook_1/syndromes_G23_0.01F.txt', 'Notebook_1/logical_operators_G23_0.01F.txt'],  
        "[[23,1,7]]_0.005": ['Notebook_1/syndromes_G23_0.005F.txt', 'Notebook_1/logical_operators_G23_0.005F.txt'],
        "[[23,1,7]]_0.0025": ['Notebook_1/syndromes_G23_0.0025F.txt', 'Notebook_1/logical_operators_G23_0.0025F.txt'],
        "[[23,1,7]]_0.001": ['Notebook_1/syndromes_G23_0.001F.txt', 'Notebook_1/logical_operators_G23_0.001F.txt'],
        "[[23,1,7]]_0.00075": ['Notebook_1/syndromes_G23_0.00075F.txt', 'Notebook_1/logical_operators_G23_0.00075F.txt'],
        "[[23,1,7]]_0.0005": ['Notebook_1/syndromes_G23_0.0005F.txt', 'Notebook_1/logical_operators_G23_0.0005F.txt'],
        "[[49,1,5]]_0.01": ['Notebook_1/syndromes_49+_0.01F.txt', 'Notebook_1/logical_operators_49+_0.01F.txt'],  
        "[[49,1,5]]_0.005": ['Notebook_1/syndromes_49+_0.005F.txt', 'Notebook_1/logical_operators_49+_0.005F.txt'],
        "[[49,1,5]]_0.0025": ['Notebook_1/syndromes_49+_0.0025F.txt', 'lNotebook_1/ogical_operators_49+_0.0025F.txt'],
        "[[49,1,5]]_0.001": ['Notebook_1/syndromes_49+_0.001F.txt', 'Notebook_1/logical_operators_49+_0.001F.txt'],
        "[[49,1,5]]_0.00075": ['Notebook_1/syndromes_49+_0.00075F.txt', 'lNotebook_1/ogical_operators_49+_0.00075F.txt'],
        "[[49,1,5]]_0.0005": ['Notebook_1/syndromes_49+_0.0005F.txt', 'Notebook_1/logical_operators_49+_0.0005F.txt'],
        "[[49,1,9]]_0.01": ['Notebook_1/syndromes_49_0.01F.txt', 'lNotebook_1/ogical_operators_49_0.01F.txt'],  
        "[[49,1,9]]_0.005": ['Notebook_1/syndromes_49_0.005F.txt', 'Notebook_1/logical_operators_49_0.005F.txt'],
        "[[49,1,9]]_0.0025": ['Notebook_1/syndromes_49_0.0025F.txt', 'Notebook_1/logical_operators_49_0.0025F.txt'],
        "[[49,1,9]]_0.001": ['Notebook_1/syndromes_49_0.001F.txt', 'Notebook_1/logical_operators_49_0.001F.txt'],
        "[[49,1,9]]_0.00075": ['Notebook_1/syndromes_49_0.00075F.txt', 'Notebook_1/logical_operators_49_0.00075F.txt'],
        "[[49,1,9]]_0.0005": ['Notebook_1/syndromes_49_0.0005F.txt', 'Notebook_1/logical_operators_49_0.0005F.txt'],
    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Displaying string from file: {media_value}")
        # Read and display the string from the file
        for file_path in media_value:
            try:
                with open(file_path, 'r') as f:
                    print(f"Contents of {file_path}:\n{f.read()}\n")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    else:
        print("Invalid media key! Please try again.")

    return


def evaluate_lUTSteane(media_key):

    # Sample second dictionary with possible image or string values
    media_dict = {
        "[[7,1,3]]_0.1": ['Notebook_1/syndromes_STE2_S7_0.01F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.01F2.txt'],  
        "[[7,1,3]]_0.05": ['Notebook_1/syndromes_STE2_S7_0.005F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.005F2.txt'],
        "[[7,1,3]]_0.025": ['Notebook_1/syndromes_STE2_S7_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.0025F2.txt'],
        "[[7,1,3]]_0.01": ['Notebook_1/syndromes_STE2_S7_0.001F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.001F2.txt'],
        "[[7,1,3]]_0.0075": ['Notebook_1/syndromes_STE2_S7_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.00075F2.txt'],
        "[[7,1,3]]_0.005": ['Notebook_1/syndromes_STE2_S7_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.0005F2.txt'],
        "[[7,1,3]]_0.0025": ['Notebook_1/syndromes_STE2_S7_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.00025F2.txt'],
        "[[7,1,3]]_0.001": ['Notebook_1/syndromes_STE2_S7_0.0001F2.txt', 'Notebook_1/logical_operators_STE2_S7_0.0001F2.txt'],

        "[[17,1,5]]_0.1": ['Notebook_1/syndromes_STE2_S17_0.01F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.01F2.txt'],  
        "[[17,1,5]]_0.05": ['Notebook_1/syndromes_STE2_S17_0.005F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.005F2.txt'],
        "[[17,1,5]]_0.025": ['Notebook_1/syndromes_STE2_S17_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.0025F2.txt'],
        "[[17,1,5]]_0.01": ['Notebook_1/syndromes_STE2_S17_0.001F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.001F2.txt'],
        "[[17,1,5]]_0.0075": ['Notebook_1/syndromes_STE2_S17_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.00075F2.txt'],
        "[[17,1,5]]_0.005": ['Notebook_1/syndromes_STE2_S17_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.0005F2.txt'],
        "[[17,1,5]]_0.0025": ['Notebook_1/syndromes_STE2_S17_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.00025F2.txt'],
        "[[17,1,5]]_0.001": ['Notebook_1/syndromes_STE2_S17_0.0001F2.txt', 'Notebook_1/logical_operators_STE2_S17_0.0001F2.txt'],

        "[[20,2,6]]_0.1": ['Notebook_1/syndromes_STE2_D20_0.01F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.01F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.01F2.txt'],  
        "[[20,2,6]]_0.05": ['Notebook_1/syndromes_STE2_D20_0.005F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.005F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.005F2.txt'],
        "[[20,2,6]]_0.025": ['Notebook_1/syndromes_STE2_D20_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.0025F2.txt'],
        "[[20,2,6]]_0.01": ['Notebook_1/syndromes_STE2_D20_0.001F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.001F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.001F2.txt'],
        "[[20,2,6]]_0.0075": ['Notebook_1/syndromes_STE2_D20_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.00075F2.txt'],
        "[[20,2,6]]_0.005": ['Notebook_1/syndromes_STE2_D20_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.0005F2.txt'],
        "[[20,2,6]]_0.0025": ['Notebook_1/syndromes_STE2_D20_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.00025F2.txt'],
        "[[20,2,6]]_0.001": ['Notebook_1/syndromes_STE2_D20_0.0001F2.txt', 'Notebook_1/logical_operators_STE2_D20_0.0001F2.txt', 'Notebook_1/logical_operators_STE2_D20_2_0.0001F2.txt'],

        "[[23,1,7]]_0.1": ['Notebook_1/syndromes_STE2_G23_0.01F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.01F2.txt'],  
        "[[23,1,7]]_0.05": ['Notebook_1/syndromes_STE2_G23_0.005F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.005F2.txt'],
        "[[23,1,7]]_0.025": ['Notebook_1/syndromes_STE2_G23_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.0025F2.txt'],
        "[[23,1,7]]_0.01": ['Notebook_1/syndromes_STE2_G23_0.001F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.001F2.txt'],
        "[[23,1,7]]_0.0075": ['Notebook_1/syndromes_STE2_G23_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.00075F2.txt'],
        "[[23,1,7]]_0.005": ['Notebook_1/syndromes_STE2_G23_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.0005F2.txt'],
        "[[23,1,7]]_0.0025": ['Notebook_1/syndromes_STE2_G23_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.00025F2.txt'],
        "[[23,1,7]]_0.001": ['Notebook_1/syndromes_STE2_G23_0.0001F2.txt', 'Notebook_1/logical_operators_STE2_G23_0.0001F2.txt'],

        "[[49,1,5]]_0.1": ['Notebook_1/syndromes_STE2_49+_0.01F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.01F2.txt'],  
        "[[49,1,5]]_0.05": ['Notebook_1/syndromes_STE2_49+_0.005F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.005F2.txt'],
        "[[49,1,5]]_0.025": ['Notebook_1/syndromes_STE2_49+_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.0025F2.txt'],
        "[[49,1,5]]_0.01": ['Notebook_1/syndromes_STE2_49+_0.001F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.001F2.txt'],
        "[[49,1,5]]_0.0075": ['Notebook_1/syndromes_STE2_49+_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.00075F2.txt'],
        "[[49,1,5]]_0.005": ['Notebook_1/syndromes_STE2_49+_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.0005F2txt'],
        "[[49,1,5]]_0.0025": ['Notebook_1/syndromes_STE2_49+_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_49+_0.00025F2.txt'],
        "[[49,1,5]]_0.001": ['Notebook_1/syndromes_STE2_49+_0.0001F2.txt', 'logical_operators_STE2_49+_0.0001F2.txt'],

        "[[49,1,9]]_0.1": ['Notebook_1/syndromes_STE2_49_0.01F2.txt', 'Notebook_1/logical_operators_STE2_49_0.01F2.txt'],  
        "[[49,1,9]]_0.05": ['Notebook_1/syndromes_STE2_49_0.005F2.txt', 'Notebook_1/logical_operators_STE2_49_0.005F2.txt'],
        "[[49,1,9]]_0.025": ['Notebook_1/syndromes_STE2_49_0.0025F2.txt', 'Notebook_1/logical_operators_STE2_49_0.0025F2.txt'],
        "[[49,1,9]]_0.01": ['Notebook_1/syndromes_STE2_49_0.001F2.txt', 'Notebook_1/logical_operators_STE2_49_0.001F2.txt'],
        "[[49,1,9]]_0.0075": ['Notebook_1/syndromes_STE2_49_0.00075F2.txt', 'Notebook_1/logical_operators_STE2_49_0.00075F2.txt'],
        "[[49,1,9]]_0.005": ['Notebook_1/syndromes_STE2_49_0.0005F2.txt', 'Notebook_1/logical_operators_STE2_49_0.0005F2txt'],
        "[[49,1,9]]_0.0025": ['Notebook_1/syndromes_STE2_49_0.00025F2.txt', 'Notebook_1/logical_operators_STE2_49_0.00025F2.txt'],
        "[[49,1,9]]_0.001": ['Notebook_1/syndromes_STE2_49_0.0001F2.txt', 'logical_operators_STE2_49_0.0001F2.txt'],
    }


    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Displaying string from file: {media_value}")
        # Read and display the string from the file
        for file_path in media_value:
            try:
                with open(file_path, 'r') as f:
                    print(f"Contents of {file_path}:\n{f.read()}\n")
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
    else:
        print("Invalid media key! Please try again.")

    return


def specific_error_rate(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {
        "[[7,1,3]]_0.01": 0.00281794,  
        "[[7,1,3]]_0.005": 0.0007098,
        "[[7,1,3]]_0.0025": 0.0001798,
        "[[7,1,3]]_0.001": 2.7828e-05,
        "[[7,1,3]]_0.00075": 1.57568e-05,
        "[[7,1,3]]_0.0005": 6.91568e-06,
        "[[17,1,5]]_0.01": 0.000969707,  
        "[[17,1,5]]_0.005": 0.000140883,
        "[[17,1,5]]_0.0025": 1.8695e-05,
        "[[17,1,5]]_0.001": 1.18384e-06,
        "[[17,1,5]]_0.00075": 5.01664e-07,
        "[[17,1,5]]_0.0005": 1.49896e-07,
        "[[20,2,6]]_0.01": 0.000349568,  
        "[[20,2,6]]_0.005": 2.54037e-05,
        "[[20,2,6]]_0.0025": 1.75522e-06,
        "[[20,2,6]]_0.001": 3.8847e-08,
        "[[20,2,6]]_0.00075": 1.215e-08,
        "[[20,2,6]]_0.0005": 2.37975e-09,
        "[[23,1,7]]_0.01": 0.00290191,  
        "[[23,1,7]]_0.005": 0.00023751,
        "[[23,1,7]]_0.0025": 1.457431e-5,
        "[[23,1,7]]_0.001": 3.6615e-07,
        "[[23,1,7]]_0.00075": 1.1315e-07,
        "[[23,1,7]]_0.0005": 2.3515e-08,
        "[[49,1,5]]_0.01": 0.0231411,  
        "[[49,1,5]]_0.005": 0.00429337, 
        "[[49,1,5]]_0.0025": 0.000601786,
        "[[49,1,5]]_0.001": 4.80312e-05,
        "[[49,1,5]]_0.00075": 2.20876e-05,
        "[[49,1,5]]_0.0005": 6.95011e-06,
        "[[49,1,9]]_0.01": 0.007181,  
        "[[49,1,9]]_0.005": 0.0005159,
        "[[49,1,9]]_0.0025": 3.3495e-05,
        "[[49,1,9]]_0.001": 3.80224e-07,
        "[[49,1,9]]_0.00075": 9.40634e-08,
        "[[49,1,9]]_0.0005": 1.4515e-08,
    }


    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")


    return


def specific_acceptance_rate(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {

        "[[7,1,3]]_0.01": 1 - 0.856088304226204,  
        "[[7,1,3]]_0.005": 1 - 0.924988,
        "[[7,1,3]]_0.0025": 1 - 0.965687,
        "[[7,1,3]]_0.001": 1 - 0.986393042554,
        "[[7,1,3]]_0.00075":  1 -  0.989512,
        "[[7,1,3]]_0.0005": 1 - 0.992996,
        "[[17,1,5]]_0.01": 1 - 0.405315,  
        "[[17,1,5]]_0.005": 1 - 0.6306409895979,
        "[[17,1,5]]_0.0025":  1 - 0.80753,
        "[[17,1,5]]_0.001": 1 - 0.9187338948,
        "[[17,1,5]]_0.00075": 1 -  0.937861,
        "[[17,1,5]]_0.0005":  1 - 0.95816,                 
        "[[20,2,6]]_0.01": 0.8533,  
        "[[20,2,6]]_0.005": 0.6200,
        "[[20,2,6]]_0.0025": 0.3844,
        "[[20,2,6]]_0.001": 0.1766 ,
        "[[20,2,6]]_0.00075": 0.1356 ,
        "[[20,2,6]]_0.0005": 0.0926 ,
        "[[23,1,7]]_0.01": 1 - 0.0355,  
        "[[23,1,7]]_0.005": 1 - 0.0464784,
        "[[23,1,7]]_0.0025": 1 - 0.20701,
        "[[23,1,7]]_0.001": 1 - 0.531728,
        "[[23,1,7]]_0.00075": 1 - 0.776686,
        "[[23,1,7]]_0.0005": 1 - 0.844654,                    
        "[[49,1,5]]_0.01": 0.9888,  
        "[[49,1,5]]_0.005": 0.9251,
        "[[49,1,5]]_0.0025": 0.7369,
        "[[49,1,5]]_0.001": 0.4154,
        "[[49,1,5]]_0.00075": 0.3321,
        "[[49,1,5]]_0.0005": 0.2368,
        "[[49,1,9]]_0.01": 1 - 0.00519401,  
        "[[49,1,9]]_0.005":  1 - 0.0464784,
        "[[49,1,9]]_0.0025": 1 - 0.20701,
        "[[49,1,9]]_0.001": 1 - 0.531728,
        "[[49,1,9]]_0.00075": 1 - 0.622555,
        "[[49,1,9]]_0.0005": 1 - 0.729074,
    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return


def specific_error_rateSteane(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {
        "[[7,1,3]]_0.1": 0.146424,  
        "[[7,1,3]]_0.05":  0.0504868,
        "[[7,1,3]]_0.025":  0.0147808,
        "[[7,1,3]]_0.01": 0.00261596,
        "[[7,1,3]]_0.0075": 0.00149119,
        "[[7,1,3]]_0.005": 0.000675191,
        "[[7,1,3]]_0.0025": 0.000170745 ,
        "[[7,1,3]]_0.001": 2.78701e-05,
        "[[17,1,5]]_0.1": 0.0821003,  
        "[[17,1,5]]_0.05":  0.0229001,
        "[[17,1,5]]_0.025": 0.00417977,
        "[[17,1,5]]_0.01": 0.00033358,
        "[[17,1,5]]_0.0075": 0.000150518,
        "[[17,1,5]]_0.005": 4.37044e-05,
        "[[17,1,5]]_0.0025": 5.94316e-06,
        "[[17,1,5]]_0.001": 3.97142e-07,
        "[[20,2,6]]_0.1": 0.0124551, 
        "[[20,2,6]]_0.05": 0.00193512,
        "[[20,2,6]]_0.025": 0.000250292,
        "[[20,2,6]]_0.01": 1.0603e-05,
        "[[20,2,6]]_0.0075": 3.10249e-06,
        "[[20,2,6]]_0.005": 6.46125e-07, 
        "[[20,2,6]]_0.0025": 2.45636e-08,
        "[[20,2,6]]_0.001": 7.23133e-10,
        "[[23,1,7]]_0.1": 0.0547054 ,  
        "[[23,1,7]]_0.05": 0.008622,
        "[[23,1,7]]_0.025": 0.0015027,
        "[[23,1,7]]_0.01": 9.36609e-05,
        "[[23,1,7]]_0.0075": 3.44e-05,
        "[[23,1,7]]_0.005": 8.7808e-06,
        "[[23,1,7]]_0.0025": 6.5335e-07,
        "[[23,1,7]]_0.001": 1.53346e-08,
        "[[49,1,9]]_0.1": 0.0168546,  
        "[[49,1,9]]_0.05": 0.00629503,
        "[[49,1,9]]_0.025": 0.00135498,
        "[[49,1,9]]_0.01": 3.97429e-05,
        "[[49,1,9]]_0.0075": 1.17561e-05 ,
        "[[49,1,9]]_0.005": 2.4783e-06 ,
        "[[49,1,9]]_0.0025": 8.82644e-08,
        "[[49,1,9]]_0.001": 9.02644e-10,
        "[[49,1,5]]_0.1": 0.03534,  
        "[[49,1,5]]_0.05":  0.01579,
        "[[49,1,5]]_0.025": 0.0065113,
        "[[49,1,5]]_0.01": 0.000774123,
        "[[49,1,5]]_0.0075": 0.000318144,
        "[[49,1,5]]_0.005":  8.67413e-05,
        "[[49,1,5]]_0.0025": 6.744332e-06,
        "[[49,1,5]]_0.001": 3.26256e-07,

    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")
               

    return


def specific_error_rateSteane_onlyX(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {
        "[[17,1,5]]_0.1": 0.10173,  
        "[[17,1,5]]_0.05": 0.0291679,
        "[[17,1,5]]_0.025": 0.00605577,
        "[[17,1,5]]_0.01": 0.000680683,
        "[[17,1,5]]_0.0075": 0.000348115,
        "[[17,1,5]]_0.005": 0.000135809,
        "[[17,1,5]]_0.0025": 2.8409e-05,
        "[[17,1,5]]_0.001": 4.1992e-06,

    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")


    return

def specific_error_rateNOSteane(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {

        "[[7,1,3]]_0.1": 0.179793,  
        "[[7,1,3]]_0.05": 0.0645194,
        "[[7,1,3]]_0.025": 0.0190806,
        "[[7,1,3]]_0.01": 0.00343583,
        "[[7,1,3]]_0.0075": 0.00201558,
        "[[7,1,3]]_0.005": 0.000915477,
        "[[7,1,3]]_0.0025": 0.000232181,
        "[[7,1,3]]_0.001": 3.83938e-05,
        "[[17,1,5]]_0.1": 0.191408,  
        "[[17,1,5]]_0.05":  0.047876,
        "[[17,1,5]]_0.025": 0.008334,
        "[[17,1,5]]_0.01":  0.000688,
        "[[17,1,5]]_0.0075": 0.000316,
        "[[17,1,5]]_0.005": 9.5e-05,
        "[[17,1,5]]_0.0025": 1.2e-05,
        "[[17,1,5]]_0.001": 8e-07,  
        "[[20,2,6]]_0.1": 0.0683431,
        "[[20,2,6]]_0.05": 0.00980682, 
        "[[20,2,6]]_0.025": 0.000969437, 
        "[[20,2,6]]_0.01": 3.27684e-05, 
        "[[20,2,6]]_0.0075":  1.10603e-05,
        "[[20,2,6]]_0.005": 2.15062e-06,
        "[[20,2,6]]_0.0025":  7.16692e-08,
        "[[20,2,6]]_0.001": 2.26692e-09, 
        "[[23,1,7]]_0.1": 0.223617,  
        "[[23,1,7]]_0.05": 0.040777,
        "[[23,1,7]]_0.025":  0.00550874,
        "[[23,1,7]]_0.01":  0.00025,
        "[[23,1,7]]_0.0075": 8.26e-05,
        "[[23,1,7]]_0.005":  1.96e-05,
        "[[23,1,7]]_0.0025": 1.47e-06,
        "[[23,1,7]]_0.001": 3.63346e-08,
        "[[49,1,9]]_0.1": 0.334597,
        "[[49,1,9]]_0.05": 0.0758927,
        "[[49,1,9]]_0.025":  0.00958927,
        "[[49,1,9]]_0.01": 0.000216343,
        "[[49,1,9]]_0.0075": 6.21921e-05,
        "[[49,1,9]]_0.005": 9.8584e-06,
        "[[49,1,9]]_0.0025": 3.29988e-07,
        "[[49,1,9]]_0.001": 3.2376e-09,
        "[[49,1,5]]_0.1": 0.325141,
        "[[49,1,5]]_0.05": 0.107752, 
        "[[49,1,5]]_0.025": 0.014319,
        "[[49,1,5]]_0.01": 0.00107451,
        "[[49,1,5]]_0.0075": 0.00039952,
        "[[49,1,5]]_0.005": 9.41486e-05,
        "[[49,1,5]]_0.0025": 6.81181e-06,
        "[[49,1,5]]_0.001": 1.75133e-07,
    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return

def specific_confidence(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {
        
        "[[7,1,3]]_0.01": [ 0.00277506835, 0.002845370],  
        "[[7,1,3]]_0.005":[ 0.0006877012, 0.00071251], 
        "[[7,1,3]]_0.0025": [ 0.0001746181, 0.000183491], 
        "[[7,1,3]]_0.001": [ 2.67357341377212e-05, 2.89482369169223e-05], 
        "[[7,1,3]]_0.00075": [ 1.53401103948066e-05 , 1.61708417279112e-05], 
        "[[7,1,3]]_0.0005": [ 6.64522069245727e-06, 7.19573159256552e-06], 
        "[[17,1,5]]_0.01": [0.000918782715423087 , 0.0010219591691446],   
        "[[17,1,5]]_0.005": [ 0.000126171999389300, 0.000155343264649644], 
        "[[17,1,5]]_0.0025": [ 1.53597867537069e-05, 2.27422329084859e-05], 
        "[[17,1,5]]_0.001": [ 7.67113436912570e-07, 1.82435689053836e-06], 
        "[[17,1,5]]_0.00075": [ 3.45806071290706e-07,7.27582778987056e-07], 
        "[[17,1,5]]_0.0005": [ 7.19522708201629e-08, 3.11873938851026e-07], 
        "[[20,2,6]]_0.01": [ 0.00032131775498760753, 0.0003803010606179507],   
        "[[20,2,6]]_0.005": [ 2.2014239365355248e-05, 2.931500953489083e-05], 
        "[[20,2,6]]_0.0025": [ 1.336851340774392e-06, 2.3045171524081675e-06], 
        "[[20,2,6]]_0.001": [2.2441448428746276e-08 , 6.724563237051604e-08], 
        "[[20,2,6]]_0.00075": [5.756157761663563e-09, 2.5646013376272712e-08 ], 
        "[[20,2,6]]_0.0005": [ 7.796983563918434e-10, 5.817422872208054e-09 ], 
        "[[23,1,7]]_0.01": [ 0.002609241479980, 0.003223054237],   
        "[[23,1,7]]_0.005": [0.000194953736683540, 0.000271344717769078], 
        "[[23,1,7]]_0.0025": [1.07878188106150e-05 , 1.96781779736436e-05], 
        "[[23,1,7]]_0.001": [ 1.80416047456506e-07,7.42483699849974e-07 ], 
        "[[23,1,7]]_0.00075": [2.87134338260145e-08 , 4.45492061490063e-07], 
        "[[23,1,7]]_0.0005": [4.08019664139825e-09 ,1.35464071327347e-07 ], 
        "[[49,1,5]]_0.01": [0.021554824047463148, 0.024841150358944613],  
        "[[49,1,5]]_0.005": [0.004060057699788913, 0.004540028535952966],
        "[[49,1,5]]_0.0025": [0.0005681726311057236, 0.0006373866839115679 ],
        "[[49,1,5]]_0.001": [4.2701142232975137e-05, 5.4026532262767024e-05], 
        "[[49,1,5]]_0.00075": [1.9074169864405745e-05, 2.5577094309434776e-05], 
        "[[49,1,5]]_0.0005": [5.640626684606442e-06, 8.563590010211958e-06], 
        "[[49,1,9]]_0.01": [0.005957659315474093, 0.008180638523754124],  
        "[[49,1,9]]_0.005": [0.00041234345496294397, 0.0005725893830442453],
        "[[49,1,9]]_0.0025": [ 2.5208025948805157e-05, 4.450640719378e-05],
        "[[49,1,9]]_0.001": [1.4785921735755804e-07, 9.777560030905905e-07 ], 
        "[[49,1,9]]_0.00075": [3.126972846383729e-08, 2.8900311219122464e-07], 
        "[[49,1,9]]_0.0005": [1.9156632185133218e-09, 1.0998029586060115e-07], 
    }



    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return


def specific_acceptance_confidence(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {
        
        # Wilson interval bounds (lower and upper) directly

        "[[7,1,3]]_0.01": [ 1 - 0.8558550736593439, 1 -  0.8563212207719434],  
        "[[7,1,3]]_0.005": [ 1 - 0.92486432784397, 1 - 0.9251114850765189],
        "[[7,1,3]]_0.0025": [ 1 -  0.9654767652488414, 1 - 0.9658959997162406],
        "[[7,1,3]]_0.001": [1 - 0.9863625321008772 , 1 - 0.9864235109338885],
        "[[7,1,3]]_0.00075":  [ 1 - 0.9894611458001257, 1 - 0.9895626113964873],
        "[[7,1,3]]_0.0005": [ 1 - 0.9929705870208103,1 - 0.9930213217509973 ],
        "[[17,1,5]]_0.01": [ 1 - 0.40450152009838264, 1 - 0.40612900014052106],  
        "[[17,1,5]]_0.005": [ 1 - 0.6300466082907697,1 - 0.631234974882957 ],
        "[[17,1,5]]_0.0025":  [1 - 0.8071947788949585 , 1 - 0.8078647770030276],
        "[[17,1,5]]_0.001": [ 1 - 0.9185880799766753, 1 - 0.9188795316213424],
        "[[17,1,5]]_0.00075": [1 - 0.9377909023157883, 1 - 0.9379310239254447],
        "[[17,1,5]]_0.0005":  [1 - 0.958114927109849 , 1 - 0.9582210085735163],
        "[[20,2,6]]_0.01": [ 0.85384382976319,  0.852728414716509],  
        "[[20,2,6]]_0.005": [ 0.620395577073227, 0.6196942976297044],
        "[[20,2,6]]_0.0025": [ 0.38458603470796987, 0.3842339955601855],
        "[[20,2,6]]_0.001": [0.17659676024625462 , 0.17651324751195005],
        "[[20,2,6]]_0.00075": [ 0.13561985423745182, 0.13556215093873852],
        "[[20,2,6]]_0.0005": [0.09259901489599444 ,0.09257098700876952],
        "[[23,1,7]]_0.01": [ 1 - 0.034460349095792805,1 - 0.03656982865663745 ],  
        "[[23,1,7]]_0.005": [ 1 -  0.1828227324391475, 1 - 0.18476725262475616],
        "[[23,1,7]]_0.0025": [1 -  0.43004489470670587 , 1 - 0.43118528930723005],
        "[[23,1,7]]_0.001": [ 1 - 0.7095156440468829, 1 - 0.7099122758843591],
        "[[23,1,7]]_0.00075": [ 1 - 0.7764785300972898,1 - 0.7768933326633822 ],
        "[[23,1,7]]_0.0005": [1 - 0.8445437844201864 ,1 - 0.8447641518020925 ],
        "[[49,1,5]]_0.01": [ 1 - 0.010104004743474462, 1 -  0.01240541956497396],  
        "[[49,1,5]]_0.005": [ 1 - 0.07391584921357966, 1 - 0.07584719668496076],
        "[[49,1,5]]_0.0025": [1 - 0.262515346596527 , 1 - 0.26375759598470583],
        "[[49,1,5]]_0.001": [ 1 - 0.5841659782203685, 1 - 0.5849699092469542],
        "[[49,1,5]]_0.00075": [ 1 - 0.6675489517302959, 1 - 0.6681988884250485],
        "[[49,1,5]]_0.0005": [1 - 0.7629865326022468 , 1 - 0.7634553073589007],
        "[[49,1,9]]_0.01": [ 1 - 0.0056493901302416315,1 - 0.0074044823192078195 ],  
        "[[49,1,9]]_0.005":  [1 - 0.05635419987158454 ,  1 - 0.05673099022729725],
        "[[49,1,9]]_0.0025": [1 - 0.23132718844218794 , 1 - 0.23251787835264678],
        "[[49,1,9]]_0.001": [ 1 - 0.5554030161977751 , 1 - 0.5559509499505063 ],
        "[[49,1,9]]_0.00075":[1 - 0.6432144600416692 , 1 - 0.6438754032790295 ],
        "[[49,1,9]]_0.0005": [1 - 0.7450907104295721 , 1 - 0.7455711404087282],
    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return

def specific_confidenceSteane(media_key):
    
    # Sample second dictionary with possible image or string values

    media_dict = {

        "[[7,1,3]]_0.1": [0.14602013679387657, 0.1468287881606927],  
        "[[7,1,3]]_0.05":[0.05027589291597441, 0.050698544607754484 ], 
        "[[7,1,3]]_0.025": [0.014690138785003828,0.014872012291720554 ], 
        "[[7,1,3]]_0.01": [0.0025901678827820033, 0.0026420082670988265], 
        "[[7,1,3]]_0.0075": [0.0014791194476398315,  0.001503358907414125], 
        "[[7,1,3]]_0.005": [0.0006704456406294661,  0.0006799699237821138], 
        "[[7,1,3]]_0.0025": [ 0.00016904050621302332,0.00017246667782163752 ], 
        "[[7,1,3]]_0.001": [2.7433241813187563e-05, 2.8313914698659092e-05 ], 
        "[[17,1,5]]_0.1": [0.10135674171107921, 0.10210447667768584],   
        "[[17,1,5]]_0.05": [0.02888432348907053, 0.029454176127959218], 
        "[[17,1,5]]_0.025": [0.005940689440862454,0.006173066007939103  ], 
        "[[17,1,5]]_0.01": [0.0006521805617143529, 0.0007104302031767845], 
        "[[17,1,5]]_0.0075": [ 0.00033754393071317926, 0.0003590170110188455], 
        "[[17,1,5]]_0.005": [0.0001310099633898133, 0.00014078380575787807 ], 
        "[[17,1,5]]_0.0025": [2.6987956796389192e-05,  2.990486559240187e-05], 
        "[[17,1,5]]_0.001": [3.7167367068617394e-06, 4.744290738461329e-06 ],
        "[[20,2,6]]_0.1": [0.012304373951267232, 0.012607648843520794 ],   
        "[[20,2,6]]_0.05": [0.0018764470343294204, 0.0019956238907931053], 
        "[[20,2,6]]_0.025": [0.0002311131547729374,0.00027106196355759825 ], 
        "[[20,2,6]]_0.01": [8.950466400472324e-06,1.256063870507606e-05 ], 
        "[[20,2,6]]_0.0075": [2.499721813978725e-06, 3.8506055942830875e-06 ], 
        "[[20,2,6]]_0.005": [4.880750350675206e-07, 8.553551488259222e-07], 
        "[[20,2,6]]_0.0025": [8.992704127726793e-09, 6.709554991719916e-08 ], 
        "[[20,2,6]]_0.001": [1.4365035910263184e-10, 3.6402368760735403e-09], 
        "[[23,1,7]]_0.1": [0.05442419034209208, 0.054987978170793296],   
        "[[23,1,7]]_0.05": [0.008508595777963823,  0.008736902376676767], 
        "[[23,1,7]]_0.025": [0.0014704696775966204, 0.0015356356726327883], 
        "[[23,1,7]]_0.01": [ 8.829733207247016e-05, 9.93502422390717e-05 ], 
        "[[23,1,7]]_0.0075": [3.175233879428129e-05, 3.726842757639825e-05], 
        "[[23,1,7]]_0.005": [7.626779138351767e-06, 1.0109435946400784e-05], 
        "[[23,1,7]]_0.0075": [4.866758229357083e-07, 8.77105822842842e-07], 
        "[[23,1,7]]_0.005": [5.954686335690723e-09,3.948989760823268e-08 ],        
        "[[49,1,9]]_0.1": [0.016660238171606737, 0.017051189976158954],  
        "[[49,1,9]]_0.05": [0.0061758495137662775, 0.006416495561683818],
        "[[49,1,9]]_0.025": [0.0013161559043594726, 0.0013949477329612044 ],
        "[[49,1,9]]_0.01": [3.489354880938391e-05, 4.5266162078064284e-05 ],
        "[[49,1,9]]_0.0075": [9.86035507544256e-06,1.401631440040057e-05 ],
        "[[49,1,9]]_0.005": [1.8499527296422153e-06, 3.320068389182611e-06],
        "[[49,1,9]]_0.0025": [3.2851370141522145e-08, 2.3714699099653862e-07],
        "[[49,1,9]]_0.001": [4.027140626628208e-10, 2.023187829208045e-09 ],
        "[[49,1,5]]_0.1": [ 0.046019609595045884, 0.04660213329711036],  
        "[[49,1,5]]_0.05": [ 0.015618196958386309, 0.015963662258865967],
        "[[49,1,5]]_0.025": [ 0.006402021877853166, 0.006622430992304902],
        "[[49,1,5]]_0.01": [ 0.0007504326810330548, 0.000798560598120981 ],
        "[[49,1,5]]_0.0075": [ 0.00030661034159529927, 0.0003301113729000419],
        "[[49,1,5]]_0.005": [ 8.148372602425048e-05, 9.233807706370555e-05],
        "[[49,1,5]]_0.0025": [ 5.900389293939858e-06, 7.708984334689172e-06],
        "[[49,1,5]]_0.001": [ 2.31871797185719e-07, 4.590595955974182e-07],
        
    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return


def specific_confidenceSteane_onlyX(media_key):
    
    # Sample second dictionary with possible image or string values
    media_dict = {
        "[[17,1,5]]_0.1": [0.10135674171107921, 0.10210447667768584],   
        "[[17,1,5]]_0.05": [0.02888432348907053, 0.029454176127959218 ], 
        "[[17,1,5]]_0.025": [0.005940689440862454, 0.006173066007939103 ], 
        "[[17,1,5]]_0.01": [0.0006521805617143529, 0.0007104302031767845], 
        "[[17,1,5]]_0.0075": [0.00033754393071317926,  0.0003590170110188455], 
        "[[17,1,5]]_0.005": [0.0001310099633898133, 0.00014078380575787807 ], 
        "[[17,1,5]]_0.0025": [ 2.6987956796389192e-05, 2.990486559240187e-05], 
        "[[17,1,5]]_0.001": [3.7167367068617394e-06, 4.744290738461329e-06 ],

    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return


def specific_confidenceNOSteane(media_key):
    
    # Sample second dictionary with possible image or string values
    
    media_dict = {
        "[[7,1,3]]_0.1": [ 0.17938097846437123, 0.18020576008950412],  
        "[[7,1,3]]_0.05":[ 0.0642988682857638,0.06474063575868753 ], 
        "[[7,1,3]]_0.025": [ 0.018984605671050755, 0.01917707022908433 ], 
        "[[7,1,3]]_0.01": [ 0.0034129270156476386, 0.003458886145005701 ], 
        "[[7,1,3]]_0.0075": [0.0020034660319734237, 0.0020277670663723588], 
        "[[7,1,3]]_0.005": [ 0.0009104703846852536, 0.0009205111209893857], 
        "[[7,1,3]]_0.0025": [ 0.0002303138825233339, 0.00023406325035303093], 
        "[[7,1,3]]_0.001": [3.791454827366226e-05 , 3.8879109382237024e-05], 
        "[[17,1,5]]_0.1": [ 0.19094747389541494 , 0.1918693733942965],   
        "[[17,1,5]]_0.05": [ 0.04754028478770563, 0.048213965925311374], 
        "[[17,1,5]]_0.025": [ 0.008212324109993426, 0.008457463297843455], 
        "[[17,1,5]]_0.01": [ 0.0006617413863390875,0.0007152998380262084], 
        "[[17,1,5]]_0.0075": [ 0.0003085680923456286, 0.00032361084829391374 ], 
        "[[17,1,5]]_0.005": [ 9.165279404179448e-05, 9.846943555864477e-05], 
        "[[17,1,5]]_0.0025": [ 1.122596679947231e-05, 1.2827402297451522e-05], 
        "[[17,1,5]]_0.001": [ 7.085431415738879e-07, 9.032618550553704e-07],
        "[[20,2,6]]_0.1": [ 0.06799890373335148, 0.06868891011174778],   
        "[[20,2,6]]_0.05": [0.00967411951139456 , 0.009941322476748338], 
        "[[20,2,6]]_0.025": [ 0.0009309580580817988, 0.0010095047706129982], 
        "[[20,2,6]]_0.01": [ 2.975535567779459e-05, 3.6086535901913564e-05], 
        "[[20,2,6]]_0.0075": [9.862988518694302e-06, 1.240295657625904e-05], 
        "[[20,2,6]]_0.005": [ 1.8434580330292651e-06, 2.5089619968633174e-06 ], 
        "[[20,2,6]]_0.0025": [ 3.9171451474679185e-08, 1.3112800003021338e-07], 
        "[[20,2,6]]_0.001": [8.540027860610594e-10, 6.017458441897534e-09],
        "[[23,1,7]]_0.1": [0.22311517557546404 ,  0.22411962750402328],   
        "[[23,1,7]]_0.05": [ 0.04054406935236732, 0.04101121166176784], 
        "[[23,1,7]]_0.025": [  0.005448495337670505, 0.005569647064293393], 
        "[[23,1,7]]_0.01": [  0.00024184420184556485,0.0002584307679441571 ], 
        "[[23,1,7]]_0.0075": [  7.948701881105656e-05, 8.583488562271807e-05], 
        "[[23,1,7]]_0.005": [ 1.798077475671975e-05, 2.136503844689095e-05], 
        "[[23,1,7]]_0.0075": [ 1.3889558420753045e-06, 1.5557729945919114e-06], 
        "[[23,1,7]]_0.005": [ 2.953832187079956e-08, 4.469458897733407e-08],       
        "[[49,1,9]]_0.1": [ 0.3339265940548294, 0.33526807440469],  
        "[[49,1,9]]_0.05": [ 0.07550697672824014, 0.07628023113586452], 
        "[[49,1,9]]_0.025": [ 0.009486646333522664, 0.009692992954462435],
        "[[49,1,9]]_0.01": [ 0.00020477092317358188, 0.00022856889205269748 ],
        "[[49,1,9]]_0.0075": [ 5.8735812445206664e-05, 6.58517581469049e-05],
        "[[49,1,9]]_0.005": [ 8.759411176692431e-06, 1.1095270583698603e-05],
        "[[49,1,9]]_0.0025": [ 2.4588419590535037e-07, 4.428591947949896e-07],
        "[[49,1,9]]_0.001": [1.2772960572870225e-09 , 8.206440213029587e-09],
        "[[49,1,5]]_0.1": [ 0.3244921290012281, 0.32579054273581615 ],  
        "[[49,1,5]]_0.05": [ 0.10732312827448454, 0.10818237783701415], 
        "[[49,1,5]]_0.025": [ 0.014157132079185165, 0.014482691475905845],
        "[[49,1,5]]_0.01": [  0.0010465377035674714, 0.0011032291259445216],
        "[[49,1,5]]_0.0075": [ 0.0003865699817771209, 0.00041290366208537584],
        "[[49,1,5]]_0.005": [ 8.866428059431446e-05, 9.997211746761158e-05 ],
        "[[49,1,5]]_0.0025": [ 5.963374814948125e-06, 7.780954797390194e-06],
        "[[49,1,5]]_0.001": [1.1009592548267392e-07, 2.785894789125788e-07],
        
    }

    # Check if the key exists in the media dictionary
    if media_key in media_dict:
        media_value = media_dict[media_key]
        
        print(f"Media Information: {media_value}")
    else:
        print("Invalid media key! Please try again.")

    return
