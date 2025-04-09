# import streamlit as st
# import pandas as pd
# #from preprocessor import evaluate
# from preprocessor import evaluate

# def write_to_file(filepath, data):
#     with open(filepath, 'w') as f:
#         f.write(data)

# st.title('Answer Validation model')
# question = st.file_uploader('Choose Question File',type=['txt'])
# model = st.file_uploader('Choose Model Answer File',type=['txt'])
# answers = st.file_uploader('Choose Answer Files',type=['txt'],accept_multiple_files=True)
# button = st.button('Evaluate')
# if button :
#     if question is not None and model is not None and answers is not None:
#         write_to_file('Data\\question.txt', question.getvalue().decode('utf-8'))
#         # write_to_file('Data\\question.txt', question.getvalue().decode('utf-8'))
#         write_to_file('Data\\model.txt', model.getvalue().decode('utf-8'))
        

#         for i, answer in enumerate(answers):
#             write_to_file(f'Data\\answer{i+1}.txt', answer.getvalue().decode('utf-8'))
#         evaluate(len(answers))
#         df = pd.read_csv('Data\\dataset.csv')
#         st.write(df.head())
#         st.download_button("Download CSV",data=df.to_csv().encode('utf-8'),file_name = 'marks.csv',mime='text/csv')
#     else:
#         st.error('Please upload all the files')


import streamlit as st
import pandas as pd
from preprocessor import evaluate

def write_to_file(filepath, data):
    with open(filepath, 'w') as f:
        f.write(data)

st.title('Answer Validation Model')

question = st.file_uploader('Choose Question File', type=['txt'])
model = st.file_uploader('Choose Model Answer File', type=['txt'])
answers = st.file_uploader('Choose Answer Files', type=['txt'], accept_multiple_files=True)

button = st.button('Evaluate')

if button:
    if question is not None and model is not None and answers is not None:
        
        write_to_file('Data\\question.txt', question.getvalue().decode('utf-8'))
        write_to_file('Data\\model.txt', model.getvalue().decode('utf-8'))

        for i, answer in enumerate(answers):
            # write_to_file(f'Data\\answer{i+1}.txt', answer.getvalue().decode('utf-8'))
            write_to_file(f'Data\\answer{i+1}.txt', answer.getvalue().decode('utf-8', errors='ignore'))

        
        evaluate(len(answers))

        df = pd.read_csv('Data\\dataset.csv')

        st.subheader("Marks Obtained:")
        st.write(df.head())

        # Display answers along with marks
        # st.subheader("Answers with Marks:")
        # for i in range(len(answers)):
        #     st.markdown(f"### Answer {i+1}")
            
        #     with open(f'Data\\answer{i+1}.txt', 'r') as f:
        #         ans_text = f.read()
            
        #     st.text_area(f"Student Answer {i+1}", ans_text, height=200)

        # st.download_button("Download CSV", data=df.to_csv().encode('utf-8'), file_name='marks.csv', mime='text/csv')
        

        for i in range(len(answers)):
            with open(f'Data\\answer{i+1}.txt', 'r', encoding='utf-8', errors='ignore') as f:
                ans_text = f.read()
                
                marks = df.loc[i, 'Marks']  
                total_marks = df.loc[i, 'Total Score']  

                st.markdown(f"#### Marks Obtained: {round(total_marks,1)}/{round(marks,1)}")
                
                st.markdown(f"### Answer {i+1}")
                st.write(ans_text)
        st.download_button("Download CSV", data=df.to_csv().encode('utf-8'), file_name='marks.csv', mime='text/csv')

               


        
        
        

    else:
        st.error('Please upload all the files')
