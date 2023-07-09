from flask import Flask, render_template, request
from datetime import datetime
import pygal
import csv


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    x=[]
    y=[]
    z=[]
    # Default synthetic data
    x = ["Afghanistan","Albania","Angola"]
    y = [647500,28748,1246700]

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

        def checkDataCsv (file_path):
            with open(file_path, 'r') as file:
                reader = csv.reader(file, delimiter=';')
                if len(next(reader))>=3:
                    return True
                else: return False

        if checkDataCsv(file_path):

            x, y, z = read_data_from_csv(file_path)

            warnMess='Данные успешно загружены'

            filtered_idx = list(filter(lambda i: z[i]>10000, range(len(z))))

            x = [x[i] for i in filtered_idx]
            y = [y[i] for i in filtered_idx]

        else:
            warnMess='Данные некорректны'

    chart_svg = create_chart(x, y)

    return render_template('index.html', chart_svg=chart_svg, now=datetime.now(),warnMess = warnMess)

def read_data_from_csv(file_path):
    x = []
    y = []
    z = []

    with open(file_path, 'r') as file:
        reader = csv.reader(file,delimiter=";")
        next(reader)  # Skip the header row
        next(reader)
        for row in reader:
            if len(row) >= 3:
                x.append(row[0])
                y.append(float(row[37].strip() if row[37].strip()!="" else 0))
                z.append(float(row[1].strip() if row[1].strip()!="" else 0))

    return x, y, z


def create_chart(x, y):
    bar_chart = pygal.Bar(width=2000,x_label_rotation=270)
    bar_chart.title = 'Население (Population) стран с площадью (Area(sq km)) более 10.000'
    bar_chart.x_labels = x
    bar_chart.add('Population', y)


    return bar_chart.render().decode().strip()

if __name__ == '__main__':
    app.run()
