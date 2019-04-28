import requests
from requests.auth import HTTPBasicAuth


def get_ml_data(temp, humidity, light):
    ''' returns a dict of the predicted soil moisture '''
    # need to login to the API first
    r = requests.get('http://192.168.0.27:5000/login',
                     auth=HTTPBasicAuth('jimmy@gmail.com', 'password')).json()
    # building headers to authenticate on backend
    headers = {
        "content-type": 'application/json',
        "x-access-token": r['token']
    }
    # will post these to the server to be predicted upon
    body = {
        'temp': temp,
        'humidity': humidity,
        'light': light
    }
    res = requests.post('http://192.168.0.27:5000/predict', headers=headers, json=body)
    mldata = res.json()
    return_me = {
        'knn_pre': mldata['knn_prediction'],
        'svm_pre': mldata['svm_prediction'],
        'rf_pre': mldata['rf_prediction'],
        'knn_acc': format(mldata['KNN_accuracy'], '.0%'),
        'svm_acc': format(mldata['SVM_accuracy'], '.0%'),
        'rf_acc': format(mldata['RF_accuracy'], '.0%')
    }
    return return_me













