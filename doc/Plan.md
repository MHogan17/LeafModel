1 - Requirements Specification
 
    This program takes a keyword argument to run a numerical experiment. The user will then specify the environmental 
    conditions of the specified experiement. The experiment will be displayed to the console as it processes. Once 
    finished processing, the user can choose whether or not to save the experiment.

2 - System Design   
        
    Input: 
        To enter the program, an experiment type keyword is required.
    Processing:
        Check if the experiment type is a valid type. If so, prompt the user for the environmental conditions of the
        experiment. Given they are valid, create the specified environment and initialize the experimental array.
        Run the experiment.
        
            Light Experiments: 
                With the array and environment, calculate and display the next arrays recursively by calling 
                calculate_next, initialized at t=0 up to t=20. Each time  
                times, indicating the delay of the carbon in the carbon-signal interaction.  
                    - While the number of iterations is less than 400:
                        - At each position on array1:
                            - Clear neighbor lists.
                            - Append values of carbon dioxide and epidermal water potential to appropriate lists from
                              the neighboring cells on array2.
                            - Calculate values for next time step.
                            - Set new values.
                            - Record temperature in output file.
                        - Copy new carbon dioxide and water potential values to array2.
                        - Increase iteration count.
                    - Save output file.
                    
                