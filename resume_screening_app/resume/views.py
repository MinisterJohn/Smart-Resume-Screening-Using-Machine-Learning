from django.shortcuts import render
import re
import joblib

def clean_resume(resume_text):
    resume_text = re.sub('http\S+\s*', ' ', resume_text)  # remove URLs
    resume_text = re.sub('RT|cc', ' ', resume_text)  # remove RT and cc
    resume_text = re.sub('#\S+', '', resume_text)  # remove hashtags
    resume_text = re.sub('@\S+', '  ', resume_text)  # remove mentions
    resume_text = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resume_text)  # remove punctuations
    resume_text = re.sub(r'[^\x00-\x7f]',r' ', resume_text)
    resume_text = re.sub('\s+', ' ', resume_text)  # remove extra whitespace
    return resume_text

def predict_category(resume_text):
    clf = joblib.load('C:\\Users\\MINISTER JOHN\\Desktop\\Chioma Smart Resume\\resume_screening_app\\resume_screening_model.pkl')
    word_vectorizer = joblib.load('C:\\Users\\MINISTER JOHN\\Desktop\\Chioma Smart Resume\\resume_screening_app\\tfidf_vectorizer.pkl')
    
    cleaned_resume = clean_resume(resume_text)
    resume_features = word_vectorizer.transform([cleaned_resume])
    predicted_category = clf.predict(resume_features)
    
    category_names = {
    0: 'Data Science',
    1: 'HR',
    2: 'Advocate',
    3: 'Arts',
    4: 'Web Designing',
    5: 'Mechanical Engineer',
    6: 'Sales',
    7: 'Health and fitness',
    8: 'Civil Engineer',
    9: 'Java Developer',
    10: 'Business Analyst',
    11: 'SAP Developer',
    12: 'Automation Testing',
    13: 'Electrical Engineering',
    14: 'Operations Manager',
    15: 'Python Developer',
    16: 'DevOps Engineer',
    17: 'Network Security Engineer',
    18: 'Project Management Officer',
    19: 'Database',
    20: 'Hadoop',
    21: 'ETL Developer',
    22: 'DotNet Developer',
    23: 'Blockchain',
    24: 'Testing'
}
    predicted_category_name = category_names.get(predicted_category[0], 'Unknown')
    return predicted_category_name

def index(request):
    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '')
        predicted_category = predict_category(resume_text)
        return render(request, 'result.html', {'predicted_category': predicted_category})
    return render(request, 'index.html')
