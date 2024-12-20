import streamlit as st
import pandas as pd
import glob

st.set_page_config(layout="wide")

RATING_INFO="""
        **Rating Scale (0-5):**
        - **0 - Very Poor:** No change in the image or a very negative version that ruins the original completely.
        - **1 - Poor:** Slight attempt towards the intended image, but tolerates a high amount of errors.
        - **2 - Okayish:** An okay attempt towards the intended image, tolerating a moderate amount of errors.
        - **3 - Decent:** A decent attempt towards the intended image, with a tolerable but noticeable amount of errors.
        - **4 - Good:** A good attempt towards the intended image, with few errors.
        - **5 - Very Good:** A very good attempt towards the intended image, with very few or no errors.
        
        **QUALITY:**  
        *How technically sound is the image? Consider clarity, resolution, sharpness, and the absence of artifacts.*

        **AESTHETICS:**  
        *How visually pleasing is the image? Consider composition, color harmony, balance, and overall artistic appeal.*
        
        **ADDITION:**  
        *How well is the new object integrated into the existing image? Did the addition affect the original image adversely?*

        **SPECIFIC OBJECT:**  
        *For prompts focusing on a specific object in the image, how effectively are the requested changes implemented?*

        **CHANGE:**  
        *Does the generated image maintain structural relevance to the original image after the changes?*

        **STYLE TRANSFER:**  
        *How successfully is the intended style conveyed in the generated image?*

        **BACKGROUND:**  
        *For prompts altering the background, how accurately and effectively is the new background depicted?*

        **SPECIFIC DETAIL:**  
        *Do the generated images accurately reflect the specific details requested, such as a tie with pink color and yellow dots?*

        **SPECIFIC POSITION:**  
        *For prompts requiring objects at certain positions, are the objects placed correctly and clearly?*

        **LANDSCAPE:**  
        *When changing the overall landscape, how well does the generated image represent the intended environment?*

        **COUNT:**  
        *For prompts specifying a number of objects, does the generated image contain the correct number as intended?*

        **ENTIRE OBJECT - RELEVANT:**  
        *If a new, structurally relevant object is introduced, how well does it fit into the original image context?*

        **ENTIRE OBJECT - IRRELEVANT:**  
        *If a new, structurally irrelevant object is introduced, how well is it generated and integrated despite not fitting naturally?*

        **FICTION REFERENCE:**  
        *For prompts with fictional references, how effectively are these elements incorporated into the generated image?*

        **TIMELINE:**  
        *If the timeline is altered (e.g., setting it in 2500 AD), how convincingly are time-related changes depicted?*

        **IMAGE:**  
        *For prompts completely transforming the original image (e.g., snow-filled mountains into a desert), how successful is the complete regeneration?*

        **CAMERA CONTROL:**  
        *When the viewing angle or perspective changes, how accurately is this visual shift represented?*

        **REMOVAL:**  
        *For prompts removing one or more objects, how well does the model handle the omission and maintain image quality?*

        **MULTIPLE-OBJECTS:**  
        *When dealing with images containing multiple objects, how effectively are all elements handled according to the prompt?*
"""

st.title("Image Human Evaluation")

if 'const' not in st.session_state:
    st.session_state.const= {
        'max_length': None,
        'rating_conversion': {
            'Very Good': 5,
            'Good': 4,
            'Decent': 3,
            'Okayish': 2,
            'Poor': 1,
            'Very Poor/ No Change': 0
        }
    }
    
if 'model_being_evalutated' not in st.session_state:
    model_options= ['Grounded-Instruct-Pix2Pix', 'ControlNet', 'Plug and Play', 'Instructpix2pix']
    model_being_evalutated= st.radio("What model are you evaluating?", model_options, index= None, horizontal= True)
    
    if not model_being_evalutated:
        st.warning("Please select a model to proceed.")
        st.stop()
    
    st.session_state.model_being_evalutated= model_being_evalutated
    st.rerun()
        
if 'df_Prompts_Final_Categories_with_Image_Paths' not in st.session_state:
    st.session_state.df_Prompts_Final_Categories_with_Image_Paths= pd.read_csv("./data/Prompts_Final_Categories_with_Image_Paths.csv")
    
    column_name= "output_image_path_"  + st.session_state.model_being_evalutated
    
    n_nan_values= st.session_state.df_Prompts_Final_Categories_with_Image_Paths[column_name].isna().sum()
    
    st.session_state.const['max_length']= len(st.session_state.df_Prompts_Final_Categories_with_Image_Paths)- n_nan_values
    

if 'df_Rating_Template_Final' not in st.session_state:
    csv_filename= f"{st.session_state.model_being_evalutated}_ratings.csv"
    if csv_filename in glob.glob("*.csv"):
        st.session_state.df_Rating_Template_Final= pd.read_csv(csv_filename)
    else:
        st.session_state.df_Rating_Template_Final= pd.read_csv("./data/Rating_Template_Final.csv")
    
if 'cache' not in st.session_state:
    st.session_state.cache= {"input_image": None, "output_image": None}
    

def get_input_image_path(iteration):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths.iloc[iteration]['input_image_path']

def get_output_image_path(iteration):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths.iloc[iteration][f'output_image_path_{st.session_state.model_being_evalutated}']

def get_images(iteration):
    st.session_state.cache['output_image']= get_output_image_path(iteration)
    
    if st.session_state.cache['output_image'] is None or pd.isna(st.session_state.cache['output_image']):
        
        if st.session_state.direction == 'forward':
            st.session_state.iteration+= 1
        else:
            st.session_state.iteration-= 1
            
        st.rerun()    

    st.session_state.cache['input_image']= get_input_image_path(iteration)
    return st.session_state.cache

def get_prompt(iteration):
    if iteration >= len(st.session_state.df_Prompts_Final_Categories_with_Image_Paths):
        st.warning("Adjusted iteration exceeds available prompts")
        st.stop()
        
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths['Prompt'][iteration]

def get_challenges(iteration)-> list[str]:
    string_of_challenges= st.session_state.df_Prompts_Final_Categories_with_Image_Paths['Challenge Category'][iteration]
    list_of_challenges= string_of_challenges.split(',')
    return ["Quality", "Aesthetics"] + [x.strip() for x in list_of_challenges]

def update_records(iteration, challenge, rating):
    rating_as_int= int(st.session_state.const['rating_conversion'][rating])
    st.session_state.df_Rating_Template_Final.at[iteration, challenge]= rating_as_int
     
if 'iteration' not in st.session_state: 
    
    start= st.number_input("**You can resume the evaluation from a specific point. Enter the point where you want to start (e.g., 0 for the first item):**", min_value=1, max_value= st.session_state.const['max_length'], value=1, step= 1)
    start-= 1
    
    if st.button("Begin Evaluation"):
        st.session_state.iteration= start
        st.session_state.direction= 'forward'
        st.session_state.ratings = {}
        st.rerun()

if 'iteration' in st.session_state:
    iteration= st.session_state.iteration
    
    if st.button("Evaluate another model"):
        for key in st.session_state:
            del st.session_state[key]
        st.rerun()
        
    if iteration < st.session_state.const['max_length']:
        if 'current_iteration' not in st.session_state or st.session_state.current_iteration != iteration:
            st.session_state.images= get_images(iteration)
            st.session_state.prompt= get_prompt(iteration)
            st.session_state.challenges= get_challenges(iteration)
            st.session_state.current_iteration= iteration
            st.session_state.ratings[iteration]= {x: None for x in st.session_state.challenges} 
        
        images= st.session_state.images
        prompt= st.session_state.prompt
        challenges= st.session_state.challenges
                
        st.subheader(f"Progress: {(iteration + 1)}/{st.session_state.const['max_length']}")
        progress=min((iteration + 1) / st.session_state.const['max_length'], 1.0)
            
        st.progress(progress)
        if st.button("Back"):
            st.session_state.iteration= max(st.session_state.iteration -1, 0)
            if st.session_state.direction!= 'backward':
                st.session_state.direction= 'backward'
            st.rerun()
            
        st.header(f"Prompt: {prompt}", divider= 'gray')
        
        with st.expander("Show Legend"):
            st.markdown(RATING_INFO)
            
        col1, col2, col3= st.columns(3, vertical_alignment= 'center')
        
        with col2:
            st.write("**input image**")
            st.image(images['input_image'], width= 400)
        with col3:
            st.write("**output image**")
            st.image(images['output_image'], width= 400)
        
        with col1:
            for challenge in challenges:
                st.session_state.ratings[iteration][challenge]= st.radio(f"Rate the output image for {challenge}", ["Very Good", "Good", "Decent", "Okayish", "Poor", "Very Poor/ No Change"], key=f"rating_{iteration}_{challenge}", index= None)

        ratings= st.session_state.ratings[iteration]
                
        if st.button("Next", use_container_width= True):
            if all(ratings.values()):
                for challenge, rating in ratings.items():
                    update_records(iteration, challenge, rating)
                
                st.session_state.df_Rating_Template_Final.to_csv(
                    f"./{st.session_state.model_being_evalutated}_ratings.csv", 
                    index=False
                )
                
                st.session_state.iteration+= 1
                
                if st.session_state.direction!= 'forward':
                    st.session_state.direction= 'forward'
                    
                st.rerun()
            else:
                st.warning("Please rate all challenges before proceeding.")
    else:
        st.write("### Evaluation Complete.")