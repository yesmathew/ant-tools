// Copyright (c) 2024, Anther and contributors
// For license information, please see license.txt




frappe.ui.form.on('Ant tool setting', {
    refresh: function(frm) {
        frm.fields_dict['beep_file'].get_query = function(doc, cdt, cdn) {
            return {
                filters: [
                    ['File', 'file_type', '=', 'MP3']  
                ]
            };
        };
    }
});
