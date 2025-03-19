import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
from flask import Flask, render_template

input_file = 'dirtydata.csv'
output_file = 'cleandata.csv'

# Load the dataset
data = pd.read_csv(input_file)

# Inspect the dataset
print(data.head())
print(data.info())
print(data.isnull().sum())


data.rename(columns={'BloodPressure': 'BP'}, inplace = True)
data = data.drop(["DiabetesPedigreeFunction", "Id"], axis=1)
data = data.drop(index=range(26,2768))

sample_data = data.sample(n= 20, random_state=42)

data.to_csv(output_file, index=False)
        
print("Data has been cleaned! See here: ", output_file)

numeric_cols = ['Pregnancies', 'Glucose', 'BP', 'SkinThickness', 'Insulin', 'BMI', 'Age']

stats_dictionary = {}

for col in numeric_cols:
    stats_data = data[col]
        
    stats_dictionary[col] = {
            'Mean': stats_data.mean(),
            'Median': stats_data.median(),
            'Mode': stats_data.mode().iloc[0] if not stats_data.mode().empty else np.nan,
            'Range': stats_data.max() - stats_data.min()
        }
        
print(stats_dictionary)


stats_df = pd.DataFrame(stats_dictionary).transpose()
print(stats_df)

#box plot for glucose
graph1 = px.box(data, x='Outcome', y='Glucose', color='Outcome', title= 'Glucose Level Distribution by Outcome',
              labels={'Glucose': 'Glucose Levels', 'Outcome': 'Type of Case'},
              color_discrete_sequence= px.colors.qualitative.Set1)
graph1_html = graph1.to_html(full_html=False, include_plotlyjs="cdn")
#fig1.show()

graph2 = px.scatter(data, x='Age', y='BMI', color='Outcome', title='Age vs BMI by Outcome',
                  labels={'Age':'Age', 'BMI':'BMI'}, 
                  color_discrete_sequence=px.colors.qualitative.Set1, )
graph2_html = graph2.to_html(full_html=False, include_plotlyjs="cdn")
#fig2.show()

graph3 = px.histogram(data, x='BP', color='Outcome', title='Blood Pressure Distribution by Outcome',
                    labels={'BP':'Blood Pressure'}, barmode='overlay', nbins=20,
                    color_discrete_sequence=px.colors.qualitative.Set2)
graph3_html = graph3.to_html(full_html=False, include_plotlyjs="cdn")
#fig3.show()

graph4 = px.scatter(data, x='SkinThickness', y='Insulin', color='Outcome', title='Skin Thickness vs Insulin by Outcome',
                  labels={'SkinThickness':'SkinThickness', 'Insulin':'Insulin Levels'},
                  color_discrete_sequence=px.colors.qualitative.Set3)
graph4_html = graph4.to_html(full_html=False, include_plotlyjs="cdn")
#fig4.show()

graph5 = px.strip(data, x='Outcome', y='Pregnancies', color='Outcome', title='Pregnancies by Outcome',
                labels={'Pregnancies':'Number of Pregnancies', 'Outcome':'Type of Case'},
                color_discrete_sequence=px.colors.qualitative.Set1)
graph5_html = graph5.to_html(full_html=False, include_plotlyjs="cdn")
#fig5.show()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/")
def graphs():
    return render_template(
        'graphs.html',
        graph1=graph1_html,
        graph2=graph2_html,
        graph3=graph3_html,
        graph4=graph4_html,
        graph5=graph5_html
    )
@app.route("/survey")
def survey():
    return render_template("survey.html")

@app.route("/suggestions")
def suggestions():
    return render_template("suggestions.html")

@app.route("/references")
def references():
    return render_template("home.html")


        
if __name__ =="__main__":
    app.run(host='0.0.0.0', port=5001, debug=False)
    
