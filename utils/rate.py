import streamlit as st
import pandas as pd
import glob

from rating_info import RATING_INFO

st.set_page_config(layout="wide")
st.title("Image Human Evaluation")

if 'const' not in st.session_state:
    st.session_state.const= {
        'max_index': None,
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
    
    st.session_state.const['max_index']= len(st.session_state.df_Prompts_Final_Categories_with_Image_Paths)- n_nan_values
    

if 'df_Rating_Template_Final' not in st.session_state:
    csv_filename= f"{st.session_state.model_being_evalutated}_ratings.csv"

    if csv_filename in glob.glob("*.csv"):
        st.session_state.df_Rating_Template_Final= pd.read_csv(csv_filename)
    else:
        st.session_state.df_Rating_Template_Final= pd.read_csv("./data/Rating_Template_Final.csv")
    
if 'cache' not in st.session_state:
    st.session_state.cache= {"input_image": None, "output_image": None}
    

def get_input_image_path(current_index):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths.iloc[current_index]['input_image_path']

def get_output_image_path(current_index):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths.iloc[current_index][f'output_image_path_{st.session_state.model_being_evalutated}']

def get_images(current_index):
    st.session_state.cache['output_image']= get_output_image_path(current_index)
    
    if st.session_state.cache['output_image'] is None or pd.isna(st.session_state.cache['output_image']):
        
        if st.session_state.forward:
            st.session_state.current_index+= 1
            st.session_state.const['max_index']+= 1

        else:
            st.session_state.current_index-= 1
            
        st.rerun()    

    st.session_state.cache['input_image']= get_input_image_path(current_index)
    return st.session_state.cache

def get_prompt(current_index):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths['Prompt'][current_index]

def get_challenges(current_index)-> list[str]:
    string_of_challenges= st.session_state.df_Prompts_Final_Categories_with_Image_Paths['Challenge Category'][current_index]
    list_of_challenges= string_of_challenges.split(',')
    return ["Quality", "Aesthetics"] + [x.strip() for x in list_of_challenges]

def update_records(current_index, challenge, rating):
    rating_as_int= int(st.session_state.const['rating_conversion'][rating])
    st.session_state.df_Rating_Template_Final.at[current_index, challenge]= rating_as_int
     
if 'current_index' not in st.session_state: 
    
    start= st.number_input(
        "**You can resume the evaluation from a specific point. Enter the point where you want to start (e.g., 0 for the first item):**",
        min_value= 1,
        max_value= st.session_state.const['max_index'],
        value= 1,
        step= 1
    )
    
    start-= 1
    
    if st.button("Begin Evaluation"):
        st.session_state.current_index= start
        st.session_state.forward= True
        st.session_state.ratings= {}
        st.rerun()

if 'current_index' in st.session_state:
    current_index= st.session_state.current_index
    
    if st.button("Evaluate another model"):
        for key in st.session_state:
            del st.session_state[key]
        st.rerun()
        
    if current_index < st.session_state.const['max_index']:
        if 'current_displayed_index' not in st.session_state or st.session_state.current_displayed_index != current_index:
            st.session_state.images= get_images(current_index)
            st.session_state.prompt= get_prompt(current_index)
            st.session_state.challenges= get_challenges(current_index)
            st.session_state.current_displayed_index= current_index
            st.session_state.ratings[current_index]= {x: None for x in st.session_state.challenges} 
        
        images= st.session_state.images
        prompt= st.session_state.prompt
        challenges= st.session_state.challenges
        
        st.subheader(f"Progress: {(current_index + 1)}/{st.session_state.const['max_index']}")
        progress=min((current_index + 1) / st.session_state.const['max_index'], 1.0)
            
        st.progress(progress)

        if st.button("Back"):
            st.session_state.current_index= max(st.session_state.current_index - 1, 0)
            if st.session_state.forward:
                st.session_state.forward= False
                
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
                st.session_state.ratings[current_index][challenge]= st.radio(
                    f"Rate the output image for {challenge}",
                    [
                        "Very Good",
                        "Good",
                        "Decent",
                        "Okayish",
                        "Poor",
                        "Very Poor/ No Change"
                    ], 
                    key=f"rating_{current_index}_{challenge}",
                    index= None
                )

        ratings= st.session_state.ratings[current_index]
                
        if st.button("Next", use_container_width= True):
            if all(ratings.values()):
                for challenge, rating in ratings.items():
                    update_records(current_index, challenge, rating)
                
                st.session_state.df_Rating_Template_Final.to_csv(
                    f"./{st.session_state.model_being_evalutated}_ratings.csv", 
                    index= False
                )
                
                st.session_state.current_index+= 1
                
                if not st.session_state.forward:
                    st.session_state.forward= True
                    
                st.rerun()
            else:
                st.warning("Please rate all challenges before proceeding.")
    else:
        st.write("### Evaluation Complete.")