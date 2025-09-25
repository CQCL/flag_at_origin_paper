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
import stim  # make sure stim is installed
from pytket.extensions.cirq import tk_to_cirq
from pytket.extensions.qiskit import tk_to_qiskit
from pytket.passes import RemoveBarriers
import stimcirq
from typing import Tuple


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


def stabilizers_to_stim_strings_numbered(code_name: tuple[int,int,int]):
    """
    Returns a list of strings representing the stabilizers and logical operators
    of a code in a numbered Stim-style format.

    Labels:
        - X-type stabilizers: X1, X2, ...
        - Z-type stabilizers: Z1, Z2, ...
        - X-type logicals: LX1, LX2, ...
        - Z-type logicals: LZ1, LZ2, ...
    """
    code_stabilisers, logical_operators = get_stabilisers_and_logicals(code_name)

    # Determine total number of qubits in the code
    n_qubits = 0
    for stab in code_stabilisers + logical_operators:
        if stab['paulis']:
            n_qubits = max(n_qubits, max(stab['paulis'].keys()) + 1)

    stim_strings = []
    x_count = 1
    z_count = 1
    lx_count = 1
    lz_count = 1

    # Process stabilizers
    for stab in code_stabilisers:
        paulis = stab['paulis']
        line = ['I'] * n_qubits
        for q, p in paulis.items():
            line[q] = p
        if all(p == 'X' for p in paulis.values()):
            label = f"X{x_count}"
            x_count += 1
        elif all(p == 'Z' for p in paulis.values()):
            label = f"Z{z_count}"
            z_count += 1
        else:
            label = "Stab"  # mixed
        stim_strings.append(f"{label}: " + ' '.join(line))

    # Process logical operators
    for log in logical_operators:
        paulis = log['paulis']
        line = ['I'] * n_qubits
        for q, p in paulis.items():
            line[q] = p
        if all(p == 'X' for p in paulis.values()):
            label = f"LX{lx_count}"
            lx_count += 1
        elif all(p == 'Z' for p in paulis.values()):
            label = f"LZ{lz_count}"
            lz_count += 1
        else:
            label = "LStab"
        stim_strings.append(f"{label}: " + ' '.join(line))

    return stim_strings


def choose_code_stim(user_key):
    """
    Retrieve circuit information based on the provided key,
    save the pytket circuit to HTML, and return both
    Qiskit and Stim versions of the circuit.
    """
    folder_path = os.path.dirname(os.path.abspath(__file__)) + '/'

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

    if user_key not in circuit_info_dict:
        print("Invalid key! Please try again.")
        return None, None, None

    circuit_data = circuit_info_dict[user_key]
    print("\nCircuit Information for key:", user_key)
    print(circuit_data)

    # Load pytket circuit from JSON
    circuit_filename = circuit_data["entire_circuit"]
    json_path = os.path.join(folder_path, "Notebook_1", circuit_filename)
    with open(json_path, 'r') as f:
        circuit_json = json.load(f)

    pytket_circ = Circuit.from_dict(circuit_json)
    print("Pytket circuit loaded.")

    # Save pytket circuit to HTML
    save_circuit(pytket_circ, folder_path, filename='ENTIRE_ft_circ_found.html')
    full_file_url = f'file://{os.path.abspath(os.path.join(folder_path, "ENTIRE_ft_circ_found.html"))}'
    webbrowser.open(full_file_url)

    print("Number of CNOTs:", circuit_data["number_CNOTs"])
    print("Number of Sim Qubits:", circuit_data["number_simQUBITS"])
    print("Number of Ancillas:", circuit_data["number_ANC"])

    # ------------------ Qiskit version ------------------
    qiskit_circ = tk_to_qiskit(pytket_circ)
    # print("\nQiskit version of the circuit:")
    # print(qiskit_circ)

    # ------------------ Stim version ------------------
    # Flatten qubits to a single linear register for Cirq
    flat_qubits = list(pytket_circ.qubits)
    reindex_map = {qb: Qubit(i) for i, qb in enumerate(flat_qubits)}
    RemoveBarriers().apply(pytket_circ)
    pytket_flat = pytket_circ.copy()
    pytket_flat.rename_units(reindex_map)

    cirq_circ = tk_to_cirq(pytket_flat)
    stim_circ = stimcirq.cirq_circuit_to_stim_circuit(cirq_circ)
    # print("\nStim version of the circuit:")
    # print(stim_circ)

    return pytket_circ, qiskit_circ, stim_circ


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


def get_stabilisers_and_logicals(code_name: tuple[int, int, int]) -> Tuple[dict, dict]:
    if code_name == (7, 1, 3):
        code_stabilisers = [{'name': 'AZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}},
                            {'name': 'BZ', 'phase': +1, 'paulis': {1: 'Z', 2: 'Z', 4: 'Z', 5: 'Z'}},
                            {'name': 'CZ', 'phase': +1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z'}},
                            {'name': 'AX', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}},
                            {'name': 'BX', 'phase': +1, 'paulis': {1: 'X', 2: 'X', 4: 'X', 5: 'X'}},
                            {'name': 'CX', 'phase': +1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X'}}]
        logical_operators = [{'name': 'LZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 4: 'Z'}},
                             {'name': 'LX', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 4: 'X'}},
                            ]
        return code_stabilisers, logical_operators
    if code_name == (15,1,3):
        code_stabilisers = [{'name': 'AZ', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}},
                            {'name': 'BZ', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 4: 'Z', 5: 'Z'}},
                            {'name': 'CZ', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z'}},
                            {'name': 'DZ', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 6: 'Z', 7: 'Z'}},
                            {'name': 'EZ', 'phase': 1, 'paulis': {1: 'Z', 4: 'Z', 8: 'Z', 12: 'Z'}},
                            {'name': 'FZ', 'phase': 1, 'paulis': {2: 'Z', 5: 'Z', 9: 'Z', 11: 'Z'}},
                            {'name': 'GZ', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 9: 'Z', 10: 'Z'}},
                            {'name': 'HZ', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 11: 'Z', 12: 'Z'}},
                            {'name': 'IZ', 'phase': 1, 'paulis': {5: 'Z', 6: 'Z', 11: 'Z', 13: 'Z'}},
                            {'name': 'JZ', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 13: 'Z', 14: 'Z'}},
                            {'name': 'AX', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 4: 'X', 5: 'X', 6: 'X', 7: 'X'}},
                            {'name': 'BX', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 4: 'X', 5: 'X', 8: 'X', 9: 'X', 11: 'X', 12: 'X'}},
                            {'name': 'CX', 'phase': 1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 11: 'X', 13: 'X'}},
                            {'name': 'DX', 'phase': 1, 'paulis': {4: 'X', 5: 'X', 6: 'X', 7: 'X', 11: 'X', 12: 'X', 13: 'X', 14: 'X'}}]
        logical_operators = [{'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 8: 'X', 9: 'X', 10: 'X'}},
                            {'name': 'LZ', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 8: 'Z'}}
                            ]
        return code_stabilisers, logical_operators
    if code_name == (16, 2, 4):  # a [[4, 2, 2]] code with qubits t, 1, 2, b encoded on top of a 4-qubit surface code
        code_stabilisers = [{'name': 'tX', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}},
                            {'name': '1X', 'phase': +1, 'paulis': {4: 'X', 5: 'X', 6: 'X', 7: 'X'}},
                            {'name': '2X', 'phase': +1, 'paulis': {8: 'X', 9: 'X', 10: 'X', 11: 'X'}},
                            {'name': 'bX', 'phase': +1, 'paulis': {12: 'X', 13: 'X', 14: 'X', 15: 'X'}},
                            {'name': 'SX', 'phase': +1, 'paulis': dict(zip([0, 1, 4, 5, 8, 9, 12, 13], ['X'] * 8))},
                            {'name': 'tAZ', 'phase': +1, 'paulis': dict(zip([0, 1], ['Z'] * 2))},
                            {'name': 'tBZ', 'phase': +1, 'paulis': dict(zip([2, 3], ['Z'] * 2))},
                            {'name': '1AZ', 'phase': +1, 'paulis': dict(zip([4, 5], ['Z'] * 2))},
                            {'name': '1BZ', 'phase': +1, 'paulis': dict(zip([6, 7], ['Z'] * 2))},
                            {'name': '2AZ', 'phase': +1, 'paulis': dict(zip([8, 9], ['Z'] * 2))},
                            {'name': '2BZ', 'phase': +1, 'paulis': dict(zip([10, 11], ['Z'] * 2))},
                            {'name': 'bAZ', 'phase': +1, 'paulis': dict(zip([12, 13], ['Z'] * 2))},
                            {'name': 'bBZ', 'phase': +1, 'paulis': dict(zip([14, 15], ['Z'] * 2))},
                            {'name': 'SZ', 'phase': +1, 'paulis': dict(zip([1, 2, 5, 6, 9, 10, 13, 14], ['Z'] * 8))}]
        logical_operators = [{'name': 'LX1', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 4: 'X', 5: 'X'}},
                             {'name': 'LX2', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 8: 'X', 9: 'X'}},
                             {'name': 'LZ1', 'phase': +1, 'paulis': {5: 'Z', 6: 'Z', 13: 'Z', 14: 'Z'}},
                             {'name': 'LZ2', 'phase': +1, 'paulis': {9: 'Z', 10: 'Z', 13: 'Z', 14: 'Z'}}]
        return code_stabilisers, logical_operators
    if code_name == (17, 1, 5): # color code
        code_stabilisers = [{'name': 'AZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}},
                            {'name': 'BZ', 'phase': +1, 'paulis': {1: 'Z', 3: 'Z', 6: 'Z', 7: 'Z'}},
                            {'name': 'CZ', 'phase': +1, 'paulis': {4: 'Z', 8: 'Z', 12: 'Z', 13: 'Z'}},
                            {'name': 'DZ', 'phase': +1, 'paulis': {4: 'Z', 5: 'Z', 8: 'Z', 9: 'Z'}},
                            {'name': 'EZ', 'phase': +1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 9: 'Z', 10: 'Z', 14: 'Z', 15: 'Z' }},
                            {'name': 'FZ', 'phase': +1, 'paulis': {6: 'Z', 7: 'Z', 10: 'Z', 11: 'Z'}},
                            {'name': 'GZ', 'phase': +1, 'paulis': {8: 'Z', 9: 'Z', 13: 'Z', 14: 'Z'}},
                            {'name': 'HZ', 'phase': +1, 'paulis': {10: 'Z', 11: 'Z', 15: 'Z', 16: 'Z'}},
                            {'name': 'AX', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}},
                            {'name': 'BX', 'phase': +1, 'paulis': {1: 'X', 3: 'X', 6: 'X', 7: 'X'}},
                            {'name': 'CX', 'phase': +1, 'paulis': {4: 'X', 8: 'X', 12: 'X', 13: 'X'}},
                            {'name': 'DX', 'phase': +1, 'paulis': {4: 'X', 5: 'X', 8: 'X', 9: 'X'}},
                            {'name': 'EX', 'phase': +1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 14: 'X', 15: 'X' }},
                            {'name': 'FX', 'phase': +1, 'paulis': {6: 'X', 7: 'X', 10: 'X', 11: 'X'}},
                            {'name': 'GX', 'phase': +1, 'paulis': {8: 'X', 9: 'X', 13: 'X', 14: 'X'}},
                            {'name': 'HX', 'phase': +1, 'paulis': {10: 'X', 11: 'X', 15: 'X', 16: 'X'}}]
        logical_operators = [{'name': 'LZ', 'phase': +1, 'paulis': {12: 'Z', 13: 'Z', 14: 'Z', 15: 'Z', 16: 'Z'}},
                             {'name': 'LX', 'phase': +1, 'paulis': {12: 'X', 13: 'X', 14: 'X', 15: 'X', 16: 'X'}},
                            ]
        return code_stabilisers, logical_operators
    if code_name == (23, 1, 7): # Golay code
        code_stabilisers = [{'name': 'AZ', 'phase': +1, 'paulis': {1: 'Z', 4: 'Z', 7: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 11: 'Z', 22: 'Z'}},
                            {'name': 'BZ', 'phase': +1, 'paulis': {0: 'Z', 3: 'Z', 6: 'Z', 7: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 21: 'Z'}},
                            {'name': 'CZ', 'phase': +1, 'paulis': {1: 'Z', 2: 'Z', 4: 'Z', 5: 'Z', 6: 'Z', 10: 'Z', 11: 'Z', 20: 'Z'}},
                            {'name': 'DZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 3: 'Z', 4: 'Z', 5: 'Z', 9: 'Z', 10: 'Z', 19: 'Z'}},
                            {'name': 'EZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z', 7: 'Z', 10: 'Z', 11: 'Z', 18: 'Z' }},
                            {'name': 'FZ', 'phase': +1, 'paulis': {0: 'Z', 2: 'Z', 4: 'Z', 6: 'Z', 7: 'Z', 8: 'Z', 11: 'Z', 17: 'Z'}},
                            {'name': 'GZ', 'phase': +1, 'paulis': {3: 'Z', 4: 'Z', 5: 'Z', 6: 'Z', 8: 'Z', 9: 'Z', 11: 'Z', 16: 'Z'}},
                            {'name': 'HZ', 'phase': +1, 'paulis': {2: 'Z', 3: 'Z', 4: 'Z', 5: 'Z', 7: 'Z', 8: 'Z', 10: 'Z', 15: 'Z'}},
                            {'name': 'IZ', 'phase': +1, 'paulis': {1: 'Z', 2: 'Z', 3: 'Z', 4: 'Z', 6: 'Z', 7: 'Z', 9: 'Z', 14: 'Z'}},
                            {'name': 'LZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 8: 'Z', 13: 'Z'}},
                            {'name': 'MZ', 'phase': +1, 'paulis': {0: 'Z', 2: 'Z', 5: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 11: 'Z', 12: 'Z'}},
                            {'name': 'AZ', 'phase': +1, 'paulis': {1: 'X', 4: 'X', 7: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 22: 'X'}},
                            {'name': 'BZ', 'phase': +1, 'paulis': {0: 'X', 3: 'X', 6: 'X', 7: 'X', 8: 'X', 9: 'X', 10: 'X', 21: 'X'}},
                            {'name': 'CZ', 'phase': +1, 'paulis': {1: 'X', 2: 'X', 4: 'X', 5: 'X', 6: 'X', 10: 'X', 11: 'X', 20: 'X'}},
                            {'name': 'DZ', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 3: 'X', 4: 'X', 5: 'X', 9: 'X', 10: 'X', 19: 'X'}},
                            {'name': 'EZ', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 7: 'X', 10: 'X', 11: 'X', 18: 'X' }},
                            {'name': 'FZ', 'phase': +1, 'paulis': {0: 'X', 2: 'X', 4: 'X', 6: 'X', 7: 'X', 8: 'X', 11: 'X', 17: 'X'}},
                            {'name': 'GZ', 'phase': +1, 'paulis': {3: 'X', 4: 'X', 5: 'X', 6: 'X', 8: 'X', 9: 'X', 11: 'X', 16: 'X'}},
                            {'name': 'HZ', 'phase': +1, 'paulis': {2: 'X', 3: 'X', 4: 'X', 5: 'X', 7: 'X', 8: 'X', 10: 'X', 15: 'X'}},
                            {'name': 'IZ', 'phase': +1, 'paulis': {1: 'X', 2: 'X', 3: 'X', 4: 'X', 6: 'X', 7: 'X', 9: 'X', 14: 'X'}},
                            {'name': 'LZ', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 5: 'X', 6: 'X', 8: 'X', 13: 'X'}},
                            {'name': 'MZ', 'phase': +1, 'paulis': {0: 'X', 2: 'X', 5: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 12: 'X'}},]
        logical_operators = [{'name': 'LZ', 'phase': +1, 'paulis': {0: 'Z', 12: 'Z', 13: 'Z', 17: 'Z', 18: 'Z', 19: 'Z', 21: 'Z'}},
                             {'name': 'LX', 'phase': +1, 'paulis': {0: 'X', 12: 'X', 13: 'X', 17: 'X', 18: 'X', 19: 'X', 21: 'X'}},
                           ]
        return code_stabilisers, logical_operators
    if code_name == (20, 2, 6): 
        code_stabilisers = [{'name': 'AZ', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}},
                            {'name': 'BZ', 'phase': +1, 'paulis': {4: 'Z', 5: 'Z', 6: 'Z', 7: 'Z'}},
                            {'name': 'CZ', 'phase': +1, 'paulis': {8: 'Z', 9: 'Z', 10: 'Z', 11: 'Z'}},
                            {'name': 'DZ', 'phase': +1, 'paulis': {12: 'Z', 13: 'Z', 14: 'Z', 15: 'Z'}},
                            {'name': 'EZ', 'phase': +1, 'paulis': {16: 'Z', 17: 'Z', 18: 'Z', 19: 'Z'}},
                            {'name': 'FZ', 'phase': +1, 'paulis': {0: 'Z', 3: 'Z', 6: 'Z', 7: 'Z', 10: 'Z', 11: 'Z', 12: 'Z', 15: 'Z'}},
                            {'name': 'GZ', 'phase': +1, 'paulis': {4: 'Z', 7: 'Z', 10: 'Z', 11: 'Z', 14: 'Z', 15: 'Z', 16: 'Z', 19: 'Z'}},
                            {'name': 'HZ', 'phase': +1, 'paulis': {0: 'Z', 3: 'Z', 8: 'Z', 11: 'Z', 14: 'Z', 15: 'Z', 18: 'Z', 19: 'Z'}},
                            {'name': 'LZ', 'phase': +1, 'paulis': {2: 'Z', 3: 'Z', 4: 'Z', 7: 'Z', 12: 'Z', 15: 'Z', 18: 'Z', 19: 'Z'}},
                            {'name': 'AX', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}},
                            {'name': 'BX', 'phase': +1, 'paulis': {4: 'X', 5: 'X', 6: 'X', 7: 'X'}},
                            {'name': 'CX', 'phase': +1, 'paulis': {8: 'X', 9: 'X', 10: 'X', 11: 'X'}},
                            {'name': 'DX', 'phase': +1, 'paulis': {12: 'X', 13: 'X', 14: 'X', 15: 'X'}},
                            {'name': 'EX', 'phase': +1, 'paulis': {16: 'X', 17: 'X', 18: 'X', 19: 'X'}},
                            {'name': 'FX', 'phase': +1, 'paulis': {0: 'X', 3: 'X', 6: 'X', 7: 'X', 10: 'X', 11: 'X', 12: 'X', 15: 'X'}},
                            {'name': 'GX', 'phase': +1, 'paulis': {4: 'X', 7: 'X', 10: 'X', 11: 'X', 14: 'X', 15: 'X', 16: 'X', 19: 'X'}},
                            {'name': 'HX', 'phase': +1, 'paulis': {0: 'X', 3: 'X', 8: 'X', 11: 'X', 14: 'X', 15: 'X', 18: 'X', 19: 'X'}},
                            {'name': 'LX', 'phase': +1, 'paulis': {2: 'X', 3: 'X', 4: 'X', 7: 'X', 12: 'X', 15: 'X', 18: 'X', 19: 'X'}}]
        logical_operators = [{'name': 'LZ1', 'phase': +1, 'paulis': {0: 'Z', 3: 'Z', 4: 'Z', 7: 'Z', 8: 'Z', 11: 'Z', 12: 'Z', 15: 'Z', 16: 'Z', 19: 'Z'}},
                             {'name': 'LZ2', 'phase': +1, 'paulis': {0: 'Z', 1: 'Z', 4: 'Z', 5: 'Z', 8: 'Z', 9: 'Z', 12: 'Z', 13: 'Z', 16: 'Z', 17: 'Z'}},
                             {'name': 'LX1', 'phase': +1, 'paulis': {0: 'X', 3: 'X', 4: 'X', 7: 'X', 8: 'X', 11: 'X', 12: 'X', 15: 'X', 16: 'X', 19: 'X'}},
                             {'name': 'LX2', 'phase': +1, 'paulis': {0: 'X', 1: 'X', 4: 'X', 5: 'X', 8: 'X', 9: 'X', 12: 'X', 13: 'X', 16: 'X', 17: 'X'}}
                           ]
        return code_stabilisers, logical_operators
    
    if code_name == (71, 1, 11):
        #11 x11 color code
        code_stabilisers = [{'name': 'X_1', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 4: 'Z', 5: 'Z'}} ,
                            {'name': 'X_2', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}} ,
                            {'name': 'X_3', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 8: 'Z', 9: 'Z'}} ,
                            {'name': 'X_4', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 9: 'Z', 10: 'Z', 14: 'Z', 15: 'Z'}} ,
                            {'name': 'X_5', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 10: 'Z', 11: 'Z'}} ,
                            {'name': 'X_6', 'phase': 1, 'paulis': {7: 'Z', 11: 'Z', 16: 'Z', 17: 'Z'}} ,
                            {'name': 'X_7', 'phase': 1, 'paulis': {12: 'Z', 18: 'Z', 24: 'Z', 25: 'Z'}} ,
                            {'name': 'X_8', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 18: 'Z', 19: 'Z'}} ,
                            {'name': 'X_9', 'phase': 1, 'paulis': {8: 'Z', 9: 'Z', 13: 'Z', 14: 'Z', 19: 'Z', 20: 'Z', 26: 'Z', 27: 'Z'}} ,
                            {'name': 'X_10', 'phase': 1, 'paulis': {14: 'Z', 15: 'Z', 20: 'Z', 21: 'Z'}} ,
                            {'name': 'X_11', 'phase': 1, 'paulis': {10: 'Z', 11: 'Z', 15: 'Z', 16: 'Z', 21: 'Z', 22: 'Z', 28: 'Z', 29: 'Z'}} ,
                            {'name': 'X_12', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 22: 'Z', 23: 'Z'}} ,
                            {'name': 'X_13', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 32: 'Z', 33: 'Z'}} ,
                            {'name': 'X_14', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 25: 'Z', 26: 'Z', 33: 'Z', 34: 'Z', 42: 'Z', 43: 'Z'}} ,
                            {'name': 'X_15', 'phase': 1, 'paulis': {26: 'Z', 27: 'Z', 34: 'Z', 35: 'Z'}} ,
                            {'name': 'X_16', 'phase': 1, 'paulis': {20: 'Z', 21: 'Z', 27: 'Z', 28: 'Z', 35: 'Z', 36: 'Z', 44: 'Z', 45: 'Z'}} ,
                            {'name': 'X_17', 'phase': 1, 'paulis': {28: 'Z', 29: 'Z', 36: 'Z', 37: 'Z'}} ,
                            {'name': 'X_18', 'phase': 1, 'paulis': {22: 'Z', 23: 'Z', 29: 'Z', 30: 'Z', 37: 'Z', 38: 'Z', 46: 'Z', 47: 'Z'}} ,
                            {'name': 'X_19', 'phase': 1, 'paulis': {30: 'Z', 31: 'Z', 38: 'Z', 39: 'Z'}} ,
                            {'name': 'X_20', 'phase': 1, 'paulis': {31: 'Z', 39: 'Z', 48: 'Z', 49: 'Z'}} ,
                            {'name': 'X_21', 'phase': 1, 'paulis': {40: 'Z', 50: 'Z', 60: 'Z', 61: 'Z'}} ,
                            {'name': 'X_22', 'phase': 1, 'paulis': {40: 'Z', 41: 'Z', 50: 'Z', 51: 'Z'}} ,
                            {'name': 'X_23', 'phase': 1, 'paulis': {32: 'Z', 33: 'Z', 41: 'Z', 42: 'Z', 51: 'Z', 52: 'Z', 62: 'Z', 63: 'Z'}} ,
                            {'name': 'X_24', 'phase': 1, 'paulis': {42: 'Z', 43: 'Z', 52: 'Z', 53: 'Z'}} ,
                            {'name': 'X_25', 'phase': 1, 'paulis': {34: 'Z', 35: 'Z', 43: 'Z', 44: 'Z', 53: 'Z', 54: 'Z', 64: 'Z', 65: 'Z'}} ,
                            {'name': 'X_26', 'phase': 1, 'paulis': {44: 'Z', 45: 'Z', 54: 'Z', 55: 'Z'}} ,
                            {'name': 'X_27', 'phase': 1, 'paulis': {36: 'Z', 37: 'Z', 45: 'Z', 46: 'Z', 55: 'Z', 56: 'Z', 66: 'Z', 67: 'Z'}} ,
                            {'name': 'X_28', 'phase': 1, 'paulis': {46: 'Z', 47: 'Z', 56: 'Z', 57: 'Z'}} ,
                            {'name': 'X_29', 'phase': 1, 'paulis': {38: 'Z', 39: 'Z', 47: 'Z', 48: 'Z', 57: 'Z', 58: 'Z', 68: 'Z', 69: 'Z'}} ,
                            {'name': 'X_30', 'phase': 1, 'paulis': {48: 'Z', 49: 'Z', 58: 'Z', 59: 'Z'}} ,
                            {'name': 'X_31', 'phase': 1, 'paulis': {50: 'Z', 51: 'Z', 61: 'Z', 62: 'Z'}} ,
                            {'name': 'X_32', 'phase': 1, 'paulis': {52: 'Z', 53: 'Z', 63: 'Z', 64: 'Z'}} ,
                            {'name': 'X_33', 'phase': 1, 'paulis': {54: 'Z', 55: 'Z', 65: 'Z', 66: 'Z'}} ,
                            {'name': 'X_34', 'phase': 1, 'paulis': {56: 'Z', 57: 'Z', 67: 'Z', 68: 'Z'}} ,
                            {'name': 'X_35', 'phase': 1, 'paulis': {58: 'Z', 59: 'Z', 69: 'Z', 70: 'Z'}} ,
                            {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 2: 'X', 4: 'X', 5: 'X'}} ,
                            {'name': 'X_2', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}} ,
                            {'name': 'X_3', 'phase': 1, 'paulis': {4: 'X', 5: 'X', 8: 'X', 9: 'X'}} ,
                            {'name': 'X_4', 'phase': 1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 14: 'X', 15: 'X'}} ,
                            {'name': 'X_5', 'phase': 1, 'paulis': {6: 'X', 7: 'X', 10: 'X', 11: 'X'}} ,
                            {'name': 'X_6', 'phase': 1, 'paulis': {7: 'X', 11: 'X', 16: 'X', 17: 'X'}} ,
                            {'name': 'X_7', 'phase': 1, 'paulis': {12: 'X', 18: 'X', 24: 'X', 25: 'X'}} ,
                            {'name': 'X_8', 'phase': 1, 'paulis': {12: 'X', 13: 'X', 18: 'X', 19: 'X'}} ,
                            {'name': 'X_9', 'phase': 1, 'paulis': {8: 'X', 9: 'X', 13: 'X', 14: 'X', 19: 'X', 20: 'X', 26: 'X', 27: 'X'}} ,
                            {'name': 'X_10', 'phase': 1, 'paulis': {14: 'X', 15: 'X', 20: 'X', 21: 'X'}} ,
                            {'name': 'X_11', 'phase': 1, 'paulis': {10: 'X', 11: 'X', 15: 'X', 16: 'X', 21: 'X', 22: 'X', 28: 'X', 29: 'X'}} ,
                            {'name': 'X_12', 'phase': 1, 'paulis': {16: 'X', 17: 'X', 22: 'X', 23: 'X'}} ,
                            {'name': 'X_13', 'phase': 1, 'paulis': {24: 'X', 25: 'X', 32: 'X', 33: 'X'}} ,
                            {'name': 'X_14', 'phase': 1, 'paulis': {18: 'X', 19: 'X', 25: 'X', 26: 'X', 33: 'X', 34: 'X', 42: 'X', 43: 'X'}} ,
                            {'name': 'X_15', 'phase': 1, 'paulis': {26: 'X', 27: 'X', 34: 'X', 35: 'X'}} ,
                            {'name': 'X_16', 'phase': 1, 'paulis': {20: 'X', 21: 'X', 27: 'X', 28: 'X', 35: 'X', 36: 'X', 44: 'X', 45: 'X'}} ,
                            {'name': 'X_17', 'phase': 1, 'paulis': {28: 'X', 29: 'X', 36: 'X', 37: 'X'}} ,
                            {'name': 'X_18', 'phase': 1, 'paulis': {22: 'X', 23: 'X', 29: 'X', 30: 'X', 37: 'X', 38: 'X', 46: 'X', 47: 'X'}} ,
                            {'name': 'X_19', 'phase': 1, 'paulis': {30: 'X', 31: 'X', 38: 'X', 39: 'X'}} ,
                            {'name': 'X_20', 'phase': 1, 'paulis': {31: 'X', 39: 'X', 48: 'X', 49: 'X'}} ,
                            {'name': 'X_21', 'phase': 1, 'paulis': {40: 'X', 50: 'X', 60: 'X', 61: 'X'}} ,
                            {'name': 'X_22', 'phase': 1, 'paulis': {40: 'X', 41: 'X', 50: 'X', 51: 'X'}} ,
                            {'name': 'X_23', 'phase': 1, 'paulis': {32: 'X', 33: 'X', 41: 'X', 42: 'X', 51: 'X', 52: 'X', 62: 'X', 63: 'X'}} ,
                            {'name': 'X_24', 'phase': 1, 'paulis': {42: 'X', 43: 'X', 52: 'X', 53: 'X'}} ,
                            {'name': 'X_25', 'phase': 1, 'paulis': {34: 'X', 35: 'X', 43: 'X', 44: 'X', 53: 'X', 54: 'X', 64: 'X', 65: 'X'}} ,
                            {'name': 'X_26', 'phase': 1, 'paulis': {44: 'X', 45: 'X', 54: 'X', 55: 'X'}} ,
                            {'name': 'X_27', 'phase': 1, 'paulis': {36: 'X', 37: 'X', 45: 'X', 46: 'X', 55: 'X', 56: 'X', 66: 'X', 67: 'X'}} ,
                            {'name': 'X_28', 'phase': 1, 'paulis': {46: 'X', 47: 'X', 56: 'X', 57: 'X'}} ,
                            {'name': 'X_29', 'phase': 1, 'paulis': {38: 'X', 39: 'X', 47: 'X', 48: 'X', 57: 'X', 58: 'X', 68: 'X', 69: 'X'}} ,
                            {'name': 'X_30', 'phase': 1, 'paulis': {48: 'X', 49: 'X', 58: 'X', 59: 'X'}} ,
                            {'name': 'X_31', 'phase': 1, 'paulis': {50: 'X', 51: 'X', 61: 'X', 62: 'X'}} ,
                            {'name': 'X_32', 'phase': 1, 'paulis': {52: 'X', 53: 'X', 63: 'X', 64: 'X'}} ,
                            {'name': 'X_33', 'phase': 1, 'paulis': {54: 'X', 55: 'X', 65: 'X', 66: 'X'}} ,
                            {'name': 'X_34', 'phase': 1, 'paulis': {56: 'X', 57: 'X', 67: 'X', 68: 'X'}} ,
                            {'name': 'X_35', 'phase': 1, 'paulis': {58: 'X', 59: 'X', 69: 'X', 70: 'X'}} 
            ]
        logical_operators = [
                        {'name': 'LX', 'phase': 1, 'paulis': {60: 'X', 61: 'X', 62: 'X', 63: 'X', 64: 'X', 65: 'X', 66: 'X', 67: 'X', 68: 'X', 69: 'X', 70: 'X'}} ,
                        {'name': 'LZ', 'phase': 1, 'paulis': {60: 'Z', 61: 'Z', 62: 'Z', 63: 'Z', 64: 'Z', 65: 'Z', 66: 'Z', 67: 'Z', 68: 'Z', 69: 'Z', 70: 'Z'}} 
        ]
        return code_stabilisers, logical_operators
    if code_name == (49, 1, 9):
        #9x9 color code
        code_stabilisers = [{'name': 'X_1', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}} ,
                        {'name': 'X_2', 'phase': 1, 'paulis': {1: 'Z', 3: 'Z', 6: 'Z', 7: 'Z'}} ,
                        {'name': 'X_3', 'phase': 1, 'paulis': {4: 'Z', 8: 'Z', 12: 'Z', 13: 'Z'}} ,
                        {'name': 'X_4', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 8: 'Z', 9: 'Z'}} ,
                        {'name': 'X_5', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 9: 'Z', 10: 'Z', 14: 'Z', 15: 'Z'}} ,
                        {'name': 'X_6', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 10: 'Z', 11: 'Z'}} ,
                        {'name': 'X_7', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 18: 'Z', 19: 'Z'}} ,
                        {'name': 'X_8', 'phase': 1, 'paulis': {8: 'Z', 9: 'Z', 13: 'Z', 14: 'Z', 19: 'Z', 20: 'Z', 26: 'Z', 27: 'Z'}} ,
                        {'name': 'X_9', 'phase': 1, 'paulis': {14: 'Z', 15: 'Z', 20: 'Z', 21: 'Z'}} ,
                        {'name': 'X_10', 'phase': 1, 'paulis': {10: 'Z', 11: 'Z', 15: 'Z', 16: 'Z', 21: 'Z', 22: 'Z', 28: 'Z', 29: 'Z'}} ,
                        {'name': 'X_11', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 22: 'Z', 23: 'Z'}} ,
                        {'name': 'X_12', 'phase': 1, 'paulis': {17: 'Z', 23: 'Z', 30: 'Z', 31: 'Z'}} ,
                        {'name': 'X_13', 'phase': 1, 'paulis': {24: 'Z', 32: 'Z', 40: 'Z', 41: 'Z'}} ,
                        {'name': 'X_14', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 32: 'Z', 33: 'Z'}} ,
                        {'name': 'X_15', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 25: 'Z', 26: 'Z', 33: 'Z', 34: 'Z', 42: 'Z', 43: 'Z'}} ,
                        {'name': 'X_16', 'phase': 1, 'paulis': {26: 'Z', 27: 'Z', 34: 'Z', 35: 'Z'}} ,
                        {'name': 'X_17', 'phase': 1, 'paulis': {20: 'Z', 21: 'Z', 27: 'Z', 28: 'Z', 35: 'Z', 36: 'Z', 44: 'Z', 45: 'Z'}} ,
                        {'name': 'X_18', 'phase': 1, 'paulis': {28: 'Z', 29: 'Z', 36: 'Z', 37: 'Z'}} ,
                        {'name': 'X_19', 'phase': 1, 'paulis': {22: 'Z', 23: 'Z', 29: 'Z', 30: 'Z', 37: 'Z', 38: 'Z', 46: 'Z', 47: 'Z'}} ,
                        {'name': 'X_20', 'phase': 1, 'paulis': {30: 'Z', 31: 'Z', 38: 'Z', 39: 'Z'}} ,
                        {'name': 'X_21', 'phase': 1, 'paulis': {32: 'Z', 33: 'Z', 41: 'Z', 42: 'Z'}} ,
                        {'name': 'X_22', 'phase': 1, 'paulis': {34: 'Z', 35: 'Z', 43: 'Z', 44: 'Z'}} ,
                        {'name': 'X_23', 'phase': 1, 'paulis': {36: 'Z', 37: 'Z', 45: 'Z', 46: 'Z'}} ,
                        {'name': 'X_24', 'phase': 1, 'paulis': {38: 'Z', 39: 'Z', 47: 'Z', 48: 'Z'}},
                        {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}} ,
                        {'name': 'X_2', 'phase': 1, 'paulis': {1: 'X', 3: 'X', 6: 'X', 7: 'X'}} ,
                        {'name': 'X_3', 'phase': 1, 'paulis': {4: 'X', 8: 'X', 12: 'X', 13: 'X'}} ,
                        {'name': 'X_4', 'phase': 1, 'paulis': {4: 'X', 5: 'X', 8: 'X', 9: 'X'}} ,
                        {'name': 'X_5', 'phase': 1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 14: 'X', 15: 'X'}} ,
                        {'name': 'X_6', 'phase': 1, 'paulis': {6: 'X', 7: 'X', 10: 'X', 11: 'X'}} ,
                        {'name': 'X_7', 'phase': 1, 'paulis': {12: 'X', 13: 'X', 18: 'X', 19: 'X'}} ,
                        {'name': 'X_8', 'phase': 1, 'paulis': {8: 'X', 9: 'X', 13: 'X', 14: 'X', 19: 'X', 20: 'X', 26: 'X', 27: 'X'}} ,
                        {'name': 'X_9', 'phase': 1, 'paulis': {14: 'X', 15: 'X', 20: 'X', 21: 'X'}} ,
                        {'name': 'X_10', 'phase': 1, 'paulis': {10: 'X', 11: 'X', 15: 'X', 16: 'X', 21: 'X', 22: 'X', 28: 'X', 29: 'X'}} ,
                        {'name': 'X_11', 'phase': 1, 'paulis': {16: 'X', 17: 'X', 22: 'X', 23: 'X'}} ,
                        {'name': 'X_12', 'phase': 1, 'paulis': {17: 'X', 23: 'X', 30: 'X', 31: 'X'}} ,
                        {'name': 'X_13', 'phase': 1, 'paulis': {24: 'X', 32: 'X', 40: 'X', 41: 'X'}} ,
                        {'name': 'X_14', 'phase': 1, 'paulis': {24: 'X', 25: 'X', 32: 'X', 33: 'X'}} ,
                        {'name': 'X_15', 'phase': 1, 'paulis': {18: 'X', 19: 'X', 25: 'X', 26: 'X', 33: 'X', 34: 'X', 42: 'X', 43: 'X'}} ,
                        {'name': 'X_16', 'phase': 1, 'paulis': {26: 'X', 27: 'X', 34: 'X', 35: 'X'}} ,
                        {'name': 'X_17', 'phase': 1, 'paulis': {20: 'X', 21: 'X', 27: 'X', 28: 'X', 35: 'X', 36: 'X', 44: 'X', 45: 'X'}} ,
                        {'name': 'X_18', 'phase': 1, 'paulis': {28: 'X', 29: 'X', 36: 'X', 37: 'X'}} ,
                        {'name': 'X_19', 'phase': 1, 'paulis': {22: 'X', 23: 'X', 29: 'X', 30: 'X', 37: 'X', 38: 'X', 46: 'X', 47: 'X'}} ,
                        {'name': 'X_20', 'phase': 1, 'paulis': {30: 'X', 31: 'X', 38: 'X', 39: 'X'}} ,
                        {'name': 'X_21', 'phase': 1, 'paulis': {32: 'X', 33: 'X', 41: 'X', 42: 'X'}} ,
                        {'name': 'X_22', 'phase': 1, 'paulis': {34: 'X', 35: 'X', 43: 'X', 44: 'X'}} ,
                        {'name': 'X_23', 'phase': 1, 'paulis': {36: 'X', 37: 'X', 45: 'X', 46: 'X'}} ,
                        {'name': 'X_24', 'phase': 1, 'paulis': {38: 'X', 39: 'X', 47: 'X', 48: 'X'}} ]
        logical_operators = [ 
                          {'name': 'LX', 'phase': 1, 'paulis': {40: 'X', 41: 'X', 42: 'X', 43: 'X', 44: 'X', 45: 'X', 46: 'X', 47: 'X', 48: 'X'}} ,
                        {'name': 'LZ', 'phase': 1, 'paulis': {40: 'Z', 41: 'Z', 42: 'Z', 43: 'Z', 44: 'Z', 45: 'Z', 46: 'Z', 47: 'Z', 48: 'Z'}} 
                    ]
        return code_stabilisers, logical_operators
    if code_name == (31, 1, 7):
        #7x7 color code
        code_stabilisers = [{'name': 'X_1', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 4: 'Z', 5: 'Z'}} ,
                        {'name': 'X_2', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z'}} ,
                        {'name': 'X_3', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 8: 'Z', 9: 'Z'}} ,
                        {'name': 'X_4', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 9: 'Z', 10: 'Z', 14: 'Z', 15: 'Z'}} ,
                        {'name': 'X_5', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 10: 'Z', 11: 'Z'}} ,
                        {'name': 'X_6', 'phase': 1, 'paulis': {7: 'Z', 11: 'Z', 16: 'Z', 17: 'Z'}} ,
                        {'name': 'X_7', 'phase': 1, 'paulis': {12: 'Z', 18: 'Z', 24: 'Z', 25: 'Z'}} ,
                        {'name': 'X_8', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 18: 'Z', 19: 'Z'}} ,
                        {'name': 'X_9', 'phase': 1, 'paulis': {8: 'Z', 9: 'Z', 13: 'Z', 14: 'Z', 19: 'Z', 20: 'Z', 26: 'Z', 27: 'Z'}} ,
                        {'name': 'X_10', 'phase': 1, 'paulis': {14: 'Z', 15: 'Z', 20: 'Z', 21: 'Z'}} ,
                        {'name': 'X_11', 'phase': 1, 'paulis': {10: 'Z', 11: 'Z', 15: 'Z', 16: 'Z', 21: 'Z', 22: 'Z', 28: 'Z', 29: 'Z'}} ,
                        {'name': 'X_12', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 22: 'Z', 23: 'Z'}} ,
                        {'name': 'X_13', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 25: 'Z', 26: 'Z'}} ,
                        {'name': 'X_14', 'phase': 1, 'paulis': {20: 'Z', 21: 'Z', 27: 'Z', 28: 'Z'}} ,
                        {'name': 'X_15', 'phase': 1, 'paulis': {22: 'Z', 23: 'Z', 29: 'Z', 30: 'Z'}} ,
                        {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 2: 'X', 4: 'X', 5: 'X'}} ,
                        {'name': 'X_2', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X'}} ,
                        {'name': 'X_3', 'phase': 1, 'paulis': {4: 'X', 5: 'X', 8: 'X', 9: 'X'}} ,
                        {'name': 'X_4', 'phase': 1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 14: 'X', 15: 'X'}} ,
                        {'name': 'X_5', 'phase': 1, 'paulis': {6: 'X', 7: 'X', 10: 'X', 11: 'X'}} ,
                        {'name': 'X_6', 'phase': 1, 'paulis': {7: 'X', 11: 'X', 16: 'X', 17: 'X'}} ,
                        {'name': 'X_7', 'phase': 1, 'paulis': {12: 'X', 18: 'X', 24: 'X', 25: 'X'}} ,
                        {'name': 'X_8', 'phase': 1, 'paulis': {12: 'X', 13: 'X', 18: 'X', 19: 'X'}} ,
                        {'name': 'X_9', 'phase': 1, 'paulis': {8: 'X', 9: 'X', 13: 'X', 14: 'X', 19: 'X', 20: 'X', 26: 'X', 27: 'X'}} ,
                        {'name': 'X_10', 'phase': 1, 'paulis': {14: 'X', 15: 'X', 20: 'X', 21: 'X'}} ,
                        {'name': 'X_11', 'phase': 1, 'paulis': {10: 'X', 11: 'X', 15: 'X', 16: 'X', 21: 'X', 22: 'X', 28: 'X', 29: 'X'}} ,
                        {'name': 'X_12', 'phase': 1, 'paulis': {16: 'X', 17: 'X', 22: 'X', 23: 'X'}} ,
                        {'name': 'X_13', 'phase': 1, 'paulis': {18: 'X', 19: 'X', 25: 'X', 26: 'X'}} ,
                        {'name': 'X_14', 'phase': 1, 'paulis': {20: 'X', 21: 'X', 27: 'X', 28: 'X'}} ,
                        {'name': 'X_15', 'phase': 1, 'paulis': {22: 'X', 23: 'X', 29: 'X', 30: 'X'}} ]
        logical_operators = [{'name': 'LX', 'phase': 1, 'paulis': {24: 'X', 25: 'X', 26: 'X', 27: 'X', 28: 'X', 29: 'X', 30: 'X'}} ,
                        {'name': 'LZ', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z', 28: 'Z', 29: 'Z', 30: 'Z'}} 
                    ]
        return code_stabilisers, logical_operators
    
    if code_name == (121, 1, 11):
            #11x11 surface
        code_stabilisers = [
                            {'name': 'X_1', 'phase': 1, 'paulis': {10: 'Z', 21: 'Z'}},
                            {'name': 'X_2', 'phase': 1, 'paulis': {32: 'Z', 43: 'Z'}},
                            {'name': 'X_3', 'phase': 1, 'paulis': {54: 'Z', 65: 'Z'}},
                            {'name': 'X_4', 'phase': 1, 'paulis': {76: 'Z', 87: 'Z'}},
                            {'name': 'X_5', 'phase': 1, 'paulis': {98: 'Z', 109: 'Z'}},
                            {'name': 'X_6', 'phase': 1, 'paulis': {20: 'Z', 21: 'Z', 31: 'Z', 32: 'Z'}},
                            {'name': 'X_7', 'phase': 1, 'paulis': {42: 'Z', 43: 'Z', 53: 'Z', 54: 'Z'}},
                            {'name': 'X_8', 'phase': 1, 'paulis': {64: 'Z', 65: 'Z', 75: 'Z', 76: 'Z'}},
                            {'name': 'X_9', 'phase': 1, 'paulis': {86: 'Z', 87: 'Z', 97: 'Z', 98: 'Z'}},
                            {'name': 'X_10', 'phase': 1, 'paulis': {108: 'Z', 109: 'Z', 119: 'Z', 120: 'Z'}},
                            {'name': 'X_11', 'phase': 1, 'paulis': {8: 'Z', 9: 'Z', 19: 'Z', 20: 'Z'}},
                            {'name': 'X_12', 'phase': 1, 'paulis': {30: 'Z', 31: 'Z', 41: 'Z', 42: 'Z'}},
                            {'name': 'X_13', 'phase': 1, 'paulis': {52: 'Z', 53: 'Z', 63: 'Z', 64: 'Z'}},
                            {'name': 'X_14', 'phase': 1, 'paulis': {74: 'Z', 75: 'Z', 85: 'Z', 86: 'Z'}},
                            {'name': 'X_15', 'phase': 1, 'paulis': {96: 'Z', 97: 'Z', 107: 'Z', 108: 'Z'}},
                            {'name': 'X_16', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 29: 'Z', 30: 'Z'}},
                            {'name': 'X_17', 'phase': 1, 'paulis': {40: 'Z', 41: 'Z', 51: 'Z', 52: 'Z'}},
                            {'name': 'X_18', 'phase': 1, 'paulis': {62: 'Z', 63: 'Z', 73: 'Z', 74: 'Z'}},
                            {'name': 'X_19', 'phase': 1, 'paulis': {84: 'Z', 85: 'Z', 95: 'Z', 96: 'Z'}},
                            {'name': 'X_20', 'phase': 1, 'paulis': {106: 'Z', 107: 'Z', 117: 'Z', 118: 'Z'}},
                            {'name': 'X_21', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 17: 'Z', 18: 'Z'}},
                            {'name': 'X_22', 'phase': 1, 'paulis': {28: 'Z', 29: 'Z', 39: 'Z', 40: 'Z'}},
                            {'name': 'X_23', 'phase': 1, 'paulis': {50: 'Z', 51: 'Z', 61: 'Z', 62: 'Z'}},
                            {'name': 'X_24', 'phase': 1, 'paulis': {72: 'Z', 73: 'Z', 83: 'Z', 84: 'Z'}},
                            {'name': 'X_25', 'phase': 1, 'paulis': {94: 'Z', 95: 'Z', 105: 'Z', 106: 'Z'}},
                            {'name': 'X_26', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 27: 'Z', 28: 'Z'}},
                            {'name': 'X_27', 'phase': 1, 'paulis': {38: 'Z', 39: 'Z', 49: 'Z', 50: 'Z'}},
                            {'name': 'X_28', 'phase': 1, 'paulis': {60: 'Z', 61: 'Z', 71: 'Z', 72: 'Z'}},
                            {'name': 'X_29', 'phase': 1, 'paulis': {82: 'Z', 83: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'X_30', 'phase': 1, 'paulis': {104: 'Z', 105: 'Z', 115: 'Z', 116: 'Z'}},
                            {'name': 'X_31', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 15: 'Z', 16: 'Z'}},
                            {'name': 'X_32', 'phase': 1, 'paulis': {26: 'Z', 27: 'Z', 37: 'Z', 38: 'Z'}},
                            {'name': 'X_33', 'phase': 1, 'paulis': {48: 'Z', 49: 'Z', 59: 'Z', 60: 'Z'}},
                            {'name': 'X_34', 'phase': 1, 'paulis': {70: 'Z', 71: 'Z', 81: 'Z', 82: 'Z'}},
                            {'name': 'X_35', 'phase': 1, 'paulis': {92: 'Z', 93: 'Z', 103: 'Z', 104: 'Z'}},
                            {'name': 'X_36', 'phase': 1, 'paulis': {14: 'Z', 15: 'Z', 25: 'Z', 26: 'Z'}},
                            {'name': 'X_37', 'phase': 1, 'paulis': {36: 'Z', 37: 'Z', 47: 'Z', 48: 'Z'}},
                            {'name': 'X_38', 'phase': 1, 'paulis': {58: 'Z', 59: 'Z', 69: 'Z', 70: 'Z'}},
                            {'name': 'X_39', 'phase': 1, 'paulis': {80: 'Z', 81: 'Z', 91: 'Z', 92: 'Z'}},
                            {'name': 'X_40', 'phase': 1, 'paulis': {102: 'Z', 103: 'Z', 113: 'Z', 114: 'Z'}},
                            {'name': 'X_41', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 13: 'Z', 14: 'Z'}},
                            {'name': 'X_42', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 35: 'Z', 36: 'Z'}},
                            {'name': 'X_43', 'phase': 1, 'paulis': {46: 'Z', 47: 'Z', 57: 'Z', 58: 'Z'}},
                            {'name': 'X_44', 'phase': 1, 'paulis': {68: 'Z', 69: 'Z', 79: 'Z', 80: 'Z'}},
                            {'name': 'X_45', 'phase': 1, 'paulis': {90: 'Z', 91: 'Z', 101: 'Z', 102: 'Z'}},
                            {'name': 'X_46', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 23: 'Z', 24: 'Z'}},
                            {'name': 'X_47', 'phase': 1, 'paulis': {34: 'Z', 35: 'Z', 45: 'Z', 46: 'Z'}},
                            {'name': 'X_48', 'phase': 1, 'paulis': {56: 'Z', 57: 'Z', 67: 'Z', 68: 'Z'}},
                            {'name': 'X_49', 'phase': 1, 'paulis': {78: 'Z', 79: 'Z', 89: 'Z', 90: 'Z'}},
                            {'name': 'X_50', 'phase': 1, 'paulis': {100: 'Z', 101: 'Z', 111: 'Z', 112: 'Z'}},
                            {'name': 'X_51', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 11: 'Z', 12: 'Z'}},
                            {'name': 'X_52', 'phase': 1, 'paulis': {22: 'Z', 23: 'Z', 33: 'Z', 34: 'Z'}},
                            {'name': 'X_53', 'phase': 1, 'paulis': {44: 'Z', 45: 'Z', 55: 'Z', 56: 'Z'}},
                            {'name': 'X_54', 'phase': 1, 'paulis': {66: 'Z', 67: 'Z', 77: 'Z', 78: 'Z'}},
                            {'name': 'X_55', 'phase': 1, 'paulis': {88: 'Z', 89: 'Z', 99: 'Z', 100: 'Z'}},
                            {'name': 'X_56', 'phase': 1, 'paulis': {11: 'Z', 22: 'Z'}},
                            {'name': 'X_57', 'phase': 1, 'paulis': {33: 'Z', 44: 'Z'}},
                            {'name': 'X_58', 'phase': 1, 'paulis': {55: 'Z', 66: 'Z'}},
                            {'name': 'X_59', 'phase': 1, 'paulis': {77: 'Z', 88: 'Z'}},
                            {'name': 'X_60', 'phase': 1, 'paulis': {99: 'Z', 110: 'Z'}},
                            {'name': 'X_61', 'phase': 1, 'paulis': {0: 'X', 1: 'X'}},
                            {'name': 'X_62', 'phase': 1, 'paulis': {2: 'X', 3: 'X'}},
                            {'name': 'X_63', 'phase': 1, 'paulis': {4: 'X', 5: 'X'}},
                            {'name': 'X_64', 'phase': 1, 'paulis': {6: 'X', 7: 'X'}},
                            {'name': 'X_65', 'phase': 1, 'paulis': {8: 'X', 9: 'X'}},
                            {'name': 'X_66', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 12: 'X', 13: 'X'}},
                            {'name': 'X_67', 'phase': 1, 'paulis': {3: 'X', 4: 'X', 14: 'X', 15: 'X'}},
                            {'name': 'X_68', 'phase': 1, 'paulis': {5: 'X', 6: 'X', 16: 'X', 17: 'X'}},
                            {'name': 'X_69', 'phase': 1, 'paulis': {7: 'X', 8: 'X', 18: 'X', 19: 'X'}},
                            {'name': 'X_70', 'phase': 1, 'paulis': {9: 'X', 10: 'X', 20: 'X', 21: 'X'}},
                            {'name': 'X_71', 'phase': 1, 'paulis': {11: 'X', 12: 'X', 22: 'X', 23: 'X'}},
                            {'name': 'X_72', 'phase': 1, 'paulis': {13: 'X', 14: 'X', 24: 'X', 25: 'X'}},
                            {'name': 'X_73', 'phase': 1, 'paulis': {15: 'X', 16: 'X', 26: 'X', 27: 'X'}},
                            {'name': 'X_74', 'phase': 1, 'paulis': {17: 'X', 18: 'X', 28: 'X', 29: 'X'}},
                            {'name': 'X_75', 'phase': 1, 'paulis': {19: 'X', 20: 'X', 30: 'X', 31: 'X'}},
                            {'name': 'X_76', 'phase': 1, 'paulis': {23: 'X', 24: 'X', 34: 'X', 35: 'X'}},
                            {'name': 'X_77', 'phase': 1, 'paulis': {25: 'X', 26: 'X', 36: 'X', 37: 'X'}},
                            {'name': 'X_78', 'phase': 1, 'paulis': {27: 'X', 28: 'X', 38: 'X', 39: 'X'}},
                            {'name': 'X_79', 'phase': 1, 'paulis': {29: 'X', 30: 'X', 40: 'X', 41: 'X'}},
                            {'name': 'X_80', 'phase': 1, 'paulis': {31: 'X', 32: 'X', 42: 'X', 43: 'X'}},
                            {'name': 'X_81', 'phase': 1, 'paulis': {33: 'X', 34: 'X', 44: 'X', 45: 'X'}},
                            {'name': 'X_82', 'phase': 1, 'paulis': {35: 'X', 36: 'X', 46: 'X', 47: 'X'}},
                            {'name': 'X_83', 'phase': 1, 'paulis': {37: 'X', 38: 'X', 48: 'X', 49: 'X'}},
                            {'name': 'X_84', 'phase': 1, 'paulis': {39: 'X', 40: 'X', 50: 'X', 51: 'X'}},
                            {'name': 'X_85', 'phase': 1, 'paulis': {41: 'X', 42: 'X', 52: 'X', 53: 'X'}},
                            {'name': 'X_86', 'phase': 1, 'paulis': {45: 'X', 46: 'X', 56: 'X', 57: 'X'}},
                            {'name': 'X_87', 'phase': 1, 'paulis': {47: 'X', 48: 'X', 58: 'X', 59: 'X'}},
                            {'name': 'X_88', 'phase': 1, 'paulis': {49: 'X', 50: 'X', 60: 'X', 61: 'X'}},
                            {'name': 'X_89', 'phase': 1, 'paulis': {51: 'X', 52: 'X', 62: 'X', 63: 'X'}},
                            {'name': 'X_90', 'phase': 1, 'paulis': {53: 'X', 54: 'X', 64: 'X', 65: 'X'}},
                            {'name': 'X_91', 'phase': 1, 'paulis': {55: 'X', 56: 'X', 66: 'X', 67: 'X'}},
                            {'name': 'X_92', 'phase': 1, 'paulis': {57: 'X', 58: 'X', 68: 'X', 69: 'X'}},
                            {'name': 'X_93', 'phase': 1, 'paulis': {59: 'X', 60: 'X', 70: 'X', 71: 'X'}},
                            {'name': 'X_94', 'phase': 1, 'paulis': {61: 'X', 62: 'X', 72: 'X', 73: 'X'}},
                            {'name': 'X_95', 'phase': 1, 'paulis': {63: 'X', 64: 'X', 74: 'X', 75: 'X'}},
                            {'name': 'X_96', 'phase': 1, 'paulis': {67: 'X', 68: 'X', 78: 'X', 79: 'X'}},
                            {'name': 'X_97', 'phase': 1, 'paulis': {69: 'X', 70: 'X', 80: 'X', 81: 'X'}},
                            {'name': 'X_98', 'phase': 1, 'paulis': {71: 'X', 72: 'X', 82: 'X', 83: 'X'}},
                            {'name': 'X_99', 'phase': 1, 'paulis': {73: 'X', 74: 'X', 84: 'X', 85: 'X'}},
                            {'name': 'X_100', 'phase': 1, 'paulis': {75: 'X', 76: 'X', 86: 'X', 87: 'X'}},
                            {'name': 'X_101', 'phase': 1, 'paulis': {77: 'X', 78: 'X', 88: 'X', 89: 'X'}},
                            {'name': 'X_102', 'phase': 1, 'paulis': {79: 'X', 80: 'X', 90: 'X', 91: 'X'}},
                            {'name': 'X_103', 'phase': 1, 'paulis': {81: 'X', 82: 'X', 92: 'X', 93: 'X'}},
                            {'name': 'X_104', 'phase': 1, 'paulis': {83: 'X', 84: 'X', 94: 'X', 95: 'X'}},
                            {'name': 'X_105', 'phase': 1, 'paulis': {85: 'X', 86: 'X', 96: 'X', 97: 'X'}},
                            {'name': 'X_106', 'phase': 1, 'paulis': {89: 'X', 90: 'X', 100: 'X', 101: 'X'}},
                            {'name': 'X_107', 'phase': 1, 'paulis': {91: 'X', 92: 'X', 102: 'X', 103: 'X'}},
                            {'name': 'X_108', 'phase': 1, 'paulis': {93: 'X', 94: 'X', 104: 'X', 105: 'X'}},
                            {'name': 'X_109', 'phase': 1, 'paulis': {95: 'X', 96: 'X', 106: 'X', 107: 'X'}},
                            {'name': 'X_110', 'phase': 1, 'paulis': {97: 'X', 98: 'X', 108: 'X', 109: 'X'}},
                            {'name': 'X_111', 'phase': 1, 'paulis': {99: 'X', 100: 'X', 110: 'X', 111: 'X'}},
                            {'name': 'X_112', 'phase': 1, 'paulis': {101: 'X', 102: 'X', 112: 'X', 113: 'X'}},
                            {'name': 'X_113', 'phase': 1, 'paulis': {103: 'X', 104: 'X', 114: 'X', 115: 'X'}},
                            {'name': 'X_114', 'phase': 1, 'paulis': {105: 'X', 106: 'X', 116: 'X', 117: 'X'}},
                            {'name': 'X_115', 'phase': 1, 'paulis': {107: 'X', 108: 'X', 118: 'X', 119: 'X'}},
                            {'name': 'X_116', 'phase': 1, 'paulis': {111: 'X', 112: 'X'}},
                            {'name': 'X_117', 'phase': 1, 'paulis': {113: 'X', 114: 'X'}},
                            {'name': 'X_118', 'phase': 1, 'paulis': {115: 'X', 116: 'X'}},
                            {'name': 'X_119', 'phase': 1, 'paulis': {117: 'X', 118: 'X'}},
                            {'name': 'X_120', 'phase': 1, 'paulis': {119: 'X', 120: 'X'}}
        ]
        logical_operators = [
                            {'name': 'LZ', 'phase': 1, 'paulis': {10: 'Z', 20: 'Z', 30: 'Z', 40: 'Z', 50: 'Z', 60: 'Z', 70: 'Z', 80: 'Z', 90: 'Z', 100: 'Z', 110: 'Z'}},
                            {'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 12: 'X', 24: 'X', 36: 'X', 48: 'X', 60: 'X', 72: 'X', 84: 'X', 96: 'X', 108: 'X', 120: 'X'}},
        ]
        return code_stabilisers, logical_operators
    if code_name == (81, 1, 9):
        #9x9 surface
        code_stabilisers = [{'name': 'X_41', 'phase': 1, 'paulis': {8: 'Z', 17: 'Z'}},
                            {'name': 'X_42', 'phase': 1, 'paulis': {26: 'Z', 35: 'Z'}},
                            {'name': 'X_43', 'phase': 1, 'paulis': {44: 'Z', 53: 'Z'}},
                            {'name': 'X_44', 'phase': 1, 'paulis': {62: 'Z', 71: 'Z'}},
                            {'name': 'X_45', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 25: 'Z', 26: 'Z'}},
                            {'name': 'X_46', 'phase': 1, 'paulis': {34: 'Z', 35: 'Z', 43: 'Z', 44: 'Z'}},
                            {'name': 'X_47', 'phase': 1, 'paulis': {52: 'Z', 53: 'Z', 61: 'Z', 62: 'Z'}},
                            {'name': 'X_48', 'phase': 1, 'paulis': {70: 'Z', 71: 'Z', 79: 'Z', 80: 'Z'}},
                            {'name': 'X_49', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 15: 'Z', 16: 'Z'}},
                            {'name': 'X_50', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 33: 'Z', 34: 'Z'}},
                            {'name': 'X_51', 'phase': 1, 'paulis': {42: 'Z', 43: 'Z', 51: 'Z', 52: 'Z'}},
                            {'name': 'X_52', 'phase': 1, 'paulis': {60: 'Z', 61: 'Z', 69: 'Z', 70: 'Z'}},
                            {'name': 'X_53', 'phase': 1, 'paulis': {14: 'Z', 15: 'Z', 23: 'Z', 24: 'Z'}},
                            {'name': 'X_54', 'phase': 1, 'paulis': {32: 'Z', 33: 'Z', 41: 'Z', 42: 'Z'}},
                            {'name': 'X_55', 'phase': 1, 'paulis': {50: 'Z', 51: 'Z', 59: 'Z', 60: 'Z'}},
                            {'name': 'X_56', 'phase': 1, 'paulis': {68: 'Z', 69: 'Z', 77: 'Z', 78: 'Z'}},
                            {'name': 'X_57', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 13: 'Z', 14: 'Z'}},
                            {'name': 'X_58', 'phase': 1, 'paulis': {22: 'Z', 23: 'Z', 31: 'Z', 32: 'Z'}},
                            {'name': 'X_59', 'phase': 1, 'paulis': {40: 'Z', 41: 'Z', 49: 'Z', 50: 'Z'}},
                            {'name': 'X_60', 'phase': 1, 'paulis': {58: 'Z', 59: 'Z', 67: 'Z', 68: 'Z'}},
                            {'name': 'X_61', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 21: 'Z', 22: 'Z'}},
                            {'name': 'X_62', 'phase': 1, 'paulis': {30: 'Z', 31: 'Z', 39: 'Z', 40: 'Z'}},
                            {'name': 'X_63', 'phase': 1, 'paulis': {48: 'Z', 49: 'Z', 57: 'Z', 58: 'Z'}},
                            {'name': 'X_64', 'phase': 1, 'paulis': {66: 'Z', 67: 'Z', 75: 'Z', 76: 'Z'}},
                            {'name': 'X_65', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 11: 'Z', 12: 'Z'}},
                            {'name': 'X_66', 'phase': 1, 'paulis': {20: 'Z', 21: 'Z', 29: 'Z', 30: 'Z'}},
                            {'name': 'X_67', 'phase': 1, 'paulis': {38: 'Z', 39: 'Z', 47: 'Z', 48: 'Z'}},
                            {'name': 'X_68', 'phase': 1, 'paulis': {56: 'Z', 57: 'Z', 65: 'Z', 66: 'Z'}},
                            {'name': 'X_69', 'phase': 1, 'paulis': {10: 'Z', 11: 'Z', 19: 'Z', 20: 'Z'}},
                            {'name': 'X_70', 'phase': 1, 'paulis': {28: 'Z', 29: 'Z', 37: 'Z', 38: 'Z'}},
                            {'name': 'X_71', 'phase': 1, 'paulis': {46: 'Z', 47: 'Z', 55: 'Z', 56: 'Z'}},
                            {'name': 'X_72', 'phase': 1, 'paulis': {64: 'Z', 65: 'Z', 73: 'Z', 74: 'Z'}},
                            {'name': 'X_73', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 9: 'Z', 10: 'Z'}},
                            {'name': 'X_74', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 27: 'Z', 28: 'Z'}},
                            {'name': 'X_75', 'phase': 1, 'paulis': {36: 'Z', 37: 'Z', 45: 'Z', 46: 'Z'}},
                            {'name': 'X_76', 'phase': 1, 'paulis': {54: 'Z', 55: 'Z', 63: 'Z', 64: 'Z'}},
                            {'name': 'X_77', 'phase': 1, 'paulis': {9: 'Z', 18: 'Z'}},
                            {'name': 'X_78', 'phase': 1, 'paulis': {27: 'Z', 36: 'Z'}},
                            {'name': 'X_79', 'phase': 1, 'paulis': {45: 'Z', 54: 'Z'}},
                            {'name': 'X_80', 'phase': 1, 'paulis': {63: 'Z', 72: 'Z'}},
                            {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 1: 'X'}},
                            {'name': 'X_2', 'phase': 1, 'paulis': {2: 'X', 3: 'X'}},
                            {'name': 'X_3', 'phase': 1, 'paulis': {4: 'X', 5: 'X'}},
                            {'name': 'X_4', 'phase': 1, 'paulis': {6: 'X', 7: 'X'}},
                            {'name': 'X_5', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 10: 'X', 11: 'X'}},
                            {'name': 'X_6', 'phase': 1, 'paulis': {3: 'X', 4: 'X', 12: 'X', 13: 'X'}},
                            {'name': 'X_7', 'phase': 1, 'paulis': {5: 'X', 6: 'X', 14: 'X', 15: 'X'}},
                            {'name': 'X_8', 'phase': 1, 'paulis': {7: 'X', 8: 'X', 16: 'X', 17: 'X'}},
                            {'name': 'X_9', 'phase': 1, 'paulis': {9: 'X', 10: 'X', 18: 'X', 19: 'X'}},
                            {'name': 'X_10', 'phase': 1, 'paulis': {11: 'X', 12: 'X', 20: 'X', 21: 'X'}},
                            {'name': 'X_11', 'phase': 1, 'paulis': {13: 'X', 14: 'X', 22: 'X', 23: 'X'}},
                            {'name': 'X_12', 'phase': 1, 'paulis': {15: 'X', 16: 'X', 24: 'X', 25: 'X'}},
                            {'name': 'X_13', 'phase': 1, 'paulis': {19: 'X', 20: 'X', 28: 'X', 29: 'X'}},
                            {'name': 'X_14', 'phase': 1, 'paulis': {21: 'X', 22: 'X', 30: 'X', 31: 'X'}},
                            {'name': 'X_15', 'phase': 1, 'paulis': {23: 'X', 24: 'X', 32: 'X', 33: 'X'}},
                            {'name': 'X_16', 'phase': 1, 'paulis': {25: 'X', 26: 'X', 34: 'X', 35: 'X'}},
                            {'name': 'X_17', 'phase': 1, 'paulis': {27: 'X', 28: 'X', 36: 'X', 37: 'X'}},
                            {'name': 'X_18', 'phase': 1, 'paulis': {29: 'X', 30: 'X', 38: 'X', 39: 'X'}},
                            {'name': 'X_19', 'phase': 1, 'paulis': {31: 'X', 32: 'X', 40: 'X', 41: 'X'}},
                            {'name': 'X_20', 'phase': 1, 'paulis': {33: 'X', 34: 'X', 42: 'X', 43: 'X'}},
                            {'name': 'X_21', 'phase': 1, 'paulis': {37: 'X', 38: 'X', 46: 'X', 47: 'X'}},
                            {'name': 'X_22', 'phase': 1, 'paulis': {39: 'X', 40: 'X', 48: 'X', 49: 'X'}},
                            {'name': 'X_23', 'phase': 1, 'paulis': {41: 'X', 42: 'X', 50: 'X', 51: 'X'}},
                            {'name': 'X_24', 'phase': 1, 'paulis': {43: 'X', 44: 'X', 52: 'X', 53: 'X'}},
                            {'name': 'X_25', 'phase': 1, 'paulis': {45: 'X', 46: 'X', 54: 'X', 55: 'X'}},
                            {'name': 'X_26', 'phase': 1, 'paulis': {47: 'X', 48: 'X', 56: 'X', 57: 'X'}},
                            {'name': 'X_27', 'phase': 1, 'paulis': {49: 'X', 50: 'X', 58: 'X', 59: 'X'}},
                            {'name': 'X_28', 'phase': 1, 'paulis': {51: 'X', 52: 'X', 60: 'X', 61: 'X'}},
                            {'name': 'X_29', 'phase': 1, 'paulis': {55: 'X', 56: 'X', 64: 'X', 65: 'X'}},
                            {'name': 'X_30', 'phase': 1, 'paulis': {57: 'X', 58: 'X', 66: 'X', 67: 'X'}},
                            {'name': 'X_31', 'phase': 1, 'paulis': {59: 'X', 60: 'X', 68: 'X', 69: 'X'}},
                            {'name': 'X_32', 'phase': 1, 'paulis': {61: 'X', 62: 'X', 70: 'X', 71: 'X'}},
                            {'name': 'X_33', 'phase': 1, 'paulis': {63: 'X', 64: 'X', 72: 'X', 73: 'X'}},
                            {'name': 'X_34', 'phase': 1, 'paulis': {65: 'X', 66: 'X', 74: 'X', 75: 'X'}},
                            {'name': 'X_35', 'phase': 1, 'paulis': {67: 'X', 68: 'X', 76: 'X', 77: 'X'}},
                            {'name': 'X_36', 'phase': 1, 'paulis': {69: 'X', 70: 'X', 78: 'X', 79: 'X'}},
                            {'name': 'X_37', 'phase': 1, 'paulis': {73: 'X', 74: 'X'}},
                            {'name': 'X_38', 'phase': 1, 'paulis': {75: 'X', 76: 'X'}},
                            {'name': 'X_39', 'phase': 1, 'paulis': {77: 'X', 78: 'X'}},
                            {'name': 'X_40', 'phase': 1, 'paulis': {79: 'X', 80: 'X'}}]
        logical_operators = [{'name': 'LZ', 'phase': 1, 'paulis': {8: 'Z', 16: 'Z', 24: 'Z', 32: 'Z', 40: 'Z', 48: 'Z', 56: 'Z', 64: 'Z', 72: 'Z'}},
                            {'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 10: 'X', 20: 'X', 30: 'X', 40: 'X', 50: 'X', 60: 'X', 70: 'X', 80: 'X'}},
                ]
        return code_stabilisers, logical_operators
    if code_name == (49, 1, 7):
        #7x7 surface
        code_stabilisers = [
                            {'name': 'X_25', 'phase': 1, 'paulis': {6: 'Z', 13: 'Z'}},
                            {'name': 'X_26', 'phase': 1, 'paulis': {20: 'Z', 27: 'Z'}},
                            {'name': 'X_27', 'phase': 1, 'paulis': {34: 'Z', 41: 'Z'}},
                            {'name': 'X_28', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 19: 'Z', 20: 'Z'}},
                            {'name': 'X_29', 'phase': 1, 'paulis': {26: 'Z', 27: 'Z', 33: 'Z', 34: 'Z'}},
                            {'name': 'X_30', 'phase': 1, 'paulis': {40: 'Z', 41: 'Z', 47: 'Z', 48: 'Z'}},
                            {'name': 'X_31', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 11: 'Z', 12: 'Z'}},
                            {'name': 'X_32', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 25: 'Z', 26: 'Z'}},
                            {'name': 'X_33', 'phase': 1, 'paulis': {32: 'Z', 33: 'Z', 39: 'Z', 40: 'Z'}},
                            {'name': 'X_34', 'phase': 1, 'paulis': {10: 'Z', 11: 'Z', 17: 'Z', 18: 'Z'}},
                            {'name': 'X_35', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 31: 'Z', 32: 'Z'}},
                            {'name': 'X_36', 'phase': 1, 'paulis': {38: 'Z', 39: 'Z', 45: 'Z', 46: 'Z'}},
                            {'name': 'X_37', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 9: 'Z', 10: 'Z'}},
                            {'name': 'X_38', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 23: 'Z', 24: 'Z'}},
                            {'name': 'X_39', 'phase': 1, 'paulis': {30: 'Z', 31: 'Z', 37: 'Z', 38: 'Z'}},
                            {'name': 'X_40', 'phase': 1, 'paulis': {8: 'Z', 9: 'Z', 15: 'Z', 16: 'Z'}},
                            {'name': 'X_41', 'phase': 1, 'paulis': {22: 'Z', 23: 'Z', 29: 'Z', 30: 'Z'}},
                            {'name': 'X_42', 'phase': 1, 'paulis': {36: 'Z', 37: 'Z', 43: 'Z', 44: 'Z'}},
                            {'name': 'X_43', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 7: 'Z', 8: 'Z'}},
                            {'name': 'X_44', 'phase': 1, 'paulis': {14: 'Z', 15: 'Z', 21: 'Z', 22: 'Z'}},
                            {'name': 'X_45', 'phase': 1, 'paulis': {28: 'Z', 29: 'Z', 35: 'Z', 36: 'Z'}},
                            {'name': 'X_46', 'phase': 1, 'paulis': {7: 'Z', 14: 'Z'}},
                            {'name': 'X_47', 'phase': 1, 'paulis': {21: 'Z', 28: 'Z'}},
                            {'name': 'X_48', 'phase': 1, 'paulis': {35: 'Z', 42: 'Z'}},
                            {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 1: 'X'}},
                            {'name': 'X_2', 'phase': 1, 'paulis': {2: 'X', 3: 'X'}},
                            {'name': 'X_3', 'phase': 1, 'paulis': {4: 'X', 5: 'X'}},
                            {'name': 'X_4', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 8: 'X', 9: 'X'}},
                            {'name': 'X_5', 'phase': 1, 'paulis': {3: 'X', 4: 'X', 10: 'X', 11: 'X'}},
                            {'name': 'X_6', 'phase': 1, 'paulis': {5: 'X', 6: 'X', 12: 'X', 13: 'X'}},
                            {'name': 'X_7', 'phase': 1, 'paulis': {7: 'X', 8: 'X', 14: 'X', 15: 'X'}},
                            {'name': 'X_8', 'phase': 1, 'paulis': {9: 'X', 10: 'X', 16: 'X', 17: 'X'}},
                            {'name': 'X_9', 'phase': 1, 'paulis': {11: 'X', 12: 'X', 18: 'X', 19: 'X'}},
                            {'name': 'X_10', 'phase': 1, 'paulis': {15: 'X', 16: 'X', 22: 'X', 23: 'X'}},
                            {'name': 'X_11', 'phase': 1, 'paulis': {17: 'X', 18: 'X', 24: 'X', 25: 'X'}},
                            {'name': 'X_12', 'phase': 1, 'paulis': {19: 'X', 20: 'X', 26: 'X', 27: 'X'}},
                            {'name': 'X_13', 'phase': 1, 'paulis': {21: 'X', 22: 'X', 28: 'X', 29: 'X'}},
                            {'name': 'X_14', 'phase': 1, 'paulis': {23: 'X', 24: 'X', 30: 'X', 31: 'X'}},
                            {'name': 'X_15', 'phase': 1, 'paulis': {25: 'X', 26: 'X', 32: 'X', 33: 'X'}},
                            {'name': 'X_16', 'phase': 1, 'paulis': {29: 'X', 30: 'X', 36: 'X', 37: 'X'}},
                            {'name': 'X_17', 'phase': 1, 'paulis': {31: 'X', 32: 'X', 38: 'X', 39: 'X'}},
                            {'name': 'X_18', 'phase': 1, 'paulis': {33: 'X', 34: 'X', 40: 'X', 41: 'X'}},
                            {'name': 'X_19', 'phase': 1, 'paulis': {35: 'X', 36: 'X', 42: 'X', 43: 'X'}},
                            {'name': 'X_20', 'phase': 1, 'paulis': {37: 'X', 38: 'X', 44: 'X', 45: 'X'}},
                            {'name': 'X_21', 'phase': 1, 'paulis': {39: 'X', 40: 'X', 46: 'X', 47: 'X'}},
                            {'name': 'X_22', 'phase': 1, 'paulis': {43: 'X', 44: 'X'}},
                            {'name': 'X_23', 'phase': 1, 'paulis': {45: 'X', 46: 'X'}},
                            {'name': 'X_24', 'phase': 1, 'paulis': {47: 'X', 48: 'X'}},]

        logical_operators = [{'name': 'LZ', 'phase': 1, 'paulis': {6: 'Z', 12: 'Z', 18: 'Z', 24: 'Z', 30: 'Z', 36: 'Z', 42: 'Z'}},
                            {'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 8: 'X', 16: 'X', 24: 'X', 32: 'X', 40: 'X', 48: 'X'}}
                            ]
        return code_stabilisers, logical_operators
    if code_name == (25, 1, 5):
        #5x5 surface
        code_stabilisers = [
                            {'name': 'X_13', 'phase': 1, 'paulis': {4: 'Z', 9: 'Z'}},
                            {'name': 'X_14', 'phase': 1, 'paulis': {14: 'Z', 19: 'Z'}},
                            {'name': 'X_15', 'phase': 1, 'paulis': {8: 'Z', 9: 'Z', 13: 'Z', 14: 'Z'}},
                            {'name': 'X_16', 'phase': 1, 'paulis': {18: 'Z', 19: 'Z', 23: 'Z', 24: 'Z'}},
                            {'name': 'X_17', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 7: 'Z', 8: 'Z'}},
                            {'name': 'X_18', 'phase': 1, 'paulis': {12: 'Z', 13: 'Z', 17: 'Z', 18: 'Z'}},
                            {'name': 'X_19', 'phase': 1, 'paulis': {6: 'Z', 7: 'Z', 11: 'Z', 12: 'Z'}},
                            {'name': 'X_20', 'phase': 1, 'paulis': {16: 'Z', 17: 'Z', 21: 'Z', 22: 'Z'}},
                            {'name': 'X_21', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 5: 'Z', 6: 'Z'}},
                            {'name': 'X_22', 'phase': 1, 'paulis': {10: 'Z', 11: 'Z', 15: 'Z', 16: 'Z'}},
                            {'name': 'X_23', 'phase': 1, 'paulis': {5: 'Z', 10: 'Z'}},
                            {'name': 'X_24', 'phase': 1, 'paulis': {15: 'Z', 20: 'Z'}},
                            {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 1: 'X'}},
                            {'name': 'X_2', 'phase': 1, 'paulis': {2: 'X', 3: 'X'}},
                            {'name': 'X_3', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 6: 'X', 7: 'X'}},
                            {'name': 'X_4', 'phase': 1, 'paulis': {3: 'X', 4: 'X', 8: 'X', 9: 'X'}},
                            {'name': 'X_5', 'phase': 1, 'paulis': {5: 'X', 6: 'X', 10: 'X', 11: 'X'}},
                            {'name': 'X_6', 'phase': 1, 'paulis': {7: 'X', 8: 'X', 12: 'X', 13: 'X'}},
                            {'name': 'X_7', 'phase': 1, 'paulis': {11: 'X', 12: 'X', 16: 'X', 17: 'X'}},
                            {'name': 'X_8', 'phase': 1, 'paulis': {13: 'X', 14: 'X', 18: 'X', 19: 'X'}},
                            {'name': 'X_9', 'phase': 1, 'paulis': {15: 'X', 16: 'X', 20: 'X', 21: 'X'}},
                            {'name': 'X_10', 'phase': 1, 'paulis': {17: 'X', 18: 'X', 22: 'X', 23: 'X'}},
                            {'name': 'X_11', 'phase': 1, 'paulis': {21: 'X', 22: 'X'}},
                            {'name': 'X_12', 'phase': 1, 'paulis': {23: 'X', 24: 'X'}},
                            ]
        logical_operators = [
                            {'name': 'LZ', 'phase': 1, 'paulis': {4: 'Z', 8: 'Z', 12: 'Z', 16: 'Z', 20: 'Z'}},
                            {'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 6: 'X', 12: 'X', 18: 'X', 24: 'X'}}
                        ]
        return code_stabilisers, logical_operators
    if code_name == (9, 1, 3):
        # 3x3 surface
        code_stabilisers = [{'name': 'X_5', 'phase': 1, 'paulis': {2: 'Z', 5: 'Z'}},
                            {'name': 'X_6', 'phase': 1, 'paulis': {4: 'Z', 5: 'Z', 7: 'Z', 8: 'Z'}},
                            {'name': 'X_7', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 3: 'Z', 4: 'Z'}},
                            {'name': 'X_8', 'phase': 1, 'paulis': {3: 'Z', 6: 'Z'}},
                            {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 1: 'X'}},
                            {'name': 'X_2', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 4: 'X', 5: 'X'}},
                            {'name': 'X_3', 'phase': 1, 'paulis': {3: 'X', 4: 'X', 6: 'X', 7: 'X'}},
                            {'name': 'X_4', 'phase': 1, 'paulis': {7: 'X', 8: 'X'}}]
        logical_operators = [ {'name': 'LZ', 'phase': 1, 'paulis': {2: 'Z', 4: 'Z', 6: 'Z'}},
                         {'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 4: 'X', 8: 'X'}}
                        ]
        return code_stabilisers, logical_operators
    if code_name == (40, 10, 4):
        #hyperbolic
        code_stabilisers =[{'name': 'stab1', 'phase': 1, 'paulis': {8: 'X', 12: 'X', 25: 'X', 26: 'X', 29: 'X'}}, {'name': 'stab2', 'phase': 1, 'paulis': {12: 'X', 16: 'X', 24: 'X', 27: 'X', 38: 'X'}}, {'name': 'stab3', 'phase': 1, 'paulis': {5: 'X', 19: 'X', 21: 'X', 29: 'X', 35: 'X'}}, {'name': 'stab4', 'phase': 1, 'paulis': {10: 'X', 27: 'X', 28: 'X', 33: 'X', 39: 'X'}}, {'name': 'stab5', 'phase': 1, 'paulis': {0: 'X', 3: 'X', 4: 'X', 6: 'X', 23: 'X'}}, {'name': 'stab6', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 15: 'X', 35: 'X', 38: 'X'}}, {'name': 'stab7', 'phase': 1, 'paulis': {19: 'X', 23: 'X', 30: 'X', 32: 'X', 33: 'X'}}, {'name': 'stab8', 'phase': 1, 'paulis': {8: 'X', 13: 'X', 17: 'X', 30: 'X', 37: 'X'}}, {'name': 'stab9', 'phase': 1, 'paulis': {2: 'X', 7: 'X', 21: 'X', 22: 'X', 34: 'X'}}, {'name': 'stab10', 'phase': 1, 'paulis': {4: 'X', 7: 'X', 9: 'X', 17: 'X', 24: 'X'}}, {'name': 'stab11', 'phase': 1, 'paulis': {3: 'X', 18: 'X', 26: 'X', 31: 'X', 36: 'X'}}, {'name': 'stab12', 'phase': 1, 'paulis': {5: 'X', 9: 'X', 20: 'X', 36: 'X', 39: 'X'}}, {'name': 'stab13', 'phase': 1, 'paulis': {1: 'X', 11: 'X', 13: 'X', 14: 'X', 20: 'X'}}, {'name': 'stab14', 'phase': 1, 'paulis': {15: 'X', 18: 'X', 22: 'X', 28: 'X', 37: 'X'}}, {'name': 'stab15', 'phase': 1, 'paulis': {14: 'X', 16: 'X', 31: 'X', 32: 'X', 34: 'X'}}, {'name': 'stab17', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 11: 'Z', 21: 'Z', 35: 'Z'}}, {'name': 'stab18', 'phase': 1, 'paulis': {0: 'Z', 6: 'Z', 10: 'Z', 27: 'Z', 38: 'Z'}}, {'name': 'stab19', 'phase': 1, 'paulis': {5: 'Z', 15: 'Z', 28: 'Z', 35: 'Z', 39: 'Z'}}, {'name': 'stab20', 'phase': 1, 'paulis': {6: 'Z', 11: 'Z', 14: 'Z', 23: 'Z', 32: 'Z'}}, {'name': 'stab21', 'phase': 1, 'paulis': {9: 'Z', 17: 'Z', 18: 'Z', 36: 'Z', 37: 'Z'}}, {'name': 'stab22', 'phase': 1, 'paulis': {5: 'Z', 13: 'Z', 19: 'Z', 20: 'Z', 30: 'Z'}}, {'name': 'stab23', 'phase': 1, 'paulis': {12: 'Z', 18: 'Z', 26: 'Z', 27: 'Z', 28: 'Z'}}, {'name': 'stab24', 'phase': 1, 'paulis': {3: 'Z', 4: 'Z', 16: 'Z', 24: 'Z', 31: 'Z'}}, {'name': 'stab25', 'phase': 1, 'paulis': {10: 'Z', 19: 'Z', 25: 'Z', 29: 'Z', 33: 'Z'}}, {'name': 'stab26', 'phase': 1, 'paulis': {3: 'Z', 23: 'Z', 33: 'Z', 36: 'Z', 39: 'Z'}}, {'name': 'stab27', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 4: 'Z', 9: 'Z', 20: 'Z'}}, {'name': 'stab28', 'phase': 1, 'paulis': {8: 'Z', 21: 'Z', 22: 'Z', 29: 'Z', 37: 'Z'}}, {'name': 'stab29', 'phase': 1, 'paulis': {7: 'Z', 13: 'Z', 14: 'Z', 17: 'Z', 34: 'Z'}}, {'name': 'stab30', 'phase': 1, 'paulis': {7: 'Z', 15: 'Z', 22: 'Z', 24: 'Z', 38: 'Z'}}, {'name': 'stab31', 'phase': 1, 'paulis': {2: 'Z', 12: 'Z', 16: 'Z', 25: 'Z', 34: 'Z'}} ]
        logical_operators =[ {'name': 'La0', 'phase': 1, 'paulis': {1: 'Z', 14: 'Z', 15: 'Z', 22: 'Z', 34: 'Z'}},
                        {'name': 'La1', 'phase': 1, 'paulis': {9: 'Z', 14: 'Z', 16: 'Z', 20: 'Z', 24: 'Z'}},
                        {'name': 'La2', 'phase': 1, 'paulis': {16: 'Z', 27: 'Z', 32: 'Z', 33: 'Z'}},
                        {'name': 'La3', 'phase': 1, 'paulis': {22: 'Z', 28: 'Z', 32: 'Z', 33: 'Z', 34: 'Z'}},
                        {'name': 'La4', 'phase': 1, 'paulis': {1: 'Z', 8: 'Z', 14: 'Z', 22: 'Z', 29: 'Z', 34: 'Z', 35: 'Z', 37: 'Z'}},
                        {'name': 'La5', 'phase': 1, 'paulis': {22: 'Z', 30: 'Z', 32: 'Z', 34: 'Z', 37: 'Z'}},
                        {'name': 'La6', 'phase': 1, 'paulis': {18: 'Z', 22: 'Z', 31: 'Z', 34: 'Z'}},
                        {'name': 'La7', 'phase': 1, 'paulis': {14: 'Z', 18: 'Z', 20: 'Z', 22: 'Z', 34: 'Z', 36: 'Z'}},
                        {'name': 'La8', 'phase': 1, 'paulis': {1: 'Z', 14: 'Z', 16: 'Z', 38: 'Z'}},
                        {'name': 'La9', 'phase': 1, 'paulis': {14: 'Z', 20: 'Z', 32: 'Z', 33: 'Z', 39: 'Z'}}]
        return code_stabilisers, logical_operators
    if code_name == (47, 1, 11):
        #[[47, 1, 11]]
        code_stabilisers = [{'name': 'X_24', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 4: 'Z', 6: 'Z', 9: 'Z', 12: 'Z', 13: 'Z', 15: 'Z', 16: 'Z', 19: 'Z', 20: 'Z', 24: 'Z'}},
                        {'name': 'X_25', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 5: 'Z', 8: 'Z', 11: 'Z', 12: 'Z', 14: 'Z', 15: 'Z', 18: 'Z', 19: 'Z', 23: 'Z', 46: 'Z'}},
                        {'name': 'X_26', 'phase': 1, 'paulis': {2: 'Z', 4: 'Z', 7: 'Z', 10: 'Z', 11: 'Z', 13: 'Z', 14: 'Z', 17: 'Z', 18: 'Z', 22: 'Z', 45: 'Z', 46: 'Z'}},
                        {'name': 'X_27', 'phase': 1, 'paulis': {1: 'Z', 3: 'Z', 6: 'Z', 9: 'Z', 10: 'Z', 12: 'Z', 13: 'Z', 16: 'Z', 17: 'Z', 21: 'Z', 44: 'Z', 45: 'Z'}},
                        {'name': 'X_28', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 5: 'Z', 8: 'Z', 9: 'Z', 11: 'Z', 12: 'Z', 15: 'Z', 16: 'Z', 20: 'Z', 43: 'Z', 44: 'Z'}},
                        {'name': 'X_29', 'phase': 1, 'paulis': {1: 'Z', 4: 'Z', 7: 'Z', 8: 'Z', 10: 'Z', 11: 'Z', 14: 'Z', 15: 'Z', 19: 'Z', 42: 'Z', 43: 'Z', 46: 'Z'}},
                        {'name': 'X_30', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 6: 'Z', 7: 'Z', 9: 'Z', 10: 'Z', 13: 'Z', 14: 'Z', 18: 'Z', 41: 'Z', 42: 'Z', 45: 'Z'}},
                        {'name': 'X_31', 'phase': 1, 'paulis': {2: 'Z', 5: 'Z', 6: 'Z', 8: 'Z', 9: 'Z', 12: 'Z', 13: 'Z', 17: 'Z', 40: 'Z', 41: 'Z', 44: 'Z', 46: 'Z'}},
                        {'name': 'X_32', 'phase': 1, 'paulis': {1: 'Z', 4: 'Z', 5: 'Z', 7: 'Z', 8: 'Z', 11: 'Z', 12: 'Z', 16: 'Z', 39: 'Z', 40: 'Z', 43: 'Z', 45: 'Z'}},
                        {'name': 'X_33', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 4: 'Z', 6: 'Z', 7: 'Z', 10: 'Z', 11: 'Z', 15: 'Z', 38: 'Z', 39: 'Z', 42: 'Z', 44: 'Z'}},
                        {'name': 'X_34', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 9: 'Z', 10: 'Z', 14: 'Z', 37: 'Z', 38: 'Z', 41: 'Z', 43: 'Z', 46: 'Z'}},
                        {'name': 'X_35', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 4: 'Z', 5: 'Z', 8: 'Z', 9: 'Z', 13: 'Z', 36: 'Z', 37: 'Z', 40: 'Z', 42: 'Z', 45: 'Z'}},
                        {'name': 'X_36', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 3: 'Z', 4: 'Z', 7: 'Z', 8: 'Z', 12: 'Z', 35: 'Z', 36: 'Z', 39: 'Z', 41: 'Z', 44: 'Z'}},
                        {'name': 'X_37', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 3: 'Z', 6: 'Z', 7: 'Z', 11: 'Z', 34: 'Z', 35: 'Z', 38: 'Z', 40: 'Z', 43: 'Z', 46: 'Z'}},
                        {'name': 'X_38', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 5: 'Z', 6: 'Z', 10: 'Z', 33: 'Z', 34: 'Z', 37: 'Z', 39: 'Z', 42: 'Z', 45: 'Z', 46: 'Z'}},
                        {'name': 'X_39', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 4: 'Z', 5: 'Z', 9: 'Z', 32: 'Z', 33: 'Z', 36: 'Z', 38: 'Z', 41: 'Z', 44: 'Z', 45: 'Z'}},
                        {'name': 'X_40', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 4: 'Z', 8: 'Z', 31: 'Z', 32: 'Z', 35: 'Z', 37: 'Z', 40: 'Z', 43: 'Z', 44: 'Z', 46: 'Z'}},
                        {'name': 'X_41', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 7: 'Z', 30: 'Z', 31: 'Z', 34: 'Z', 36: 'Z', 39: 'Z', 42: 'Z', 43: 'Z', 45: 'Z', 46: 'Z'}},
                        {'name': 'X_42', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 6: 'Z', 29: 'Z', 30: 'Z', 33: 'Z', 35: 'Z', 38: 'Z', 41: 'Z', 42: 'Z', 44: 'Z', 45: 'Z'}},
                        {'name': 'X_43', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 5: 'Z', 28: 'Z', 29: 'Z', 32: 'Z', 34: 'Z', 37: 'Z', 40: 'Z', 41: 'Z', 43: 'Z', 44: 'Z'}},
                        {'name': 'X_44', 'phase': 1, 'paulis': {0: 'Z', 4: 'Z', 27: 'Z', 28: 'Z', 31: 'Z', 33: 'Z', 36: 'Z', 39: 'Z', 40: 'Z', 42: 'Z', 43: 'Z', 46: 'Z'}},
                        {'name': 'X_45', 'phase': 1, 'paulis': {3: 'Z', 26: 'Z', 27: 'Z', 30: 'Z', 32: 'Z', 35: 'Z', 38: 'Z', 39: 'Z', 41: 'Z', 42: 'Z', 45: 'Z', 46: 'Z'}},
                        {'name': 'X_46', 'phase': 1, 'paulis': {2: 'Z', 25: 'Z', 26: 'Z', 29: 'Z', 31: 'Z', 34: 'Z', 37: 'Z', 38: 'Z', 40: 'Z', 41: 'Z', 44: 'Z', 45: 'Z'}},
                        {'name': 'X_1', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 4: 'X', 6: 'X', 9: 'X', 12: 'X', 13: 'X', 15: 'X', 16: 'X', 19: 'X', 20: 'X', 24: 'X'}},
                        {'name': 'X_2', 'phase': 1, 'paulis': {0: 'X', 3: 'X', 5: 'X', 8: 'X', 11: 'X', 12: 'X', 14: 'X', 15: 'X', 18: 'X', 19: 'X', 23: 'X', 46: 'X'}},
                        {'name': 'X_3', 'phase': 1, 'paulis': {2: 'X', 4: 'X', 7: 'X', 10: 'X', 11: 'X', 13: 'X', 14: 'X', 17: 'X', 18: 'X', 22: 'X', 45: 'X', 46: 'X'}},
                        {'name': 'X_4', 'phase': 1, 'paulis': {1: 'X', 3: 'X', 6: 'X', 9: 'X', 10: 'X', 12: 'X', 13: 'X', 16: 'X', 17: 'X', 21: 'X', 44: 'X', 45: 'X'}},
                        {'name': 'X_5', 'phase': 1, 'paulis': {0: 'X', 2: 'X', 5: 'X', 8: 'X', 9: 'X', 11: 'X', 12: 'X', 15: 'X', 16: 'X', 20: 'X', 43: 'X', 44: 'X'}},
                        {'name': 'X_6', 'phase': 1, 'paulis': {1: 'X', 4: 'X', 7: 'X', 8: 'X', 10: 'X', 11: 'X', 14: 'X', 15: 'X', 19: 'X', 42: 'X', 43: 'X', 46: 'X'}},
                        {'name': 'X_7', 'phase': 1, 'paulis': {0: 'X', 3: 'X', 6: 'X', 7: 'X', 9: 'X', 10: 'X', 13: 'X', 14: 'X', 18: 'X', 41: 'X', 42: 'X', 45: 'X'}},
                        {'name': 'X_8', 'phase': 1, 'paulis': {2: 'X', 5: 'X', 6: 'X', 8: 'X', 9: 'X', 12: 'X', 13: 'X', 17: 'X', 40: 'X', 41: 'X', 44: 'X', 46: 'X'}},
                        {'name': 'X_9', 'phase': 1, 'paulis': {1: 'X', 4: 'X', 5: 'X', 7: 'X', 8: 'X', 11: 'X', 12: 'X', 16: 'X', 39: 'X', 40: 'X', 43: 'X', 45: 'X'}},
                        {'name': 'X_10', 'phase': 1, 'paulis': {0: 'X', 3: 'X', 4: 'X', 6: 'X', 7: 'X', 10: 'X', 11: 'X', 15: 'X', 38: 'X', 39: 'X', 42: 'X', 44: 'X'}},
                        {'name': 'X_11', 'phase': 1, 'paulis': {2: 'X', 3: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 14: 'X', 37: 'X', 38: 'X', 41: 'X', 43: 'X', 46: 'X'}},
                        {'name': 'X_12', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 4: 'X', 5: 'X', 8: 'X', 9: 'X', 13: 'X', 36: 'X', 37: 'X', 40: 'X', 42: 'X', 45: 'X'}},
                        {'name': 'X_13', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 3: 'X', 4: 'X', 7: 'X', 8: 'X', 12: 'X', 35: 'X', 36: 'X', 39: 'X', 41: 'X', 44: 'X'}},
                        {'name': 'X_14', 'phase': 1, 'paulis': {0: 'X', 2: 'X', 3: 'X', 6: 'X', 7: 'X', 11: 'X', 34: 'X', 35: 'X', 38: 'X', 40: 'X', 43: 'X', 46: 'X'}},
                        {'name': 'X_15', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 5: 'X', 6: 'X', 10: 'X', 33: 'X', 34: 'X', 37: 'X', 39: 'X', 42: 'X', 45: 'X', 46: 'X'}},
                        {'name': 'X_16', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 4: 'X', 5: 'X', 9: 'X', 32: 'X', 33: 'X', 36: 'X', 38: 'X', 41: 'X', 44: 'X', 45: 'X'}},
                        {'name': 'X_17', 'phase': 1, 'paulis': {0: 'X', 3: 'X', 4: 'X', 8: 'X', 31: 'X', 32: 'X', 35: 'X', 37: 'X', 40: 'X', 43: 'X', 44: 'X', 46: 'X'}},
                        {'name': 'X_18', 'phase': 1, 'paulis': {2: 'X', 3: 'X', 7: 'X', 30: 'X', 31: 'X', 34: 'X', 36: 'X', 39: 'X', 42: 'X', 43: 'X', 45: 'X', 46: 'X'}},
                        {'name': 'X_19', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 6: 'X', 29: 'X', 30: 'X', 33: 'X', 35: 'X', 38: 'X', 41: 'X', 42: 'X', 44: 'X', 45: 'X'}},
                        {'name': 'X_20', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 5: 'X', 28: 'X', 29: 'X', 32: 'X', 34: 'X', 37: 'X', 40: 'X', 41: 'X', 43: 'X', 44: 'X'}},
                        {'name': 'X_21', 'phase': 1, 'paulis': {0: 'X', 4: 'X', 27: 'X', 28: 'X', 31: 'X', 33: 'X', 36: 'X', 39: 'X', 40: 'X', 42: 'X', 43: 'X', 46: 'X'}},
                        {'name': 'X_22', 'phase': 1, 'paulis': {3: 'X', 26: 'X', 27: 'X', 30: 'X', 32: 'X', 35: 'X', 38: 'X', 39: 'X', 41: 'X', 42: 'X', 45: 'X', 46: 'X'}},
                        {'name': 'X_23', 'phase': 1, 'paulis': {2: 'X', 25: 'X', 26: 'X', 29: 'X', 31: 'X', 34: 'X', 37: 'X', 38: 'X', 40: 'X', 41: 'X', 44: 'X', 45: 'X'}}]
        logical_operators = [{'name': 'LX', 'phase': 1, 'paulis': {23: 'X', 27: 'X', 28: 'X', 32: 'X', 33: 'X', 34: 'X', 36: 'X', 37: 'X', 39: 'X', 40: 'X', 41: 'X', 43: 'X', 44: 'X', 45: 'X', 46: 'X'}},
                        {'name': 'LZ', 'phase': 1, 'paulis': {23: 'Z', 27: 'Z', 28: 'Z', 32: 'Z', 33: 'Z', 34: 'Z', 36: 'Z', 37: 'Z', 39: 'Z', 40: 'Z', 41: 'Z', 43: 'Z', 44: 'Z', 45: 'Z', 46: 'Z'}}]
        
        return code_stabilisers, logical_operators
    if code_name == (49, 1, 5):
        #[[49,1,5]]
        code_stabilisers =[ {'name': 'Zn0', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 3: 'Z', 4: 'Z'}},
                        {'name': 'Zo0', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 3: 'Z', 5: 'Z'}},
                        {'name': 'Zp0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 3: 'Z', 6: 'Z'}},
                        {'name': 'Zq0', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 7: 'Z', 8: 'Z'}},
                        {'name': 'Zr0', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 7: 'Z', 9: 'Z'}},
                        {'name': 'Zs0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 7: 'Z', 10: 'Z'}},
                        {'name': 'Zt0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z', 7: 'Z', 11: 'Z'}},
                        {'name': 'Zu0', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 7: 'Z', 12: 'Z'}},
                        {'name': 'Zv0', 'phase': 1, 'paulis': {1: 'Z', 3: 'Z', 7: 'Z', 13: 'Z'}},
                        {'name': 'Zw0', 'phase': 1, 'paulis': {2: 'Z', 3: 'Z', 7: 'Z', 14: 'Z'}},
                        {'name': 'Zx0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 17: 'Z', 18: 'Z'}},
                        {'name': 'Zy0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 19: 'Z', 20: 'Z'}},
                        {'name': 'Zz0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 21: 'Z', 22: 'Z'}},
                        {'name': 'ZA0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 16: 'Z', 17: 'Z', 19: 'Z', 21: 'Z', 23: 'Z'}},
                        {'name': 'ZB0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 15: 'Z', 17: 'Z', 19: 'Z', 21: 'Z', 24: 'Z'}},
                        {'name': 'ZC0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 25: 'Z', 26: 'Z'}},
                        {'name': 'ZD0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 16: 'Z', 17: 'Z', 19: 'Z', 25: 'Z', 27: 'Z'}},
                        {'name': 'ZE0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 15: 'Z', 17: 'Z', 19: 'Z', 25: 'Z', 28: 'Z'}},
                        {'name': 'ZF0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 15: 'Z', 16: 'Z', 17: 'Z', 19: 'Z', 21: 'Z', 25: 'Z', 29: 'Z'}},
                        {'name': 'ZG0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 17: 'Z', 19: 'Z', 21: 'Z', 25: 'Z', 30: 'Z'}},
                        {'name': 'ZH0', 'phase': 1, 'paulis': {15: 'Z', 21: 'Z', 25: 'Z', 31: 'Z'}},
                        {'name': 'ZI0', 'phase': 1, 'paulis': {16: 'Z', 21: 'Z', 25: 'Z', 32: 'Z'}},
                        {'name': 'ZJ0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 33: 'Z', 34: 'Z'}},
                        {'name': 'ZK0', 'phase': 1, 'paulis': {17: 'Z', 19: 'Z', 33: 'Z', 35: 'Z'}},
                        {'name': 'ZL0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 17: 'Z', 19: 'Z', 33: 'Z', 36: 'Z'}},
                        {'name': 'ZM0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 37: 'Z', 38: 'Z'}},
                        {'name': 'ZN0', 'phase': 1, 'paulis': {17: 'Z', 19: 'Z', 37: 'Z', 39: 'Z'}},
                        {'name': 'ZO0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 17: 'Z', 19: 'Z', 37: 'Z', 40: 'Z'}},
                        {'name': 'ZP0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 41: 'Z', 42: 'Z'}},
                        {'name': 'ZQ0', 'phase': 1, 'paulis': {17: 'Z', 19: 'Z', 41: 'Z', 43: 'Z'}},
                        {'name': 'ZR0', 'phase': 1, 'paulis': {15: 'Z', 16: 'Z', 17: 'Z', 19: 'Z', 41: 'Z', 44: 'Z'}},
                        {'name': 'ZS0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 15: 'Z', 16: 'Z', 17: 'Z', 33: 'Z', 37: 'Z', 41: 'Z', 45: 'Z'}},
                        {'name': 'ZT0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 17: 'Z', 33: 'Z', 37: 'Z', 41: 'Z', 46: 'Z'}},
                        {'name': 'ZU0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 15: 'Z', 16: 'Z', 19: 'Z', 33: 'Z', 37: 'Z', 41: 'Z', 47: 'Z'}},
                        {'name': 'ZV0', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 19: 'Z', 33: 'Z', 37: 'Z', 41: 'Z', 48: 'Z'}},
                        {'name': 'Xa0', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 4: 'X', 5: 'X', 6: 'X', 7: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 12: 'X', 13: 'X', 14: 'X', 16: 'X', 18: 'X', 20: 'X', 22: 'X', 24: 'X', 26: 'X', 28: 'X', 30: 'X', 32: 'X', 34: 'X', 36: 'X', 38: 'X', 40: 'X', 42: 'X', 44: 'X', 46: 'X', 48: 'X'}},
                        {'name': 'Xb0', 'phase': 1, 'paulis': {19: 'X', 20: 'X', 21: 'X', 22: 'X', 25: 'X', 26: 'X', 29: 'X', 30: 'X', 35: 'X', 36: 'X', 39: 'X', 40: 'X', 43: 'X', 44: 'X', 47: 'X', 48: 'X'}},
                        {'name': 'Xc0', 'phase': 1, 'paulis': {15: 'X', 16: 'X', 23: 'X', 24: 'X', 27: 'X', 28: 'X', 31: 'X', 32: 'X'}},
                        {'name': 'Xd0', 'phase': 1, 'paulis': {33: 'X', 34: 'X', 35: 'X', 36: 'X', 45: 'X', 46: 'X', 47: 'X', 48: 'X'}},
                        {'name': 'Xe0', 'phase': 1, 'paulis': {17: 'X', 18: 'X', 19: 'X', 20: 'X', 37: 'X', 38: 'X', 39: 'X', 40: 'X'}},
                        {'name': 'Xf0', 'phase': 1, 'paulis': {21: 'X', 22: 'X', 23: 'X', 24: 'X', 29: 'X', 30: 'X', 31: 'X', 32: 'X'}},
                        {'name': 'Xg0', 'phase': 1, 'paulis': {25: 'X', 26: 'X', 27: 'X', 28: 'X', 29: 'X', 30: 'X', 31: 'X', 32: 'X'}},
                        {'name': 'Xh0', 'phase': 1, 'paulis': {33: 'X', 34: 'X', 35: 'X', 36: 'X', 37: 'X', 38: 'X', 39: 'X', 40: 'X'}},
                        {'name': 'Xi0', 'phase': 1, 'paulis': {41: 'X', 42: 'X', 43: 'X', 44: 'X', 45: 'X', 46: 'X', 47: 'X', 48: 'X'}},
                        {'name': 'Xj0', 'phase': 1, 'paulis': {0: 'X', 2: 'X', 4: 'X', 6: 'X', 8: 'X', 10: 'X', 12: 'X', 14: 'X'}},
                        {'name': 'Xk0', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 5: 'X', 6: 'X', 9: 'X', 10: 'X', 13: 'X', 14: 'X'}},
                        {'name': 'Xl0', 'phase': 1, 'paulis': {3: 'X', 4: 'X', 5: 'X', 6: 'X', 11: 'X', 12: 'X', 13: 'X', 14: 'X'}},
                        {'name': 'Xm0', 'phase': 1, 'paulis': {7: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 12: 'X', 13: 'X', 14: 'X'}}
                        ]
        logical_operators =[
                        {'name': 'LZ', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 15: 'Z', 16: 'Z'}},
                        {'name': 'LX', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 4: 'X', 5: 'X', 6: 'X', 15: 'X', 16: 'X', 17: 'X', 18: 'X', 19: 'X', 20: 'X', 21: 'X', 22: 'X', 23: 'X', 24: 'X'}},
                        ]
        return code_stabilisers, logical_operators
    
    if code_name == (95, 1, 7):
        code_stabilisers = [
                            {'name': 'Zc1', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z', 6: 'Z', 9: 'Z', 11: 'Z', 22: 'Z', 23: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 29: 'Z', 32: 'Z', 34: 'Z', 45: 'Z'}},
                            {'name': 'Zc2', 'phase': 1, 'paulis': {3: 'Z', 5: 'Z', 6: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 11: 'Z', 21: 'Z', 26: 'Z', 28: 'Z', 29: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 34: 'Z', 44: 'Z'}},
                            {'name': 'Zc3', 'phase': 1, 'paulis': {2: 'Z', 4: 'Z', 5: 'Z', 7: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 20: 'Z', 25: 'Z', 27: 'Z', 28: 'Z', 30: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 43: 'Z'}},
                            {'name': 'Zc4', 'phase': 1, 'paulis': {1: 'Z', 3: 'Z', 4: 'Z', 6: 'Z', 7: 'Z', 8: 'Z', 9: 'Z', 19: 'Z', 24: 'Z', 26: 'Z', 27: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 32: 'Z', 42: 'Z'}},
                            {'name': 'Zc5', 'phase': 1, 'paulis': {0: 'Z', 2: 'Z', 3: 'Z', 5: 'Z', 6: 'Z', 7: 'Z', 8: 'Z', 18: 'Z', 23: 'Z', 25: 'Z', 26: 'Z', 28: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 41: 'Z'}},
                            {'name': 'Zc6', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 4: 'Z', 5: 'Z', 7: 'Z', 9: 'Z', 11: 'Z', 17: 'Z', 23: 'Z', 26: 'Z', 27: 'Z', 28: 'Z', 30: 'Z', 32: 'Z', 34: 'Z', 40: 'Z'}},
                            {'name': 'Zc7', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 4: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 11: 'Z', 16: 'Z', 23: 'Z', 24: 'Z', 27: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 34: 'Z', 39: 'Z'}},
                            {'name': 'Zc8', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 6: 'Z', 7: 'Z', 8: 'Z', 10: 'Z', 11: 'Z', 15: 'Z', 24: 'Z', 25: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 33: 'Z', 34: 'Z', 38: 'Z'}},
                            {'name': 'Zc9', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 5: 'Z', 6: 'Z', 7: 'Z', 9: 'Z', 10: 'Z', 14: 'Z', 23: 'Z', 24: 'Z', 28: 'Z', 29: 'Z', 30: 'Z', 32: 'Z', 33: 'Z', 37: 'Z'}},
                            {'name': 'Zc10', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 3: 'Z', 4: 'Z', 5: 'Z', 8: 'Z', 11: 'Z', 13: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z', 28: 'Z', 31: 'Z', 34: 'Z', 36: 'Z'}},
                            {'name': 'Zc11', 'phase': 1, 'paulis': {0: 'Z', 1: 'Z', 2: 'Z', 3: 'Z', 4: 'Z', 7: 'Z', 10: 'Z', 12: 'Z', 23: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z', 30: 'Z', 33: 'Z', 35: 'Z'}},
                            {'name': 'Zc12', 'phase': 1, 'paulis': {23: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z', 28: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 34: 'Z', 35: 'Z', 36: 'Z', 37: 'Z', 38: 'Z', 39: 'Z', 40: 'Z', 41: 'Z', 42: 'Z', 43: 'Z', 44: 'Z', 45: 'Z', 46: 'Z', 47: 'Z', 48: 'Z', 49: 'Z', 50: 'Z', 51: 'Z', 52: 'Z', 53: 'Z', 54: 'Z', 55: 'Z', 56: 'Z', 57: 'Z', 58: 'Z', 59: 'Z', 60: 'Z', 61: 'Z', 62: 'Z', 63: 'Z', 64: 'Z', 65: 'Z', 66: 'Z', 67: 'Z', 68: 'Z', 69: 'Z', 70: 'Z', 71: 'Z', 72: 'Z', 73: 'Z', 74: 'Z', 75: 'Z', 76: 'Z', 77: 'Z', 78: 'Z', 79: 'Z', 80: 'Z', 81: 'Z', 82: 'Z', 83: 'Z', 84: 'Z', 85: 'Z', 86: 'Z', 87: 'Z', 88: 'Z', 89: 'Z', 90: 'Z', 91: 'Z', 92: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc13', 'phase': 1, 'paulis': {46: 'Z', 47: 'Z', 51: 'Z', 52: 'Z', 63: 'Z', 64: 'Z', 68: 'Z', 69: 'Z'}},
                            {'name': 'Zc14', 'phase': 1, 'paulis': {51: 'Z', 52: 'Z', 55: 'Z', 56: 'Z', 68: 'Z', 69: 'Z', 72: 'Z', 73: 'Z'}},
                            {'name': 'Zc15', 'phase': 1, 'paulis': {55: 'Z', 56: 'Z', 59: 'Z', 61: 'Z', 72: 'Z', 73: 'Z', 76: 'Z', 78: 'Z'}},
                            {'name': 'Zc16', 'phase': 1, 'paulis': {59: 'Z', 60: 'Z', 61: 'Z', 62: 'Z', 76: 'Z', 77: 'Z', 78: 'Z', 79: 'Z'}},
                            {'name': 'Zc17', 'phase': 1, 'paulis': {47: 'Z', 48: 'Z', 52: 'Z', 53: 'Z', 56: 'Z', 57: 'Z', 59: 'Z', 60: 'Z', 64: 'Z', 65: 'Z', 69: 'Z', 70: 'Z', 73: 'Z', 74: 'Z', 76: 'Z', 77: 'Z'}},
                            {'name': 'Zc18', 'phase': 1, 'paulis': {48: 'Z', 49: 'Z', 53: 'Z', 54: 'Z', 65: 'Z', 66: 'Z', 70: 'Z', 71: 'Z'}},
                            {'name': 'Zc19', 'phase': 1, 'paulis': {53: 'Z', 54: 'Z', 57: 'Z', 58: 'Z', 70: 'Z', 71: 'Z', 74: 'Z', 75: 'Z'}},
                            {'name': 'Zc20', 'phase': 1, 'paulis': {49: 'Z', 50: 'Z', 54: 'Z', 58: 'Z', 66: 'Z', 67: 'Z', 71: 'Z', 75: 'Z'}},
                            {'name': 'Zc21', 'phase': 1, 'paulis': {63: 'Z', 64: 'Z', 65: 'Z', 66: 'Z', 67: 'Z', 68: 'Z', 69: 'Z', 70: 'Z', 71: 'Z', 72: 'Z', 73: 'Z', 74: 'Z', 75: 'Z', 76: 'Z', 77: 'Z', 78: 'Z', 79: 'Z', 80: 'Z', 81: 'Z', 82: 'Z', 83: 'Z', 84: 'Z', 85: 'Z', 86: 'Z', 87: 'Z', 88: 'Z', 89: 'Z', 90: 'Z', 91: 'Z', 92: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc22', 'phase': 1, 'paulis': {80: 'Z', 82: 'Z', 84: 'Z', 86: 'Z', 88: 'Z', 90: 'Z', 92: 'Z', 94: 'Z'}},
                            {'name': 'Zc23', 'phase': 1, 'paulis': {81: 'Z', 82: 'Z', 85: 'Z', 86: 'Z', 89: 'Z', 90: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc24', 'phase': 1, 'paulis': {83: 'Z', 84: 'Z', 85: 'Z', 86: 'Z', 91: 'Z', 92: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc25', 'phase': 1, 'paulis': {87: 'Z', 88: 'Z', 89: 'Z', 90: 'Z', 91: 'Z', 92: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc26', 'phase': 1, 'paulis': {23: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 29: 'Z', 32: 'Z', 34: 'Z', 45: 'Z'}},
                            {'name': 'Zc27', 'phase': 1, 'paulis': {26: 'Z', 28: 'Z', 29: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 34: 'Z', 44: 'Z'}},
                            {'name': 'Zc28', 'phase': 1, 'paulis': {25: 'Z', 27: 'Z', 28: 'Z', 30: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 43: 'Z'}},
                            {'name': 'Zc29', 'phase': 1, 'paulis': {24: 'Z', 26: 'Z', 27: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 32: 'Z', 42: 'Z'}},
                            {'name': 'Zc30', 'phase': 1, 'paulis': {23: 'Z', 25: 'Z', 26: 'Z', 28: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 41: 'Z'}},
                            {'name': 'Zc31', 'phase': 1, 'paulis': {23: 'Z', 26: 'Z', 27: 'Z', 28: 'Z', 30: 'Z', 32: 'Z', 34: 'Z', 40: 'Z'}},
                            {'name': 'Zc32', 'phase': 1, 'paulis': {23: 'Z', 24: 'Z', 27: 'Z', 31: 'Z', 32: 'Z', 33: 'Z', 34: 'Z', 39: 'Z'}},
                            {'name': 'Zc33', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 29: 'Z', 30: 'Z', 31: 'Z', 33: 'Z', 34: 'Z', 38: 'Z'}},
                            {'name': 'Zc34', 'phase': 1, 'paulis': {23: 'Z', 24: 'Z', 28: 'Z', 29: 'Z', 30: 'Z', 32: 'Z', 33: 'Z', 37: 'Z'}},
                            {'name': 'Zc35', 'phase': 1, 'paulis': {24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z', 28: 'Z', 31: 'Z', 34: 'Z', 36: 'Z'}},
                            {'name': 'Zc36', 'phase': 1, 'paulis': {23: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z', 30: 'Z', 33: 'Z', 35: 'Z'}},
                            {'name': 'Zc37', 'phase': 1, 'paulis': {3: 'Z', 6: 'Z', 9: 'Z', 11: 'Z', 26: 'Z', 29: 'Z', 32: 'Z', 34: 'Z'}},
                            {'name': 'Zc38', 'phase': 1, 'paulis': {5: 'Z', 8: 'Z', 9: 'Z', 10: 'Z', 28: 'Z', 31: 'Z', 32: 'Z', 33: 'Z'}},
                            {'name': 'Zc39', 'phase': 1, 'paulis': {4: 'Z', 7: 'Z', 8: 'Z', 9: 'Z', 27: 'Z', 30: 'Z', 31: 'Z', 32: 'Z'}},
                            {'name': 'Zc40', 'phase': 1, 'paulis': {3: 'Z', 6: 'Z', 7: 'Z', 8: 'Z', 26: 'Z', 29: 'Z', 30: 'Z', 31: 'Z'}},
                            {'name': 'Zc41', 'phase': 1, 'paulis': {0: 'Z', 3: 'Z', 5: 'Z', 7: 'Z', 23: 'Z', 26: 'Z', 28: 'Z', 30: 'Z'}},
                            {'name': 'Zc42', 'phase': 1, 'paulis': {0: 'Z', 4: 'Z', 9: 'Z', 11: 'Z', 23: 'Z', 27: 'Z', 32: 'Z', 34: 'Z'}},
                            {'name': 'Zc43', 'phase': 1, 'paulis': {1: 'Z', 8: 'Z', 10: 'Z', 11: 'Z', 24: 'Z', 31: 'Z', 33: 'Z', 34: 'Z'}},
                            {'name': 'Zc44', 'phase': 1, 'paulis': {1: 'Z', 6: 'Z', 7: 'Z', 10: 'Z', 24: 'Z', 29: 'Z', 30: 'Z', 33: 'Z'}},
                            {'name': 'Zc45', 'phase': 1, 'paulis': {1: 'Z', 5: 'Z', 24: 'Z', 28: 'Z'}},
                            {'name': 'Zc46', 'phase': 1, 'paulis': {1: 'Z', 2: 'Z', 3: 'Z', 4: 'Z', 24: 'Z', 25: 'Z', 26: 'Z', 27: 'Z'}},
                            {'name': 'Zc47', 'phase': 1, 'paulis': {1: 'Z', 3: 'Z', 6: 'Z', 9: 'Z', 24: 'Z', 26: 'Z', 29: 'Z', 32: 'Z'}},
                            {'name': 'Zc48', 'phase': 1, 'paulis': {46: 'Z', 47: 'Z', 51: 'Z', 52: 'Z'}},
                            {'name': 'Zc49', 'phase': 1, 'paulis': {51: 'Z', 52: 'Z', 55: 'Z', 56: 'Z'}},
                            {'name': 'Zc50', 'phase': 1, 'paulis': {55: 'Z', 56: 'Z', 59: 'Z', 61: 'Z'}},
                            {'name': 'Zc51', 'phase': 1, 'paulis': {59: 'Z', 60: 'Z', 61: 'Z', 62: 'Z'}},
                            {'name': 'Zc52', 'phase': 1, 'paulis': {47: 'Z', 48: 'Z', 52: 'Z', 53: 'Z', 56: 'Z', 57: 'Z', 59: 'Z', 60: 'Z'}},
                            {'name': 'Zc53', 'phase': 1, 'paulis': {48: 'Z', 49: 'Z', 53: 'Z', 54: 'Z'}},
                            {'name': 'Zc54', 'phase': 1, 'paulis': {53: 'Z', 54: 'Z', 57: 'Z', 58: 'Z'}},
                            {'name': 'Zc55', 'phase': 1, 'paulis': {49: 'Z', 50: 'Z', 54: 'Z', 58: 'Z'}},
                            {'name': 'Zc56', 'phase': 1, 'paulis': {51: 'Z', 52: 'Z', 68: 'Z', 69: 'Z'}},
                            {'name': 'Zc57', 'phase': 1, 'paulis': {47: 'Z', 52: 'Z', 64: 'Z', 69: 'Z'}},
                            {'name': 'Zc58', 'phase': 1, 'paulis': {52: 'Z', 56: 'Z', 69: 'Z', 73: 'Z'}},
                            {'name': 'Zc59', 'phase': 1, 'paulis': {56: 'Z', 59: 'Z', 73: 'Z', 76: 'Z'}},
                            {'name': 'Zc60', 'phase': 1, 'paulis': {59: 'Z', 60: 'Z', 76: 'Z', 77: 'Z'}},
                            {'name': 'Zc61', 'phase': 1, 'paulis': {48: 'Z', 53: 'Z', 65: 'Z', 70: 'Z'}},
                            {'name': 'Zc62', 'phase': 1, 'paulis': {53: 'Z', 57: 'Z', 70: 'Z', 74: 'Z'}},
                            {'name': 'Zc63', 'phase': 1, 'paulis': {53: 'Z', 54: 'Z', 70: 'Z', 71: 'Z'}},
                            {'name': 'Zc64', 'phase': 1, 'paulis': {82: 'Z', 86: 'Z', 90: 'Z', 94: 'Z'}},
                            {'name': 'Zc65', 'phase': 1, 'paulis': {84: 'Z', 86: 'Z', 92: 'Z', 94: 'Z'}},
                            {'name': 'Zc66', 'phase': 1, 'paulis': {88: 'Z', 90: 'Z', 92: 'Z', 94: 'Z'}},
                            {'name': 'Zc67', 'phase': 1, 'paulis': {85: 'Z', 86: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc68', 'phase': 1, 'paulis': {89: 'Z', 90: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Zc69', 'phase': 1, 'paulis': {91: 'Z', 92: 'Z', 93: 'Z', 94: 'Z'}},
                            {'name': 'Xc1', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 6: 'X', 9: 'X', 11: 'X', 22: 'X', 23: 'X', 24: 'X', 25: 'X', 26: 'X', 29: 'X', 32: 'X', 34: 'X', 45: 'X'}},
                            {'name': 'Xc2', 'phase': 1, 'paulis': {3: 'X', 5: 'X', 6: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 21: 'X', 26: 'X', 28: 'X', 29: 'X', 31: 'X', 32: 'X', 33: 'X', 34: 'X', 44: 'X'}},
                            {'name': 'Xc3', 'phase': 1, 'paulis': {2: 'X', 4: 'X', 5: 'X', 7: 'X', 8: 'X', 9: 'X', 10: 'X', 20: 'X', 25: 'X', 27: 'X', 28: 'X', 30: 'X', 31: 'X', 32: 'X', 33: 'X', 43: 'X'}},
                            {'name': 'Xc4', 'phase': 1, 'paulis': {1: 'X', 3: 'X', 4: 'X', 6: 'X', 7: 'X', 8: 'X', 9: 'X', 19: 'X', 24: 'X', 26: 'X', 27: 'X', 29: 'X', 30: 'X', 31: 'X', 32: 'X', 42: 'X'}},
                            {'name': 'Xc5', 'phase': 1, 'paulis': {0: 'X', 2: 'X', 3: 'X', 5: 'X', 6: 'X', 7: 'X', 8: 'X', 18: 'X', 23: 'X', 25: 'X', 26: 'X', 28: 'X', 29: 'X', 30: 'X', 31: 'X', 41: 'X'}},
                            {'name': 'Xc6', 'phase': 1, 'paulis': {0: 'X', 3: 'X', 4: 'X', 5: 'X', 7: 'X', 9: 'X', 11: 'X', 17: 'X', 23: 'X', 26: 'X', 27: 'X', 28: 'X', 30: 'X', 32: 'X', 34: 'X', 40: 'X'}},
                            {'name': 'Xc7', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 4: 'X', 8: 'X', 9: 'X', 10: 'X', 11: 'X', 16: 'X', 23: 'X', 24: 'X', 27: 'X', 31: 'X', 32: 'X', 33: 'X', 34: 'X', 39: 'X'}},
                            {'name': 'Xc8', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 6: 'X', 7: 'X', 8: 'X', 10: 'X', 11: 'X', 15: 'X', 24: 'X', 25: 'X', 29: 'X', 30: 'X', 31: 'X', 33: 'X', 34: 'X', 38: 'X'}},
                            {'name': 'Xc9', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 5: 'X', 6: 'X', 7: 'X', 9: 'X', 10: 'X', 14: 'X', 23: 'X', 24: 'X', 28: 'X', 29: 'X', 30: 'X', 32: 'X', 33: 'X', 37: 'X'}},
                            {'name': 'Xc10', 'phase': 1, 'paulis': {1: 'X', 2: 'X', 3: 'X', 4: 'X', 5: 'X', 8: 'X', 11: 'X', 13: 'X', 24: 'X', 25: 'X', 26: 'X', 27: 'X', 28: 'X', 31: 'X', 34: 'X', 36: 'X'}},
                            {'name': 'Xc11', 'phase': 1, 'paulis': {0: 'X', 1: 'X', 2: 'X', 3: 'X', 4: 'X', 7: 'X', 10: 'X', 12: 'X', 23: 'X', 24: 'X', 25: 'X', 26: 'X', 27: 'X', 30: 'X', 33: 'X', 35: 'X'}},
                            {'name': 'Xc12', 'phase': 1, 'paulis': {23: 'X', 24: 'X', 25: 'X', 26: 'X', 27: 'X', 28: 'X', 29: 'X', 30: 'X', 31: 'X', 32: 'X', 33: 'X', 34: 'X', 35: 'X', 36: 'X', 37: 'X', 38: 'X', 39: 'X', 40: 'X', 41: 'X', 42: 'X', 43: 'X', 44: 'X', 45: 'X', 46: 'X', 47: 'X', 48: 'X', 49: 'X', 50: 'X', 51: 'X', 52: 'X', 53: 'X', 54: 'X', 55: 'X', 56: 'X', 57: 'X', 58: 'X', 59: 'X', 60: 'X', 61: 'X', 62: 'X', 63: 'X', 64: 'X', 65: 'X', 66: 'X', 67: 'X', 68: 'X', 69: 'X', 70: 'X', 71: 'X', 72: 'X', 73: 'X', 74: 'X', 75: 'X', 76: 'X', 77: 'X', 78: 'X', 79: 'X', 80: 'X', 81: 'X', 82: 'X', 83: 'X', 84: 'X', 85: 'X', 86: 'X', 87: 'X', 88: 'X', 89: 'X', 90: 'X', 91: 'X', 92: 'X', 93: 'X', 94: 'X'}},
                            {'name': 'Xc13', 'phase': 1, 'paulis': {46: 'X', 47: 'X', 51: 'X', 52: 'X', 63: 'X', 64: 'X', 68: 'X', 69: 'X'}},
                            {'name': 'Xc14', 'phase': 1, 'paulis': {51: 'X', 52: 'X', 55: 'X', 56: 'X', 68: 'X', 69: 'X', 72: 'X', 73: 'X'}},
                            {'name': 'Xc15', 'phase': 1, 'paulis': {55: 'X', 56: 'X', 59: 'X', 61: 'X', 72: 'X', 73: 'X', 76: 'X', 78: 'X'}},
                            {'name': 'Xc16', 'phase': 1, 'paulis': {59: 'X', 60: 'X', 61: 'X', 62: 'X', 76: 'X', 77: 'X', 78: 'X', 79: 'X'}},
                            {'name': 'Xc17', 'phase': 1, 'paulis': {47: 'X', 48: 'X', 52: 'X', 53: 'X', 56: 'X', 57: 'X', 59: 'X', 60: 'X', 64: 'X', 65: 'X', 69: 'X', 70: 'X', 73: 'X', 74: 'X', 76: 'X', 77: 'X'}},
                            {'name': 'Xc18', 'phase': 1, 'paulis': {48: 'X', 49: 'X', 53: 'X', 54: 'X', 65: 'X', 66: 'X', 70: 'X', 71: 'X'}},
                            {'name': 'Xc19', 'phase': 1, 'paulis': {53: 'X', 54: 'X', 57: 'X', 58: 'X', 70: 'X', 71: 'X', 74: 'X', 75: 'X'}},
                            {'name': 'Xc20', 'phase': 1, 'paulis': {49: 'X', 50: 'X', 54: 'X', 58: 'X', 66: 'X', 67: 'X', 71: 'X', 75: 'X'}},
                            {'name': 'Xc21', 'phase': 1, 'paulis': {63: 'X', 64: 'X', 65: 'X', 66: 'X', 67: 'X', 68: 'X', 69: 'X', 70: 'X', 71: 'X', 72: 'X', 73: 'X', 74: 'X', 75: 'X', 76: 'X', 77: 'X', 78: 'X', 79: 'X', 80: 'X', 81: 'X', 82: 'X', 83: 'X', 84: 'X', 85: 'X', 86: 'X', 87: 'X', 88: 'X', 89: 'X', 90: 'X', 91: 'X', 92: 'X', 93: 'X', 94: 'X'}},
                            {'name': 'Xc22', 'phase': 1, 'paulis': {80: 'X', 82: 'X', 84: 'X', 86: 'X', 88: 'X', 90: 'X', 92: 'X', 94: 'X'}},
                            {'name': 'Xc23', 'phase': 1, 'paulis': {81: 'X', 82: 'X', 85: 'X', 86: 'X', 89: 'X', 90: 'X', 93: 'X', 94: 'X'}},
                            {'name': 'Xc24', 'phase': 1, 'paulis': {83: 'X', 84: 'X', 85: 'X', 86: 'X', 91: 'X', 92: 'X', 93: 'X', 94: 'X'}},
                            {'name': 'Xc25', 'phase': 1, 'paulis': {87: 'X', 88: 'X', 89: 'X', 90: 'X', 91: 'X', 92: 'X', 93: 'X', 94: 'X'}}
        ]
        logical_operators = [
                             {'name': 'LX', 'phase': 1, 'paulis': {11: 'X', 13: 'X', 15: 'X', 16: 'X', 17: 'X', 21: 'X', 22: 'X', 34: 'X', 36: 'X', 38: 'X', 39: 'X', 40: 'X', 44: 'X', 45: 'X', 50: 'X', 57: 'X', 58: 'X', 60: 'X', 62: 'X', 67: 'X', 74: 'X', 75: 'X', 77: 'X', 79: 'X', 82: 'X', 84: 'X', 85: 'X', 88: 'X', 89: 'X', 91: 'X', 94: 'X'}},
                            {'name': 'LZ', 'phase': 1, 'paulis': {0: 'Z', 23: 'Z', 46: 'Z', 63: 'Z', 80: 'Z', 81: 'Z', 83: 'Z', 87: 'Z', 94: 'Z'}}
        ]
        return code_stabilisers, logical_operators
    
    else:
        raise Exception('code name not prepared yet')