import base64
from collections import defaultdict
from io import BytesIO

import barcode
import frappe
from barcode.writer import SVGWriter


@frappe.whitelist(allow_guest=True)
def barcode_generator(data):
        """
        This function will accept a param as data and return an svg data as barcode use a access it throw jinga tag as {{barcode_generator(data)}}
        """
        try:    
                code128 = barcode.get_barcode_class("code128")
                # Create the barcode instance
                barcode_instance = code128(data, writer=SVGWriter())
                # Create an in-memory stream to hold the SVG data
                svg_stream = BytesIO()
                # Write the SVG data to the in-memory stream
                barcode_instance.write(svg_stream)
                # Seek to the beginning of the stream
                svg_stream.seek(0)
                # Read the SVG data from the stream
                svg_data = svg_stream.read().decode("utf-8")
                # Encode the SVG data as base64
                base64_svg_data = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
                # Construct the data URI
                data_uri = f"data:image/svg+xml;base64,{base64_svg_data}"
                return data_uri
        except Exception as e:
                frappe.throw(f"Error generating barcode: {str(e)}")


@frappe.whitelist(allow_guest=True)
def length_counter(data):
       """
       This function will accept a variable ant return the length of it 
       """
       if not isinstance(data, str):
            frappe.throw("The input data must be a string")
       return len(data)

@frappe.whitelist(allow_guest=True)
def item_gst_filter(items):
       grouped_items = defaultdict(
               lambda: {
                       "total_sgst_amount": 0,
                       "total_cgst_amount": 0,
                       "total_igst_amount": 0,
                       "total_qty": 0,
                       "total_taxable_amount": 0,
                       "uom": None,
                       "hsn": None,
                       "igst_rate": None,
                       "cgst_rate": None,
                       "sgst_rate": None,
                       "items": []
               }
       )
       # Group items by gst_hsn_code, igst_rate, cgst_rate, and sgst_rate
       for item in items:
               key = ( item.get("gst_hsn_code"), item.get("igst_rate"), item.get("cgst_rate"), item.get("sgst_rate") )    
               # Add item to the group
               grouped_items[key]["items"].append(item)
               # Safely sum up SGST, CGST, and IGST amounts, treating None as 0
               grouped_items[key]["total_cgst_amount"] += item.get("cgst_amount", 0) or 0
               grouped_items[key]["total_igst_amount"] += item.get("igst_amount", 0) or 0
               grouped_items[key]["sgst_rate"] = item.get("sgst_rate", 0) or 0
               # Sum the quantities and taxable amounts, treating None as 0
               grouped_items[key]["total_qty"] += item.get("qty", 0) or 0
               grouped_items[key]["total_taxable_amount"] += item.get("taxable_value", 0) or 0
               # Set UOM and HSN (use the first item's UOM for each group)
               if grouped_items[key]["uom"] is None:
                       grouped_items[key]["uom"] = item.get("uom")
                       grouped_items[key]["hsn"] = item.get("gst_hsn_code")
                       grouped_items[key]["igst_rate"] = item.get("igst_rate", 0) or 0
                       grouped_items[key]["cgst_rate"] = item.get("cgst_rate", 0) or 0
                       grouped_items[key]["sgst_rate"] = item.get("sgst_rate", 0) or 0
       # Convert defaultdict to a list of dictionaries for easier use in Jinja
       grouped_list = []
       idx = 1
       for group, data in grouped_items.items():
               data["idx"] = idx
               grouped_list.append(data)
               idx += 1
       return grouped_list
