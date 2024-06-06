// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

// render
frappe.listview_settings['Sale Invoice'] = {
	get_indicator: function(doc) {
		const status_colors = {
			"Draft": "grey",
			"Unpaid": "orange",
			"Paid": "green",
			"Partly Paid": "yellow",
		};
		return [__(doc.status), status_colors[doc.status], "status,=,"+doc.status];
	}
};
