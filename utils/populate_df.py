import os
import re
import glob
import pandas as pd 

def get_key_name(x):
    name= os.path.basename(x)
    name= name.replace("_", "")
    return re.sub(r"\.(png|jpg)$", "", name, flags=re.IGNORECASE)

def get_key_name_for_input(x):
    return re.sub(r"Prompt\d*", "", get_key_name(x))
    
if __name__ == '__main__':
    master_df= pd.read_csv('./data/Prompts_Final_Categories.csv')
    master_df['lkey']= master_df['Prompt Number'].apply(get_key_name)
    master_df['lkey_input']= master_df['Prompt Number'].apply(get_key_name_for_input)
    
    input_images_df= pd.read_csv("./data/image_name_input.txt", header=None, names=["input_image_path"])
    input_images_df['rkey_input']= input_images_df['input_image_path'].apply(get_key_name_for_input)
    master_df= pd.merge(master_df, input_images_df, how= 'left', left_on= 'lkey_input', right_on= 'rkey_input')
    
    output_text_files= glob.glob("./data/image_name_output_*.txt")
    all_output_df = pd.DataFrame()
    for file in output_text_files:
        file_name= os.path.basename(file)
        column_suffix= file_name.replace("image_name_output_", "").replace(".txt", "")
        column_name= f"output_image_path_{column_suffix}"

        df= pd.read_csv(file, header=None, names=[column_name])
        
        df['rkey']= df[column_name].apply(get_key_name)
        
        if all_output_df.empty:
            all_output_df= df
        else:
            all_output_df= pd.merge(all_output_df, df, on='rkey', how='outer')
    
    final_df= pd.merge(master_df, all_output_df, how='left', left_on='lkey', right_on='rkey')
    final_df.drop(columns= ['lkey', 'rkey', 'lkey_input', 'rkey_input'], inplace= True)
    
    final_df.to_csv('./data/Prompts_Final_Categories_with_Image_Paths.csv', index= False)