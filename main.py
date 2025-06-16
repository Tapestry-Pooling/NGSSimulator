import pysam
import os
import random
import csv
import argparse

def map_filenames(filenames):
    """
    Maps file names to S1, S2, ..., Sn and saves the mapping as sample_name_mapping.csv.
    
    Parameters:
        filenames (list of str): List of file names.
    
    Returns:
        dict: Mapping of file names to S1, S2, ..., Sn.
    """
    mapping = {filename: f"S{i+1}.bam" for i, filename in enumerate(filenames)}
    
    # Save to CSV
    with open("sample_name_mapping.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Sample Name"])
        for filename, sample_name in mapping.items():
            writer.writerow([filename, sample_name])
    return mapping

def make_pools(input_bam_path,output_bam_path,number_of_samples):
    #check if the number of samples is a perfect square
    if int(number_of_samples**0.5)!=number_of_samples**0.5:
        print("The number of samples is not a perfect square")
        return
    number_of_samples_per_pool=int(number_of_samples**0.5)
    #Check if the input directory exists and has the correct number of files
    if os.path.exists(input_bam_path):
        bam_files = [f for f in os.listdir(input_bam_path) if f.endswith(".bam")]
        bam_count = len(bam_files)
        if bam_count!=number_of_samples:
            print("The number of BAM files in the input directory is not equal to the number of samples")
            return
    else:
        print("The input directory does not exist")
        return

    bam_files = sorted([f for f in os.listdir(input_bam_path) if f.endswith(".bam")])
    name2index = map_filenames(bam_files)
    index2name = {v: k for k, v in name2index.items()}
    #Using the first file as a template for the header
    template_file = pysam.AlignmentFile(os.path.join(input_bam_path, index2name["S1.bam"]), "rb")

    #mkdir while deleting the existing directory for output
    if os.path.exists(output_bam_path):
        print("The output directory already exists. Please delete it and try again")
        return
    os.mkdir(output_bam_path)

    PoolFiles = {}
    for i in range(3* number_of_samples_per_pool):
        PoolFiles["pool_"+str(i+1)]=pysam.AlignmentFile(os.path.join(output_bam_path,"pool_"+str(i+1)+".bam"),"wb",template=template_file)

    for i in range(number_of_samples):
        #Find the Indices for the pools
        a_index, b_index = divmod(i,number_of_samples_per_pool) #find matrix index in column major
        if a_index>=b_index:
            c_index = ((a_index - b_index) + number_of_samples_per_pool) % number_of_samples_per_pool
        else:
            c_index = number_of_samples_per_pool - (b_index - a_index)
        #Open Sample File
        sam_file = pysam.AlignmentFile(os.path.join(input_bam_path,index2name["S"+str(i+1)+".bam"]), "rb")
        for read in sam_file:
            #Sample the read into one of the three choices
            pool_choice = random.choice(["a", "b", "c"])
            if pool_choice == "a":
                PoolFiles["pool_"+str(a_index+1)].write(read)
            elif pool_choice == "b":
                PoolFiles["pool_"+str(b_index+1+number_of_samples_per_pool)].write(read)
            else:
                PoolFiles["pool_"+str(c_index+1+(2* number_of_samples_per_pool))].write(read)
        sam_file.close()
        print("sample - {} processed!".format(index2name["S"+str(i+1)+".bam"]))

    for files in PoolFiles.values():
        files.close()
    template_file.close()
    print("pooling completed!!")
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process BAM files and create pools.")
    parser.add_argument("input_bam_path", type=str, help="Path to the input BAM directory")
    parser.add_argument("output_bam_path", type=str, help="Path to the output BAM directory")
    parser.add_argument("number_of_samples", type=int, help="Total number of BAM samples (must be a perfect square)")
    
    args = parser.parse_args()
    make_pools(args.input_bam_path, args.output_bam_path, args.number_of_samples)

# example : python main.py /path/to/input_bam /path/to/output_bam 64
