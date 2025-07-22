import sys, logging, json
from time import time, sleep
from pprint import pprint # just for debugging sometimes
from flask import Flask, render_template, jsonify, request, Response
from werkzeug.exceptions import abort
from pympler import asizeof

package_directory = "/reporting/python/"
sys.path.append(package_directory)

from flask_restful import Api
from flasgger import Swagger, swag_from
# from flask_caching import Cache

from libs import api_courses, api_enrollments, api_sis_users, api_grades, api_assessment_answers, logs_dict, swagger_docs, api_nwri_eligible_enrolled, api_eligibleNotEnrolled, api_eligibleAndEnrolled, api_pets
from root import common_params
from root.libs import send_email
from libs import check_api_key, return_messages

app = Flask(__name__)
Flask(__name__).logger.setLevel(logging.DEBUG)
api = Api(app)
app.config['SECRET_KEY'] = 'xxxxxxxxx'

###################################################
################ API Endpoints ####################
###################################################


# Configuring Swagger
app.config['SWAGGER'] = {
    'title': 'My API',
    'uiversion': 3,
    "specs_route": "/swagger/"
}
swagger = Swagger(app)


@app.route('/')
def index():
    return render_template('index.html') #, posts=cursor.fetchall())

@app.route('/view_logs')
def view_logs(): 
    return render_template('view_logs.html', final_dict=logs_dict.get_logs())


#########################
# API Endpoints
#########################
# cache_timeout = 60
# if common_params.get_env() == 'STAGING' or common_params.get_env() == 'TEST':
#     print('Dev Environment!  Cache timeout forced to 1 second')
#     cache_timeout = 1

def too_slow(msg):
    error_dict = {
        "From": "SLOWAPI@xxxx.xxxx.xxxxxx.ufl.edu",
        "To": common_params.api_warning_list,
        "Subject": msg,
        "Body": msg,
        "FromDisplayName": "APIWarning-Long Request",
    }
    send_email.send_out_email(error_dict)

def start_session(end_point):
    if request.headers.get('ApiKey') is None:
        return False
    session_id = str(time())+'_'+request.headers.get('ApiKey')
    if not check_api_key.validate_key(end_point, request.headers.get('ApiKey'), session_id):
        return False
    print(session_id + ':'+end_point+' Request Started:', flush=True)
    #if not os.path.exists(ip_log): open(ip_log, "x").close()
    #with open(ip_log, "a") as f: 
    #    f.write(request.remote_addr + '\n')
    #    f.flush()
    return session_id

@app.route('/pets')
@swag_from(swagger_docs.swagger_dict["pets"])
def pets(): 
    start_time = time()
    session_id = start_session('/pets')
    if not session_id: return return_messages.noway    
    paginated_result = api_pets.get_pets(str(session_id))
    # Handle error response if it's not a dict
    if not isinstance(paginated_result, dict):
        return paginated_result
    result_dict = {
        'data': paginated_result.get('data'),
        'total_count': paginated_result.get('total_count'),
        'total_pages': paginated_result.get('total_pages'),
        'current_page': paginated_result.get('current_page'),
        'per_page': paginated_result.get('per_page')
    }
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return Response(json.dumps(result_dict, indent=2), mimetype='application/json')

@app.route('/courses')
@swag_from(swagger_docs.swagger_dict["courses"])
def all_courses(): 
    start_time = time()
    session_id = start_session('/courses')
    if not session_id: return return_messages.noway    
    start_time = time()
    result_dict = api_courses.get_courses(str(start_time))
    result_dict.update({'warning_message': 'Warning: This endpoint returns full data, which may be deprecated in favor of segmentation in the future.'})
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return jsonify(result_dict)


@app.route('/enrollments')
@swag_from(swagger_docs.swagger_dict["enrollments"])
def enrollments(): 
    start_time = time()
    session_id = start_session('/enrollments')
    if not session_id: return return_messages.noway    
    paginated_result = api_enrollments.get_enrollments(str(session_id))
    # Handle error response if it's not a dict
    if not isinstance(paginated_result, dict):
        return paginated_result
    result_dict = {
        'data': paginated_result.get('data'),
        'total_count': paginated_result.get('total_count'),
        'total_pages': paginated_result.get('total_pages'),
        'current_page': paginated_result.get('current_page'),
        'per_page': paginated_result.get('per_page'),
        'warning_message': 'Warning: This endpoint returns full data, which may be deprecated in favor of segmentation in the future.'
    }
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return Response(json.dumps(result_dict, indent=2), mimetype='application/json')

@app.route('/sis_users')
@swag_from(swagger_docs.swagger_dict["sis_users"])
def sis_users(): 
    start_time = time()
    session_id = start_session('/sis_users')
    if not session_id: return return_messages.noway
    paginated_result  = api_sis_users.get_sis_users(str(session_id))
    # Handle error response if it's not a dict
    if not isinstance(paginated_result, dict):
        return paginated_result
    result_dict = {
        'data': paginated_result.get('data'),
        'total_count': paginated_result.get('total_count'),
        'total_pages': paginated_result.get('total_pages'),
        'current_page': paginated_result.get('current_page'),
        'per_page': paginated_result.get('per_page'),
        'warning_message': 'Warning: This endpoint returns full data, which may be deprecated in favor of segmentation in the future.'
    }
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return Response(json.dumps(result_dict, indent=2), mimetype='application/json')

@app.route('/grades')
@swag_from(swagger_docs.swagger_dict["grades"])
def grades(): 
    start_time = time()
    session_id = start_session('/grades')
    if not session_id: return return_messages.noway    
    paginated_result = api_grades.get_grades(str(session_id))
    # Handle error response if it's not a dict
    if not isinstance(paginated_result, dict):
        return paginated_result
    result_dict = {
        'data': paginated_result.get('data'),
        'total_count': paginated_result.get('total_count'),
        'total_pages': paginated_result.get('total_pages'),
        'current_page': paginated_result.get('current_page'),
        'per_page': paginated_result.get('per_page'),
        'warning_message': 'Warning: This endpoint returns full data, which may be deprecated in favor of segmentation in the future.'
    }
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return Response(json.dumps(result_dict, indent=2), mimetype='application/json')

@app.route('/assessment_answers')
@swag_from(swagger_docs.swagger_dict["assessment_answers"])
def assessment_answers(): 
    start_time = time()
    session_id = start_session('/assessment_answers')
    if not session_id: return return_messages.noway    
    paginated_result = api_assessment_answers.get_assessment_answers(str(session_id))
    # Handle error response if it's not a dict
    if not isinstance(paginated_result, dict):
        return paginated_result
    result_dict = {
        'data': paginated_result.get('data'),
        'total_count': paginated_result.get('total_count'),
        'total_pages': paginated_result.get('total_pages'),
        'current_page': paginated_result.get('current_page'),
        'per_page': paginated_result.get('per_page'),
        'warning_message': 'Warning: This endpoint returns full data, which may be deprecated in favor of segmentation in the future.'
    }
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return Response(json.dumps(result_dict, indent=2), mimetype='application/json')

@app.route('/nwri_Overview')
@swag_from(swagger_docs.swagger_dict["nwri_Overview1"])
def nwri_eligible_enrolled(): 
    print("Incoming Header, lets debug")
    for k, v in request.headers.items():
        print(f"{k}: {v}", flush=True)
    start_time = time()
    session_id = start_session('/nwri_Overview')
    if not session_id: return return_messages.noway    
    result_dict = {}
    # result_dict['data'] = { "hello": "world"}
    result_dict['data'] = api_nwri_eligible_enrolled.get_nwri_eligible_enrolled(str(session_id))
    print(result_dict['data'])
    # result_dict['records'] = len(result_dict['data'])
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return jsonify(result_dict)

@app.route('/eligibleNotEnrolled')
@swag_from(swagger_docs.swagger_dict["eligibleNotEnrolled"])
def eligibleNotEnrolled(): 
    print("Incoming Header, lets debug")
    for k, v in request.headers.items():
        print(f"{k}: {v}", flush=True)
    start_time = time()
    session_id = start_session('/eligibleNotEnrolled')
    if not session_id: return return_messages.noway    
    result_dict = {}
    result_dict['data'] = api_eligibleNotEnrolled.get_eligibleNotEnrolled(str(session_id))
    result_dict['records'] = len(result_dict['data'])
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return jsonify(result_dict)

@app.route('/eligibleAndEnrolled')
@swag_from(swagger_docs.swagger_dict["eligibleAndEnrolled"])
def eligibleAndEnrolled(): 
    print("Incoming Header, lets debug")
    for k, v in request.headers.items():
        print(f"{k}: {v}", flush=True)
    start_time = time()
    session_id = start_session('/eligibleAndEnrolled')
    if not session_id: return return_messages.noway    
    result_dict = {}
    result_dict['data'] = api_eligibleAndEnrolled.get_eligibleAndEnrolled(str(session_id))
    result_dict['records'] = len(result_dict['data'])
    if (time() - start_time) > common_params.api_max_execution_seconds: too_slow("Sessionid:"+session_id+": A request took " + str(str(time() - start_time)) + " seconds",)
    print(session_id + ':Execution seconds:'+str(time() - start_time)+":Bytes sent: " + (str(asizeof.asizeof(result_dict))), flush=True) 
    return jsonify(result_dict)