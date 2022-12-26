import secrets
from flask import Flask, send_file, send_from_directory
from flask import jsonify, make_response, request, session
from flask_httpauth import HTTPBasicAuth
from logger import trace, exc
from api_app.views import EMPLOYEE as emp

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = 'tIZs2IzxoCTCd0_SkJK4fz7gRNQ'.encode('utf-8')


@auth.verify_password
def authenticate(username, password):
    """
    Authenticating user credential
    """
    try:
        if username and password:
            auth_status = emp.read_auth_details(username)
            if auth_status:
                session['id'] = secrets.token_urlsafe(20)
                return True
            else:
                return False
        return False
    except Exception as e:
        exc.exception(f'Authentication error : {e}')
        return make_response(jsonify({'message': 'Internal server Issue:'}), 500)


@app.route('/')
@auth.login_required
def login():
    """
    This function is used to created user login and to generate user session key
    """
    try:
        if session['id']:
            trace.info("Login success - Session id created")
            return jsonify({"Status":"Login Success", "Access token": session['id']})
        else:
            session['id'] = secrets.token_urlsafe(20)
            trace.info("Login success - Session id created")
            return jsonify({"Status":"Login Success", "Access token": session['id']})
    except Exception as e:
        exc.exception(f'Error while user login: {e}')
        return make_response(jsonify({'message': 'Internal server Issue:'}), 500)


@app.route('/api/employee/register', methods=["GET", "POST"])
def emp_register():
    try:
        trace.info("Processing New Employee Registration")
        res, make = emp.insert_emp_details(request)
        if make:
            return make_response(jsonify(res), make)
        else:
            return jsonify(res)
    except Exception as e:
        exc.exception(f'Error while registration : {e}')
        return make_response(jsonify({'message': 'Internal server Issue:'}), 500)


@app.route('/api/employee/reports', methods=["GET", "POST"])
def emp_reports():
    try:
        trace.info("Processing employee attendance reports")
        res, make = emp.get_emp_atten_dates(request)
        if make:
            return make_response(jsonify(res), make)
        else:
            return jsonify(res)
    except Exception as e:
        exc.exception(f'Error while processing employee attendance report : {e}')
        return make_response(jsonify({'message': 'Internal server Issue:'}), 500)


@app.route('/api/employee/<string:tab>', methods=["GET", "POST"])
def emp_atten_reports(tab):
    try:
        trace.info("Processing employee reports")
        res, make = emp.get_all_emp_atten_report(request, tab)
        if make:
            return make_response(jsonify(res), make)
        else:
            return jsonify(res)
    except Exception as e:
        exc.exception(f'Error while Processing employee reports : {e}')
        return make_response(jsonify({'message': 'Internal server Issue:'}), 500)


@app.route('/api/employee/download/<string:tab>', methods=["GET", "POST"])
def emp_reports_download(tab):
    try:
        trace.info("Processing excel reports")
        res_path, make = emp.get_all_emp_atten_report(request, tab)
        return make_response(send_file(res_path, as_attachment=True, mimetype='xlsx', download_name="report.xlsx"), 200)
    except Exception as e:
        exc.exception(f'Error while downloading the reports files : {e}')
        return make_response(jsonify({'message': 'Internal server Issue:'}), 500)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)