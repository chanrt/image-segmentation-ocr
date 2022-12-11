# Image Segmentation and Optical Character Recognition
 
 This project was done by Chandan R T as a part of E9 241: Digital Image Processing course offered at IISc Bangalore in fall of 2022
 GitHub repository link: https://github.com/chanrt/image-segmentation-ocr

 Instructions:
 1) The input image must be placed inside the 'inputs' folder.
 2) The main() function in main.py must be called with the name of the input image
 3) All necessary corrections can be turned off or on, inside the main() function of main.py
 4) The main() function will display and return the predicted string of characters
 5) Parameters can be further tweaked in the settings.py file
 
 How to carry out rigorous evaluation:
 1) The evaluator() function in evaluation.py must be called with the name of the input image
 2) The input image must be present in the 'inputs' folder
 3) The transcribed text of the input image must be present in the 'expected_outputs' folder, with the same file name as the input image
 4) The evaluator() function will display the Levenshtein distance between the program output and the expected output, as well as the error
 
 -------------------------------------------------------------------
 Example
 
 Input image:
 ![alt_text](https://i.ibb.co/7n9fB1v/polya-description.png)
 
 Program output:
 in thss classic text george pblya l18871985j offers something
 unique a set ofstratekies foi solving mathelnatical problems
 the heutistic theotetical appioach based on a deep analysis
 of the methods and wles of discovery and invention ptoved
 an inspiration to a geneiation of teachers and students yet the
 lessons ate uttetiy practical pblya ptslliantly demonstiates
 how the true mathematician learns to diaw unexpected analo
 gies tackle ptobiems ftom unusual angles and extiact a little
 more information fiom the data tiaditional mathematics gan
 often seem just a piocess of dcy rigotous dedugtion holv to
 solbe it wondeifully conveys its challenge and excitement as
 a problemsolmng activity
 
 Evaluations:
 Levenshtein distance: 47
 Error: 6.79 %
 
 -------------------------------------------------------------------
 
 Models: there are four trained models here
 1) A Dense Neural Network trained on handwritten data
 2) A Dense Neural Network trained on printed characters data
 3) A Convolutional Neural Network trained on handwritten data
 4) A Convolutional Neural Network trained on printed characters data
 CNNs generally perform better
 You can select the desired model in the arguments of character_recognizer() function in main.py
 
 Datasets:
 1) Hand-written characters dataset: Cohen, G., Afshar, S., Tapson, J., & van Schaik, A. (2017). EMNIST: an extension of MNIST to handwritten letters
 2) Printed characters dataset: T. E. de Campos, B. R. Babu and M. Varma (2009). Character recognition in natural images
 These datasets are not included in the repository due to space concerns.
 You can download these datasets from the links given in the dataset_links.txt file inside the 'data' folder
