import streamlit as st
import pandas as pd
import glob

st.set_page_config(layout="wide")
st.title("Image Human Evaluation")

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

if 'df_Rating_Template_Final' not in st.session_state:
    csv_filename= f"{st.session_state.model_being_evalutated}_ratings.csv"
    if csv_filename in glob.glob("*.csv"):
        st.session_state.df_Rating_Template_Final= pd.read_csv(csv_filename)
    else:
        st.session_state.df_Rating_Template_Final= pd.read_csv("./data/Rating_Template_Final.csv")
    
if 'cache' not in st.session_state:
    st.session_state.cache= {"input_image": None, "output_image": None}
    
    
if 'const' not in st.session_state:
    st.session_state.const= {
        'input_max_length': 50,
        'N_PROMPTS': 5,      
        'rating_conversion': {
            'Very Good': 5,
            'Good': 4,
            'Decent': 3,
            'Okayish': 2,
            'Poor': 1,
            'Very Poor': 0
        }
    }

def get_input_image_name(iteration):
    if iteration >= st.session_state.const['input_max_length']:
        return None
    
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths.iloc[iteration]['input_image_path']

def get_output_image_name(iteration):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths.iloc[iteration][f'output_image_path_{st.session_state.model_being_evalutated}']

def get_images(iteration):
    prompt_idx= iteration% st.session_state.const['N_PROMPTS']
    
    if prompt_idx== 0 or st.session_state.cache['input_image'] is None:
        st.session_state.cache['input_image']= get_input_image_name(iteration//5)
    
    if st.session_state.cache['input_image'] is None:
        st.warning("No more images to display. Evaluation complete.")
        st.stop()
        
    st.session_state.cache['output_image']= get_output_image_name(iteration)
    return st.session_state.cache

def get_prompt(iteration):
    return st.session_state.df_Prompts_Final_Categories_with_Image_Paths['Prompt'][iteration]

def get_challenges(iteration)-> list[str]:
    string_of_challenges= st.session_state.df_Prompts_Final_Categories_with_Image_Paths['Challenge Category'][iteration]
    list_of_challenges= string_of_challenges.split(',')
    return ["Quality", "Aesthetics"] + [x.strip() for x in list_of_challenges]

def update_records(iteration, challenge, rating):
    rating_as_int= int(st.session_state.const['rating_conversion'][rating])
    st.session_state.df_Rating_Template_Final.at[iteration, challenge]= rating_as_int
    
     
if 'iteration' not in st.session_state: 
    
    start= st.number_input("Enter the start iteration to resume (e.g., 0):", min_value=1, max_value=250, value=1, step= 1)
        
    if st.button("Begin Evaluation"):
        st.session_state.iteration= start -1
        st.session_state.ratings = {}
        st.rerun()
    
if 'iteration' in st.session_state:
    iteration= st.session_state.iteration
    
    if iteration < 250:
        if 'current_iteration' not in st.session_state or st.session_state.current_iteration != iteration:
            st.session_state.images= get_images(iteration)
            st.session_state.prompt= get_prompt(iteration)
            st.session_state.challenges= get_challenges(iteration)
            st.session_state.current_iteration= iteration
            st.session_state.ratings[iteration]= {x: None for x in st.session_state.challenges} 
        
        images= st.session_state.images
        prompt= st.session_state.prompt
        challenges= st.session_state.challenges
        
        if st.button("Evaluate another model"):
            for key in st.session_state:
                del st.session_state[key]
            st.rerun()
        
        st.markdown(
            f"""
            <div style="display: flex; justify-content">
                <h4 style="margin: 0;">Progress: <span style="color: #0a84ff;">{iteration+1}/250</span></h4>
            </div>
            """, 
            unsafe_allow_html=True
        )
        progress = (iteration + 1) / 250
        
            
        st.progress(progress)
        if st.button("Back"):
            st.session_state.iteration= max(st.session_state.iteration -1, 0)
            st.rerun()
            
        st.header(f"Prompt: {prompt}", divider= 'gray')
        col1, col2, col3= st.columns(3, vertical_alignment= 'center')
        
        with col2:
            st.write("**input image**")
            st.image(images['input_image'], width=400)
        with col3:
            st.write("**output image**")
            st.image(images['output_image'], width=400)
        
        with col1:
            for challenge in challenges:
                st.session_state.ratings[iteration][challenge]= st.radio(f"Rate the output image for {challenge}", ["Very Good", "Good", "Decent", "Okayish", "Poor", "Very Poor"], key=f"rating_{iteration}_{challenge}", index= None)

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
                st.rerun()
            else:
                st.warning("Please rate all challenges before proceeding.")
    else:
        st.write("### Evaluation Complete.")