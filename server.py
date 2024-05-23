import io
from settings.vonfig import config
import matplotlib.pyplot as plt
from flask import Flask, Response, request, jsonify

app = Flask(__name__)

@app.route('/plot', methods=['POST'])
def plot_endpoint():
    # Get the request body
    request_body = request.get_data(as_text=True)
    # Create the plot
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Plot Example')

    # Save the plot as bytes
    image_bytes = io.BytesIO()
    plt.savefig(image_bytes, format='png')
    image_bytes.seek(0)
    print(request_body)
    # Return the plot as an HTTP response
    return Response(image_bytes, mimetype='image/png')

@app.route('/config', methods=['GET'])
def config_endpoint():
    return jsonify(config)

if __name__ == '__main__':
    app.run()