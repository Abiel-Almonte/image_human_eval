import pandas as pd 
import glob
import os

if __name__ == '__main__':
    master_df= pd.read_csv('./data/Prompts_Final_Categories.csv')
    paths_for_input_images= pd.read_csv("./data/image_name_input.txt", header=None, names=["input_image_path"])
    output_text_files= glob.glob("./data/image_name_output_*.txt")

    output_columns= {}
    for file in output_text_files:
        file_name= os.path.basename(file)
        column_suffix= file_name.replace("image_name_output_", "").replace(".txt", "")
        column_name= f"output_image_path_{column_suffix}"

        df= pd.read_csv(file, header=None, names=[column_name])
        output_columns[column_name]= df[column_name]

    paths_for_output_images= pd.DataFrame(output_columns)
    combined_df= pd.concat([paths_for_input_images, paths_for_output_images], axis=1)
    
    final_df = pd.concat([master_df.reset_index(drop=True), combined_df.reset_index(drop=True)], axis=1)
    final_df.to_csv('./data/Prompts_Final_Categories_with_Image_Paths.csv', index= False)