import io
import json
import matplotlib
matplotlib.use('Agg')
from settings.vonfig import config
import matplotlib.pyplot as plt
from flask import Flask, Response, request, jsonify, send_file
from client_side.client import client
from server_side.workers import phone_support
from server_side.vm import vm_deliver
from server_side.server import server
from settings.statistic import statistic_collector
from simpy import Environment
import matplotlib.pyplot as plt
from settings.vonfig import config
from flask_cors import CORS
import warnings
import pandas
import numpy as np


app = Flask(__name__)
result = {}
skip = 0

def parse_result():
    df = pandas.DataFrame()
    warnings.filterwarnings("ignore")
    for key in statistic_collector.load:
        if key[:10] == "client_vms":
            if len(statistic_collector.load[key]) == 1 and statistic_collector.load[key][0] == 0:
                continue
            # plt.plot(statistic_collector.load[key])
            x = [np.NaN] * (config["runtime"] // 2 - len(statistic_collector.load[key])) + statistic_collector.load[key]
            try:
                df[key] = np.array(x)
            except:
                print(key)
    df['mean'] = df.mean(axis=1)        
    df['median'] = df.median(axis=1)        
    df["sum"] = df.sum(axis=1)
    df1 = df.iloc[skip:]
    return df

@app.route('/plot', methods=['GET'])
def plot_endpoint():
    df = parse_result()
    plt.plot(df['mean'], label="среднее кол-во виртуальных машин")
    try:
        plt.vlines([x // 2 - skip for x in statistic_collector.load["break_time_hadoop_claster"]], df['mean'].max() * 0.95, df['mean'].max() * 1.05, 'y', label="неполадки в кластере данных")
    except:
        pass
    try:
        plt.vlines([x // 2 - skip for x in statistic_collector.load["break_time_proxmox_claster"]], df['mean'].mean() * 0.45, df['mean'].mean() * 0.65, 'r')
    except:
        pass
    plt.legend()

    # Save the plot as bytes
    image_bytes = io.BytesIO()
    plt.savefig(image_bytes, format='png')
    image_bytes.seek(0)
    # Return the plot as an HTTP response
    del df
    plt.clf()
    statistic_collector.unload()
    return Response(image_bytes, mimetype='image/png')

@app.route('/result', methods=['GET'])
def get_result():
    try:
        return send_file(statistic_collector.result_file_name)
    except Exception as e:
        return str(e) + ' ' + str(statistic_collector.result_file_name)

@app.route('/config', methods=['GET'])
def get_config_endpoint():
    return jsonify(config)

@app.route('/config', methods=['POST'])
def post_config_endpoint():
    # config.update(request.get_data(as_text=True))
    config.update(json.loads(request.get_data(as_text=True)))
    env = Environment()
    client(env, phone_support(env), vm_deliver(env, server(env, "server")))
    env.run(until=config["runtime"])
    statistic_collector.save()
    try:
        return send_file(statistic_collector.result_file_name)
    except Exception as e:
        return str(e) + ' ' + str(statistic_collector.result_file_name)

if __name__ == '__main__':
    CORS(app)
    app.run()