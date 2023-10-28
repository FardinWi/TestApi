from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# first lets create a database connection
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\SafesmartBusinessEn\Database\Property2.mdb;"
    r"PWD=AnsonSTMake811;"
)

connection = pyodbc.connect(conn_str)
cursor = connection.cursor()


# at first create a route to retrieve event records with employee details in JSON format
@app.route("/eventRecord")
def get_eventRecord():
    try:
        # retrive all the event records with employee details and department details
        cursor.execute(
            """
            SELECT E.EmployeeID, E.EmployeeName, E.Code, E.DepartmentID, A.AriseTime, A.EventType, D.DepartmentName, C.CardLow, CO.CommString, CO.CtrlName, CO.CtrlID
            FROM (((Employee AS E
            INNER JOIN EventRecord AS A ON E.EmployeeID = A.EmployeeID)
            INNER JOIN Department AS D ON E.DepartmentID = D.DepartmentID)
            LEFT JOIN Card AS C ON E.EmployeeID = C.EmployeeID)
            LEFT JOIN Controller AS CO ON A.CtrlID = CO.CtrlID
            """
        )

        event_rows = cursor.fetchall()

        # Create a dictionary to store employee data
        employees = {}
        for row in event_rows:
            employee_id = row.EmployeeID
            if employee_id not in employees:
                employees[employee_id] = {
                    "EmployeeID": row.EmployeeID,
                    "EmployeeName": row.EmployeeName,
                    "Code": row.Code,
                    "DepartmentID": row.DepartmentID,
                    "DepartmentName": row.DepartmentName,
                    "Events": [],
                }
            employees[employee_id]["Events"].append(
                {
                    "Date": str(row.AriseTime.date()),
                    "Time": str(row.AriseTime.time()),
                    "EventType": row.EventType,
                    "CardLow": row.CardLow,
                    "CtrlID": row.CtrlID,
                    "CommString": row.CommString,
                    "CtrlName": row.CtrlName,
                }
            )

        # now convert the dictionary into a list
        employee_list = list(employees.values())

        return jsonify(employee_list)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
