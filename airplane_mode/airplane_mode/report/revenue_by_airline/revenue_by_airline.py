# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from collections import defaultdict

def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	# columns=get_columns()
	# data = get_data()
	# new_data=frappe.get_all("Airplane Ticket", fields=["total_amount", "flight"], group_by="flight")
	# [{'total_amount': 5000.0, 'airplane': 'Air India-002'},
	#  {'total_amount': 4000.0, 'airplane': 'Indigo-004'},
	#  {'total_amount': 780.0, 'airplane': None},
	#  {'total_amount': 84.0, 'airplane': None},
	#  {'total_amount': 0.0, 'airplane': None}]
	# airline_data=frappe.get_all("Airplane", fields=[ "airline"], group_by="airline")
	# [{'name': 'Indigo-004', 'airline': 'Indigo'},
	#  {'name': 'Air India-002', 'airline': 'Air India'}]

	airplanes = frappe.get_all("Airplane", fields=["name", "airline"])
	airplane_map = {a['name']: a['airline'] for a in airplanes}
	tickets = frappe.get_all("Airplane Ticket",filters={"docstatus": 1},fields=["total_amount", "flight.airplane"], order_by="total_amount DESC")



	airline_totals = defaultdict(float)

	for ticket in tickets:
		flight_name = ticket.get("airplane")
		amount = ticket.get("total_amount", 0)
		airline = airplane_map.get(flight_name)
		
		if airline:
			airline_totals[airline] += amount

	#Converting the list of dicts
	result = [{"airline": k, "total_amount": v} for k, v in airline_totals.items()]
	data = [[x["airline"], x["total_amount"]] for x in result]

	# new_data = {	
	# 				{
	# 					name: "Some Data", type: "bar",
	# 					values: [25, 40, 30, 35, 8, 52, 17, -4]
	# 				},
	# 				{
	# 					name: "Another Set", type: "line",
	# 					values: [25, 50, -10, 15, 18, 32, 27, 14]
	# 				}
	# 		}

	chart = {
		"data": {
			"labels": [x["airline"] for x in result],
			"datasets": [{"values": [x["total_amount"] for x in result]}]
		},
		"type": "donut"
	}


	columns = get_columns()
	# data_test=get_columns()
	# print(data_test)
	total_revenue = sum(x["total_amount"] for x in result)
	report_summary = [
    {
        "value": total_revenue,
        "indicator": "Green",
        "label": "Total Revenue",
        "datatype": "Currency",
        "currency": "INR"
    }
]

	return columns,data, "Total Revenue", chart, report_summary

def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airplane"
		},
		{
			"label": _("Revenue"),
			"fieldname": "total_revenue",
			"fieldtype": "Currency",
		},
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	return [
		["Row 1", 1],
		["Row 2", 2],
	]
