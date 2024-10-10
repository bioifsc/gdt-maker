#!/usr/bin/env python3

import os
import sys
import subprocess
import numpy as np
from scipy.cluster.hierarchy import linkage, to_tree
from scipy.spatial.distance import squareform
from newick_to_img import draw_phylogenetic_tree_to_png  # Importando a função

# Function to execute a command and capture the output
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)

# Function to display help
def print_help():
    print(f"Usage: {sys.argv[0]} -d <directory> [-o <output_directory>] [-W <width_inch>] [-H <height_inch>] [-D <dpi>] [-img <output_image>]")
    print("Options:")
    print("  -d <directory>       Path where genome (.fasta) files are located (mandatory).")
    print("  -o <output_directory> Directory to save results (optional, default is current directory).")
    print("  -W <width_inch>      Width of the output image in inches (optional).")
    print("  -H <height_inch>     Height of the output image in inches (optional).")
    print("  -D <dpi>             Dots per inch for the output image (optional, default is 300).")
    print("  -img <output_image>  Name of the output image file (optional, default is 'phylogenetic_tree.png').")
    print("  -h, --help           Show this help message and exit.")
    sys.exit(1)

# Check if the user requested help
if '-h' in sys.argv or '--help' in sys.argv:
    print_help()

# Check if the directories were passed as arguments
if len(sys.argv) < 3 or '-d' not in sys.argv:
    print_help()

# Get the input and output directory arguments
DIR = sys.argv[sys.argv.index('-d') + 1]

# If the output directory is not specified, use the current directory
OUTPUT_DIR = os.getcwd() if '-o' not in sys.argv else sys.argv[sys.argv.index('-o') + 1]

# Set optional parameters for image generation
width_inch = 12
height_inch = 8
dpi = 300  # Default DPI
output_image = "phylogenetic_tree.png"  # Default output image name

if '-W' in sys.argv:
    width_inch = float(sys.argv[sys.argv.index('-W') + 1])

if '-H' in sys.argv:
    height_inch = float(sys.argv[sys.argv.index('-H') + 1])

if '-D' in sys.argv:
    dpi = int(sys.argv[sys.argv.index('-D') + 1])

if '-img' in sys.argv:
    output_image = sys.argv[sys.argv.index('-img') + 1]

# Check if the output directory exists; if not, create it
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# List all .fasta files in the input directory
files = [f for f in os.listdir(DIR) if f.endswith('.fasta')]

# Remove the extensions from the files to get the base names
files_base = [os.path.splitext(f)[0] for f in files]

# Loop through the found files to calculate distances
for ref in files_base:
    for query in files_base:
        if ref != query:
            print(f"Running {ref} vs {query}")
#            command = f"sudo docker run --rm -v {os.getcwd()}:/data/ -w /data staphb/mash mash dist -s #1000000 {DIR}/{ref}.fasta {DIR}/{query}.fasta > {OUTPUT_DIR}/{ref}_vs_{query}.out"
            command = f"mash dist -s 1000000 {DIR}/{ref}.fasta {DIR}/{query}.fasta > {OUTPUT_DIR}/{ref}_vs_{query}.out"
            run_command(command)

# Creating the matrix
print("Creating matrix")
matrix = ""

for ref in files_base:
    line = ""
    for query in files_base:
        if ref == query:
            dist = 0  # If ref is equal to query, the distance is 0
        else:
            # Capture the distance value from the output file
            out_file = f"{OUTPUT_DIR}/{ref}_vs_{query}.out"
            with open(out_file, 'r') as f:
                dist = f.read().split()[2]  # Capture the third value from the line
        # Add the value to the line, separating by tab
        line += f"{dist}\t"
    # Remove the last tab and add the line to the matrix
    matrix += line.rstrip('\t') + "\n"

# Save the matrix to distances.txt in the output directory
with open(os.path.join(OUTPUT_DIR, "distances.txt"), "w") as f:
    f.write(matrix)

print(f"Matrix saved to {OUTPUT_DIR}/distances.txt")

# Function to read the distance matrix from a file
def read_distance_matrix(file_path):
    # Read the distance matrix and return a numpy array
    return np.loadtxt(file_path)

# Read the distance matrix
dist_matrix = read_distance_matrix(os.path.join(OUTPUT_DIR, 'distances.txt'))

# Transform the distance matrix into condensed format
condensed_dist_matrix = squareform(dist_matrix)

# Build the tree using the UPGMA method
Z = linkage(condensed_dist_matrix, method='average')

# Convert to a tree
tree = to_tree(Z, rd=False)

# Generate the Newick representation with distances and names
def tree_to_newick_with_distances(node):
    if node.is_leaf():
        return "{}:0.0".format(files_base[node.id])  # Return the sample name with distance 0
    else:
        left_newick = tree_to_newick_with_distances(node.left)
        right_newick = tree_to_newick_with_distances(node.right)
        distance = node.dist  # Distance of the node
        return "({},{}){}:{}".format(left_newick, right_newick, distance, distance)

# Call the function to create the tree in Newick format with distances
newick_str_with_distances = tree_to_newick_with_distances(tree)

# Save the tree in Newick format in the output directory
newick_file_path = os.path.join(OUTPUT_DIR, "tree.newick")
with open(newick_file_path, "w") as f:
    f.write(newick_str_with_distances + '\n')

# Print the Newick representation with distances and inform about the save
print(newick_str_with_distances)
print(f"Newick tree saved to {newick_file_path}")

# Agora chamamos a função de geração da imagem em vez de usar o comando python3
draw_phylogenetic_tree_to_png(newick_file_path, os.path.join(OUTPUT_DIR, output_image), width_inch, height_inch, dpi)

print(f"Image saved to {os.path.join(OUTPUT_DIR, output_image)}")

