import streamlit as st
from core.model import analyze_patient
from core.safety import quick_safety_check
from core.hospital_finder import find_hospitals
from core.case_lab import generate_case, answer_student_question, review_reasoning
import urllib.parse

st.set_page_config(page_title='CuraGlide',page_icon='🏥',layout='wide')
if 'page' not in st.session_state: st.session_state.page='Home'
for k,v in {'case':None,'conversation':[],'review':None}.items(): st.session_state.setdefault(k,v)

def nav(name): st.session_state.page=name
with st.sidebar:
    st.title('🏥 CuraGlide')
    st.caption('Your well-being in every step — accessed from a single touch.')
    for name,icon in [('Home','🏠'),('Patient Mode','👤'),('Hospital Finder','📍'),('Case Lab','🧪')]:
        if st.button(f'{icon} {name}',use_container_width=True): nav(name); st.rerun()
    st.divider(); st.caption('Health information and education only — not a replacement for professional medical care.')

if st.session_state.page=='Home':
    st.title('🏥 CuraGlide'); st.subheader('Your well-being in every step — accessed from a single touch.')
    a,b,c=st.columns(3)
    with a: st.markdown('### 👤 Patient Mode'); st.write('Share symptoms and receive cautious AI-powered health-information guidance.'); st.button('Start Patient Mode',on_click=nav,args=('Patient Mode',),use_container_width=True)
    with b: st.markdown('### 📍 Hospital Finder'); st.write('Search for hospitals near a city or area and open directions.'); st.button('Find Hospitals',on_click=nav,args=('Hospital Finder',),use_container_width=True)
    with c: st.markdown('### 🧪 Case Lab'); st.write('Practice clinical reasoning using fictional educational cases.'); st.button('Open Case Lab',on_click=nav,args=('Case Lab',),use_container_width=True)
    st.info('CuraGlide does not provide confirmed diagnoses or emergency services.')

elif st.session_state.page=='Patient Mode':
    st.title('👤 Patient Mode'); st.caption('Provide only information you are comfortable sharing.')
    with st.form('patient_form'):
        c1,c2=st.columns(2)
        age=c1.number_input('Age',1,120,18); gender=c2.text_input('Sex or gender (optional)')
        weight=c1.number_input('Weight (kg)',1.0,500.0,60.0); height=c2.number_input('Height (cm)',30.0,300.0,170.0)
        conditions=st.text_input('Existing medical conditions'); medications=st.text_input('Current/recent medications'); allergies=st.text_input('Allergies'); history=st.text_area('Important medical history'); symptoms=st.text_area('What symptoms or concerns are you experiencing?'); duration=st.text_input('How long have you had them?')
        submitted=st.form_submit_button('Analyze',type='primary')
    if submitted:
        data=locals(); safety=quick_safety_check(symptoms); st.subheader('🚦 Safety guidance'); st.warning(safety['message']) if safety['level']=='URGENT ATTENTION' else st.info(safety['message'])
        with st.spinner('CuraGlide is reviewing the information...'):
            result=analyze_patient({k:data[k] for k in ['age','gender','weight','height','conditions','medications','allergies','history','symptoms','duration']})
        if result['success']: st.markdown(result['analysis'])
        else: st.error(result['error'])

elif st.session_state.page=='Hospital Finder':
    st.title('📍 Hospital Finder'); st.caption('Searches public OpenStreetMap/Nominatim data. Results may be incomplete or unavailable.')
    location=st.text_input('Enter a city or area',placeholder='Example: Lahore, Pakistan')
    if st.button('Search hospitals',type='primary') and location:
        with st.spinner('Searching...'): result=find_hospitals(location)
        if not result['success']: st.error(result['error'])
        else:
            st.success(f"Showing hospitals near {result['origin']['display_name']}")
            for h in result['hospitals']:
                st.markdown(f"### 🏥 {h['name']}"); st.write(h['address']); st.caption(h['distance'])
                q=urllib.parse.quote_plus(f"{h['latitude']},{h['longitude']}"); st.link_button('Open directions',f'https://www.google.com/maps/search/?api=1&query={q}')

elif st.session_state.page=='Case Lab':
    st.title('🧪 Case Lab'); st.warning('⚠️ Educational use only. Cases are fictional and not clinical advice.')
    c1,c2=st.columns(2); topic=c1.text_input('Topic',placeholder='Neurology, cardiology, respiratory...'); difficulty=c1.selectbox('Difficulty',['Beginner','Intermediate','Advanced']); case_type=c2.selectbox('Case type',['Diagnostic mystery','Emergency presentation','Patient interview','Clinical reasoning challenge','Differential diagnosis']); custom=c2.text_area('Optional custom request')
    if st.button('🚀 Generate New Case',type='primary'):
        if not topic: st.warning('Please enter a topic.')
        else:
            with st.spinner('Generating fictional case...'): result=generate_case(topic,difficulty,case_type,custom)
            if 'error' in result: st.error(result['error'])
            else: st.session_state.case=result['case']; st.session_state.conversation=[]; st.session_state.review=None; st.rerun()
    case=st.session_state.case
    if case:
        st.divider(); st.subheader(case.get('title','Fictional Case')); st.info(case.get('professor_intro',''))
        patient=case.get('patient',{}); st.markdown(f"**Patient:** {patient.get('description','')}"); st.write(patient.get('opening_presentation',''))
        st.markdown('### Initial information')
        for x in case.get('initial_information',[]): st.write('• '+str(x))
        for item in st.session_state.conversation:
            st.markdown(f"**You:** {item['q']}"); st.write(f"**Professor:** {item['a']}");
        question=st.text_input('Ask the professor a question',key='case_q')
        if st.button('Ask question') and question:
            with st.spinner('Professor is responding...'): ans=answer_student_question(case,question,st.session_state.conversation)
            if 'error' in ans: st.error(ans['error'])
            else: st.session_state.conversation.append({'q':question,'a':ans.get('answer',''),'teaching_point':ans.get('teaching_point','')}); st.rerun()
        reasoning=st.text_area('Your clinical reasoning / final thoughts')
        if st.button('🎓 Get Professor Review') and reasoning:
            with st.spinner('Reviewing reasoning...'): rr=review_reasoning(case,reasoning,st.session_state.conversation)
            if 'error' in rr: st.error(rr['error'])
            else: st.session_state.review=rr['review']
        if st.session_state.review:
            r=st.session_state.review; st.subheader('🎓 Professor Review'); st.write(r.get('overall_feedback',''))
            for title,key in [('What went well','what_went_well'),('What was missed','what_was_missed'),('Important warning signs','important_warning_signs')]:
                st.markdown(f'**{title}**'); [st.write('• '+str(x)) for x in r.get(key,[])]
            st.markdown('**Key lesson:** '+str(r.get('key_lesson','')))
