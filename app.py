from flask import Flask, render_template, request
from datetime import datetime
import pygal
import csv


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file uploaded'

        file = request.files['file']

        if file.filename == '':
            return 'No file selected'

        if not file.filename.endswith('.csv'):
            return 'Invalid file format. Please upload a CSV file.'

        file_path = 'tmp.csv'
        file.save(file_path)

        x, y = read_data_from_csv(file_path)
    else:
        # Default synthetic data
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

    chart_svg = create_chart(x, y)

    return render_template('index.html', chart_svg=chart_svg, now=datetime.now(),)

def read_data_from_csv(file_path):
    x = []
    y = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            x.append(row[0])
            y.append(float(row[1]))

    return x, y

def create_chart(x, y):
    line_chart = pygal.Line()
    line_chart.title = 'Example Chart'
    line_chart.x_labels = x
    line_chart.add('Series', y)

    return line_chart.render().decode().strip()

if __name__ == '__main__':
    app.run()