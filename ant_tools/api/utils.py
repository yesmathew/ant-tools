import frappe
import barcode
from barcode.writer import SVGWriter
from io import BytesIO
import base64

@frappe.whitelist(allow_guest=True)
def barcode_generator(data):
    '''

        This function will accept a param as data and return an svg data as barcode use a access it throw jinga tag as {{barcode_generator(data)}}

    '''
    try:
        code128 = barcode.get_barcode_class('code128')

        # Create the barcode instance
        barcode_instance = code128(data, writer=SVGWriter())

        # Create an in-memory stream to hold the SVG data
        svg_stream = BytesIO()

        # Write the SVG data to the in-memory stream
        barcode_instance.write(svg_stream)

        # Seek to the beginning of the stream
        svg_stream.seek(0)

        # Read the SVG data from the stream
        svg_data = svg_stream.read().decode('utf-8')

        # Encode the SVG data as base64
        base64_svg_data = base64.b64encode(svg_data.encode('utf-8')).decode('utf-8')

        # Construct the data URI
        data_uri = f'data:image/svg+xml;base64,{base64_svg_data}'
        return data_uri
    except:
        #   Throw a error message 
        frappe.throw("sent a proper param to access the barcode data")

@frappe.whitelist(allow_guest=True)
def length_counter(data):
    '''
        This function will accept a variable ant return the length of it 
    '''
    try:
        return len(data)
    except:
        frappe.throw("something went wrong")