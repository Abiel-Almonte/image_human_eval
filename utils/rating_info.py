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