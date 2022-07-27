import pickle
import streamlit as st
import numpy as np
import pandas as pd

# for regression
#           inverse log the salary
#           apply standard scalar

# 	ssc_p	degree_p	mba_p	hsc_p	workex_No	workex_Yes	mba_t_Mkt&Fin	mba_t_Mkt&HR	degree_t_Comm&Mgmt	degree_t_Others	degree_t_Sci&Tech
#   etest_p	mba_p	ssc_p	hsc_p	workex_Yes	workex_No	mba_t_Mkt&Fin	mba_t_Mkt&HR	gender_M	gender_F

def status():
    # loading the trained model
    pickle_one = open('status_model.pkl', 'rb')
    classifier = pickle.load(pickle_one)
    status = classifier.predict([[float(tenthPercent), float(degreePercent), float(mbaPercent), float(twelfthPercent), workex_No, workex_Yes, mba_t_MktAndFin, mba_t_MktAndHR, degree_t_CommAndMgmt, degree_t_Others, degree_t_SciAndTech]])
    return status[0]

def salary():

    pickle_two = open('salary_model.pkl', 'rb')
    regressor = pickle.load(pickle_two)

    pickle_three = open('standardScalar.pkl', 'rb')
    standardScalar = pickle.load(pickle_three)

    temp = {
         'etest_p': float(entrancePercent),
         'mba_p': float(mbaPercent),
         'ssc_p': float(tenthPercent),
         'hsc_p': float(twelfthPercent),
         'workex_Yes': workex_Yes,
         'workex_No': workex_No,
         'mba_t_MktAndFin': mba_t_MktAndFin,
         'mba_t_MktAndHR': mba_t_MktAndHR,
         'gender_M': gender_M,
         'gender_F': gender_F
    }

    temp_df = pd.DataFrame(temp, index=[0])
    #st.write(temp_df)
    temp_obj = standardScalar.transform(temp_df)
    #st.write(temp_obj)
    salary = regressor.predict(temp_obj)
    #st.write(salary)
    return np.exp(salary)

html_temp = """
    <div style = "padding-bottom:33px;">
    <div style ="background-color:#ff4d4d;padding:13px; border: 5px solid; border-radius: 25px;">
    <h1 style ="color:black;text-align:center;">Placements and Salary Prediction</h1>
    </div>
    <div></div>
    </div>
    """

# display the front end aspect
st.markdown(html_temp, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
     gender = st.radio("Gender", ('Male', 'Female'))
     tenthPercent = st.text_input('10th Percent')
     degreePercent = st.text_input('Degree Percent')

with col2:
     work = st.radio("Work Experience", ("Yes", "No"))
     twelfthPercent = st.text_input('12th Percent')
     entrancePercent = st.text_input('Entrance Percent')

mbaPercent = st.text_input('MBA Percent')

colu1, colu2 = st.columns(2)

with colu1:
     degreeTitle = st.selectbox('UG Degree Title', ('Communication & Management', 'Science & Technology', 'Others'))

with colu2:
     mbaTitle = st.selectbox('MBA Degree Title', ('Marketing & HR', 'Marketing & Finance'))

html_temp1 = """
    <div style = "padding-bottom:30px;">
    </div>
    """

# display the front end aspect
st.markdown(html_temp1, unsafe_allow_html=True)

c1,c2,c3,c4,c5 = st.columns(5)
with c3:
      click = st.button('Predict')

html_temp1 = """
    <div style = "padding-bottom:30px;">
    </div>
    """

# display the front end aspect
st.markdown(html_temp1, unsafe_allow_html=True)

if click:
     if gender == 'Male':
          gender_F = 0
          gender_M = 1
     else:
          gender_F = 1
          gender_M = 0

     if work == 'Yes':
          workex_Yes = 1
          workex_No = 0
     else:
          workex_Yes = 1
          workex_No = 1

     if degreeTitle == 'Communication & Management':
          degree_t_CommAndMgmt = 1
          degree_t_Others = 0
          degree_t_SciAndTech = 0
     elif degreeTitle == 'Science & Technology':
          degree_t_CommAndMgmt = 0
          degree_t_Others = 0
          degree_t_SciAndTech = 1
     else:
          degree_t_CommAndMgmt = 0
          degree_t_Others = 1
          degree_t_SciAndTech = 0

     if mbaTitle == 'Marketing & HR':
          mba_t_MktAndHR = 1
          mba_t_MktAndFin = 0
     else:
          mba_t_MktAndHR = 0
          mba_t_MktAndFin = 1

     val = status()

     if val == 1:
          st.success('You are PLACED!')
          actual_salary = salary()
          actual_salary = np.round(actual_salary[0],2)
          st.write("Your salary package would be ", actual_salary)
     else:
         st.error('SORRY....You are NOT PLACED!')