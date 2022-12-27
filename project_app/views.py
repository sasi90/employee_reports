import os
import pandas as pd
from datetime import datetime
from copy import deepcopy
from dataaccess import model_details_access as db
from logger import trace, exc


ROOT = os.getcwd()


class EMPLOYEE:

    @staticmethod
    def read_auth_details(user_email):
        """
        This function is used to fetch the default user credential from database
        :param user_email ---> Hr email id
        :return Boolean Success message
        """
        try:
            data_db = db.get_hr_cred(user_email)
            hr_details = []
            for data in data_db:
                hr_details.append(data.fetchall())
            if hr_details[0]:
                return True
            else:
                return False
        except Exception as e:
            exc.exception(f'Error while fetching the user credential: {e}')
            return False

    @staticmethod
    def insert_emp_details(request_param):
        """
        This function will add the new employee details into the database
        :param request_param ---> request parameter
        :return Success message
        """
        try:
            if request_param.method == 'POST':
                json_resp = request_param.json
                trace.info("Collecting the market summaries")
                # "token": "M734ARnzRj59miTyiGWiiUhveYc",
                f_name = json_resp["First Name"]
                l_name = json_resp["Last Name"]
                emp_id = json_resp["Employee Id"]
                email = json_resp["E-Mail Address"]
                phn_num = json_resp["Cell Phone number"]
                depart = json_resp["Department"]
                rep_man = json_resp["Reporting Manager"]
                arg_ddb = [f_name, l_name, emp_id, email, phn_num, depart, rep_man]
                res = db.insert_emp_details(arg_ddb)
                if res:
                    return ['Data inserted successfully', 200]
                else:
                    return ['Data not inserted into DB', 200]
            else:
                return [{'message': 'Invalid API Request'}, 400]
        except Exception as e:
            exc.exception(f'Error while adding new employee details into the DB: {e}')
            return [{'message': 'Unexpected internal server error'}, 500]

    def leave_count(self, data):
        """
           This function handles the data from DB and collect the no of leave counts
           :param: data ---> all employee attendance data
           :return consolidated leave count "final_dict as dictionary values" and data to be write in excel
       """
        try:
            leave = {}
            per_mission = {}
            for dat in data:
                Flag = False
                if dat['sign_in_time'] == '0:00:00' or dat['sign_out_time'] == '0:00:00':
                    Flag = True
                elif str(dat['sign_in_time']).lower() == 'none' or str(dat['sign_out_time']).lower() == 'none':
                    Flag = True
                elif str(dat['sign_in_time']).lower() == 'null' or str(dat['sign_out_time']).lower() == 'null':
                    Flag = True
                else:
                    pass
                if Flag:
                    if dat['emp_id'] in leave:
                        leave[dat['emp_id']] += 1
                    else:
                        leave[dat['emp_id']] = 1
            for dat in data:
                if dat['permission_days'] != '0':
                    if dat['emp_id'] in per_mission:
                        per_mission[dat['emp_id']] += 1
                    else:
                        per_mission[dat['emp_id']] = 1

            final_dic = {}
            emp_id = []
            abs_days = []
            total_leave = []
            permission = []
            for ky, val in leave.items():
                if ky in per_mission:
                    abs = leave[ky] - per_mission[ky]
                    per_mis = per_mission[ky]
                else:
                    abs = leave[ky]
                    per_mis = 0
                dic = {"absent_days":abs, "total_leave_taken":leave[ky], "permission_leave_taken":per_mis}
                final_dic[ky] = dic
                emp_id.append(deepcopy(ky))
                abs_days.append(deepcopy(abs))
                total_leave.append(deepcopy(leave[ky]))
                permission.append(deepcopy(per_mis))

            xl_report = {"Employee ID":emp_id, "No.of Absent days":abs_days, "Total Leave":total_leave, "Permission":permission}

            return final_dic, xl_report

        except Exception as e:
            exc.exception(f'Error while calculating the employee leave counts: {e}')
            return [{'message': 'Unexpected internal server error'}, 500]

    def work_duration(self, data):
        """
           This function handles the data from DB and collect the no of less work duration
           :param data ---> all employee attendance data
           :returns consolidated leave count "res_dic as dictionary values" and data to be write in excel
       """
        try:
            final = []
            res_dic = {}
            for dat in data:
                if dat['sign_in_time'] != '0:00:00' and str(dat['sign_in_time']).lower() != 'none' and str(dat['sign_in_time']).lower() != 'null':
                    if dat['sign_out_time'] != '0:00:00' and str(dat['sign_out_time']).lower() != 'none' and str(
                            dat['sign_out_time']).lower() != 'null':
                        final.append(deepcopy(dat))
                        del_ta = datetime.strptime(dat['sign_out_time'], '%H:%M:%S') - datetime.strptime(
                            dat['sign_in_time'],
                            '%H:%M:%S')
                        dur = [int(x) for x in str(del_ta).split(':')]
                        if dur[0] < 9:
                            if dat['emp_id'] in res_dic:
                                res_dic[dat['emp_id']]['less_work'] += 1
                            else:
                                res_dic[dat['emp_id']] = {'less_work':1}
            emp_ = []
            less_wk = []
            for ky, val in res_dic.items():
                emp_.append(deepcopy(ky))
                less_wk.append(deepcopy(val["less_work"]))

            xl_report = {"Employee ID":emp_, "No.of less work":less_wk}

            return res_dic, xl_report

        except Exception as e:
            exc.exception(f'Error while calculting the employee work duration: {e}')
            return [{'message': 'Unexpected internal server error'}, 500]

    def generate_excel(self, res_data, file_name):
        """"
           This function will generate the report in excel and save in the local directory
           :params res_data ---> consolidated data to be write in excel
                   file_name ---> excel file path
           :returns excel file
       """
        try:
            app_path = os.getcwd()
            file = app_path + '/' + 'docx_download/' + file_name
            df = pd.DataFrame(res_data)
            writer = pd.ExcelWriter(file, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            header_format = workbook.add_format({
                'bold': True,
                'text_wrap': True,
                'valign': 'top',
                'fg_color': '#D7E4BC',
                'border': 1})
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num + 1, value, header_format)

            writer.close()

            return file

        except Exception as e:
            exc.exception(f'Error while generating the excel reports: {e}')
            return [{'message': 'Unexpected internal server error'}, 500]

    @staticmethod
    def get_emp_atten_dates(request_param):
        """
         This function will fetch the data from the DB with respect to the given dates
        :param request_param ---> request parameter
        :returns specified employee attendance report
        """
        try:
            if request_param.method == 'GET':
                json_resp = request_param.json
                # trace.info("Collecting the market summaries")
                # "token": "M734ARnzRj59miTyiGWiiUhveYc",
                emp_id = json_resp["emp_id"]
                fr_date = json_resp["from_date"]
                to_date = json_resp["to_date"]
                arg_ddb = [emp_id, fr_date, to_date]
                data_db = db.get_emp_details_id(arg_ddb)
                if data_db:
                    hr_details = []
                    for data in data_db:
                        hr_details = data.fetchall()
                    if hr_details:
                        # res = [json.dumps(list(data), indent=4, sort_keys=True, default=str).replace(' ', '').replace('\n',
                        #                                                                                         '') for
                        #  data in hr_details]
                        lis_ = [list(data) for data in hr_details]
                        resp = []
                        for dat in lis_:
                            dic = {"emp_id":"", "login_date":"", "sign_in_time":"", "sign_out_time":"", "permission_days":""}
                            dic["login_date"] = str(dat[1])
                            dic["emp_id"] = dat[2]
                            dic["sign_in_time"] = str(dat[3])
                            dic["sign_out_time"] = str(dat[4])
                            dic["permission_days"] = str(dat[5])
                            resp.append(deepcopy(dic))
                        return [sorted(resp, key=lambda k:k['login_date']), 200]
                    else:
                        return ['No data found', 200]
                else:
                    return [{'message': 'Unexpected internal server error'}, 500]
            else:
                return [{'message': 'Invalid API Request'}, 400]
        except Exception as e:
            exc.exception(f'Error while collecting the employee attendance data: {e}')
            return [{'message': 'Unexpected internal server error'}, 500]

    @staticmethod
    def get_all_emp_atten_report(request_param, req_tab):
        """"
        This function will scrab the summary details from the "api.bittrex.com" website
        :param request_param ---> request parameter
        :returns --->  employee report and excel files
        """
        try:
            if request_param.method == 'GET':
                if request_param.args:
                    fr_date = request_param.args["from_date"]
                    to_date = request_param.args["to_date"]
                else:
                    json_resp = request_param.json
                    # trace.info("Collecting the market summaries")
                    # "token": "M734ARnzRj59miTyiGWiiUhveYc",
                    fr_date = json_resp["from_date"]
                    to_date = json_resp["to_date"]
                arg_ddb = [fr_date, to_date]
                data_db = db.get_all_attendance(arg_ddb)
                if data_db:
                    hr_details = []
                    for data in data_db:
                        hr_details = data.fetchall()
                    if hr_details:
                        lis_ = [list(data) for data in hr_details]
                        resp = []
                        for dat in lis_:
                            dic = {"emp_id": "", "login_date": "", "sign_in_time": "", "sign_out_time": "", "permission_days":""}
                            dic["login_date"] = str(dat[1])
                            dic["emp_id"] = dat[2]
                            dic["sign_in_time"] = str(dat[3])
                            dic["sign_out_time"] = str(dat[4])
                            dic["permission_days"] = str(dat[5])
                            resp.append(deepcopy(dic))
                        if req_tab == 'leave_count':
                            res_list, report = EMPLOYEE().leave_count(resp)
                            return [[res_list], None]
                        elif req_tab == 'work_duration':
                            dura_tion, repot = EMPLOYEE().work_duration(resp)
                            return [dura_tion, None]
                        elif req_tab == 'absent':
                            res_list, report = EMPLOYEE().leave_count(resp)
                            xl_path = EMPLOYEE().generate_excel(report, 'leave_report.xlsx')
                            return [xl_path, None]
                        elif req_tab == 'lesswork':
                            res_list, report = EMPLOYEE().work_duration(resp)
                            xl_path = EMPLOYEE().generate_excel(report, 'duration_report.xlsx')
                            return [xl_path, None]
                    else:
                        return ['No data found', 200]
                else:
                    return [{'message': 'Unexpected internal server error'}, 500]
            else:
                return [{'message': 'Invalid API Request'}, 400]
        except Exception as e:
            exc.exception(f'Error while collecting employee attendance data: {e}')
            return [{'message': 'Unexpected internal server error'}, 500]