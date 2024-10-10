#!/usr/bin/env python3

import argparse
from Bio import Phylo
import matplotlib.pyplot as plt
import io
import cairosvg

# Function to generate the phylogenetic tree and save it as a 300dpi PNG
def draw_phylogenetic_tree_to_png(newick_file, output_image, width_inch=12, height_inch=8, dpi=300):
    # Load the tree from the .newick file
    tree = Phylo.read(newick_file, "newick")
    
    # Create a figure with the specified size
    fig = plt.figure(figsize=(width_inch, height_inch), dpi=dpi)
    axes = fig.add_subplot(1, 1, 1)
    
    # Draw the tree without displaying it
    Phylo.draw(tree, axes=axes, do_show=False)
    
    # Automatically adjust the layout so all elements fit within the figure
    plt.tight_layout()

    # Save the tree as an SVG file (vector format)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='svg', bbox_inches='tight')
    plt.close()

    # Convert SVG to PNG with specified DPI
    buffer.seek(0)  # Rewind to the start of the buffer
    cairosvg.svg2png(bytestring=buffer.getvalue(), write_to=output_image, dpi=dpi)

# Main block to handle command-line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a phylogenetic tree from a .newick file and save as a PNG image.")
    
    # Mandatory argument for the newick file
    parser.add_argument('newick_file', help="Path to the .newick file.")
    
    # Optional arguments for output image, width, height, and dpi
    parser.add_argument('-o', '--output_image', default="phylogenetic_tree.png", help="Output PNG image file (default: phylogenetic_tree.png).")
    parser.add_argument('-W', '--width_inch', type=float, default=12, help="Width of the image in inches (default: 12).")
    parser.add_argument('-H', '--height_inch', type=float, default=8, help="Height of the image in inches (default: 8).")
    parser.add_argument('-d', '--dpi', type=int, default=300, help="DPI (dots per inch) of the image (default: 300).")
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the function to draw the tree and save it
    draw_phylogenetic_tree_to_png(args.newick_file, args.output_image, args.width_inch, args.height_inch, args.dpi)

