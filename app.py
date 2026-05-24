from flask import Flask, render_template, request
import numpy as np

app = Flask(__name__)

# Rational / Lagrange-style interpolation
def rational_interpolation(x_points, y_points, x):

    n = len(x_points)

    numerator = 0
    denominator = 0

    steps = []

    for i in range(n):

        term = 1

        step_text = f"L{i}(x) = "

        for j in range(n):

            if i != j:

                fraction = (
                    (x - x_points[j]) /
                    (x_points[i] - x_points[j])
                )

                term *= fraction

                step_text += (
                    f"(({x} - {x_points[j]}) / "
                    f"({x_points[i]} - {x_points[j]})) × "
                )

        numerator += term * y_points[i]
        denominator += term

        steps.append({

            'basis': f"L{i}(x)",

            'formula': step_text[:-2],

            'value': round(term, 6),

            'weighted': round(term * y_points[i], 6)

        })

    result = numerator / denominator

    return result, steps


@app.route('/', methods=['GET', 'POST'])
def index():

    result = None

    # Step-by-step data
    steps = []

    # Graph data
    chart_x = []
    chart_y = []

    # User input data
    x_points = []
    y_points = []

    user_x = None

    if request.method == 'POST':

        try:

            # Get x points
            x_points = list(map(
                float,
                request.form['x_points'].split(',')
            ))

            # Get y points
            y_points = list(map(
                float,
                request.form['y_points'].split(',')
            ))

            # Interpolation point
            user_x = float(request.form['x'])

            # Calculate interpolation
            result, steps = rational_interpolation(
                x_points,
                y_points,
                user_x
            )

            # Generate graph range
            x_min = min(x_points) - 1
            x_max = max(x_points) + 1

            chart_x = np.linspace(
                x_min,
                x_max,
                200
            )

            # Generate graph y values
            chart_y = [

                rational_interpolation(
                    x_points,
                    y_points,
                    value
                )[0]

                for value in chart_x

            ]

            # Convert numpy array to list
            chart_x = chart_x.tolist()

        except Exception as e:

            result = f"Error: {str(e)}"

    return render_template(

        'index.html',

        result=result,

        # Step-by-step
        steps=steps,

        # Chart
        chart_x=chart_x,
        chart_y=chart_y,

        # Original points
        x_points=x_points,
        y_points=y_points,

        # User interpolation point
        user_x=user_x

    )


if __name__ == '__main__':

    app.run(debug=True)