import pandas as pd
import os

def split_csv(file_path, output_dir, chunk_size=50):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Create output directory if it does not exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Calculate the number of chunks needed
    num_chunks = (len(df) // chunk_size) + (1 if len(df) % chunk_size != 0 else 0)

    # Split the DataFrame into chunks and save each chunk as a new CSV file
    for i in range(num_chunks):
        start_index = i * chunk_size
        end_index = min((i + 1) * chunk_size, len(df))
        chunk_df = df.iloc[start_index:end_index]
        
        # Define the output file path
        output_file = os.path.join(output_dir, f'chunk_{i + 1}.csv')
        
        # Save the chunk to a CSV file
        chunk_df.to_csv(output_file, index=False)
        print(f'Saved chunk {i + 1} to {output_file}')

# Example usage
file_path = 'C:\\Users\\hp\\Documents\\data\\emails_with_names_and_companies444444444444444\\emails_with_names_and_companies444444444444444.csv'
output_dir = 'C:\\Users\\hp\\Documents\\data\\emails_with_names_and_companies444444444444444'

split_csv(file_path, output_dir)
