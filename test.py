from flask import Flask, jsonify
import pyodbc

app = Flask(__name__)

# Create a database connection
conn_str = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\SafesmartBusinessEn\Database\Property2.mdb;"
    r"PWD=AnsonSTMake811;"
)

connection = pyodbc.connect(conn_str)
cursor = connection.cursor()


# Create a route to retrieve event records with employee details in JSON format
@app.route("/eventRecord")
def get_eventRecord():
    # Retrieve event records and employee details using SQL JOIN
    cursor.execute(
        """
        SELECT E.EmployeeID, E.EmployeeName, E.Code, E.DepartmentID, A.AriseTime, A.EventType
        FROM Employee E
        INNER JOIN EventRecord A ON E.EmployeeID = A.EmployeeID
    """
    )
    rows = cursor.fetchall()

    # Create a list of dictionaries for the combined data
    eventRecord = []
    for row in rows:
        data = {
            "EmployeeID": row.EmployeeID,
            "EmployeeName": row.EmployeeName,
            "Code": row.Code,
            "DepartmentID": row.DepartmentID,
            "Date": str(row.AriseTime.date()),  # Date as a string
            "Time": str(row.AriseTime.time()),  # Time as a string
            "EventType": row.EventType,
        }
        eventRecord.append(data)

    return jsonify(eventRecord)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
