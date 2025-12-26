# Copyright (c) 2025, Sydney and contributors
# For license information, please see license.txt

import frappe
from frappe import _


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

	airlines = frappe.get_all("Airline", pluck=	"name")

	#set 0 as intital revenue for all airline
	airline_totals = {airline: 0 for airline in airlines}
	airplanes = frappe.get_all("Airplane", fields=["name", "airline"])
	airplane_map = {a["name"]: a["airline"] for a in airplanes}

	tickets = frappe.get_all( "Airplane Ticket", filters={"docstatus": 1}, fields=["total_amount", "flight.airplane"])

	for ticket in tickets:
		airplane = ticket.get("airplane")
		airline = airplane_map.get(airplane)
		#some test data is malformed
		if not airline:
			continue

		airline_totals[airline] += ticket.get("total_amount") or 0

	#for displaying table
	data = []
	for airline in airlines:
		data.append([airline, airline_totals[airline]])
		
	columns = get_columns()

	chart = {
	"data": {
		"labels": airlines,
		"datasets": [{
			"values": [airline_totals[a] for a in airlines]
		}]
	},
	"type": "donut"
	}

	total_revenue = sum(airline_totals.values())

	report_summary = [{
		"label": "Total Revenue",
		"value": total_revenue,
		"indicator": "Green",
		"datatype": "Currency",
		"currency": "INR"
	}]

 
	return columns, data, None, chart, report_summary

def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Airline"),
			"fieldname": "airline",
			"fieldtype": "Link",
			"options": "Airline"
		},
		{
			"label": _("Revenue"),
			"fieldname": "total_amount",
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

