from dataaccess import DataAccess
from logger import trace, exc


def get_hr_cred(userid):
    """
    Fetch the hr login cred from Database
    :param userid: Hr login email id
    :return: login password
    """
    try:
        av3arDB_CNX = DataAccess.openConnection()
        dbCursor = av3arDB_CNX.cursor()
        dbCursor.callproc("hr_retrive", [userid])
        training_json = dbCursor.stored_results()
        # cache.__setattr__(model_table_key, str(result))
        return training_json
    except Exception as e:
        exc is not None and exc.exception("Error while fetching the user cred from DB")
        return False
    finally:
        DataAccess.closeConnection()


def get_all_attendance(arg_db):
    """
    This function will fetch the employee attendance report between the dates from the database
    :param arg_db: list of arguments for the query
    :return: employee attendance data
    """
    try:
        av3arDB_CNX = DataAccess.openConnection()
        dbCursor = av3arDB_CNX.cursor()
        dbCursor.callproc("get_emp_atten_all_dates", arg_db)
        training_json = dbCursor.stored_results()
        # cache.__setattr__(model_table_key, str(result))
        return training_json
    except Exception as e:
        exc is not None and exc.exception("Error while fetching the all attendance details from DB")
        return False
    finally:
        DataAccess.closeConnection()


def get_emp_details_id(arg_db):
    """
    This function will fetch the employee attendance report for the sepecific user between the dates from the database
    :param arg_db: list of arguments for the query
    :return: employee attendance data
    """
    try:
        av3arDB_CNX = DataAccess.openConnection()
        dbCursor = av3arDB_CNX.cursor()
        dbCursor.callproc("get_emp_atten_id_dates", arg_db)
        training_json = dbCursor.stored_results()
        # cache.__setattr__(model_table_key, str(result))
        return training_json
    except Exception as e:
        exc is not None and exc.exception("Error while fetching the specefic employee details by dates")
        return False
    finally:
        DataAccess.closeConnection()


def insert_emp_details(arg_db_list):
    """
    This function will add the new employee details into the database
    :param arg_db_list: list of arguments for the query
    :return: boolean success message
    """
    try:
        av3arDB_CNX = DataAccess.openConnection()
        dbCursor = av3arDB_CNX.cursor()
        dbCursor.callproc("emp_details_insert", arg_db_list)
        av3arDB_CNX.commit()
        return True
    except Exception as e:
        exc is not None and exc.exception("Error while inserting the employee details into DB")
        return False
    finally:
        DataAccess.closeConnection()

