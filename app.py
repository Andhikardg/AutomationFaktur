from logging import PlaceHolder
import streamlit as st
import pandas as pd
from fpdf import FPDF
from num2words import num2words
from datetime import datetime

st.set_page_config(page_title="Pembuatan Faktur Githa Persada Tehnik", layout="wide")

def draw_header(pdf):
    pdf.set_font('Times', 'B', 20)
    pdf.cell(0, 8, 'GITHA PERSADA TEHNIK', 0, 1, 'C')
    
    pdf.set_font('Times', 'B', 11)
    pdf.cell(0, 5, 'Rubber Industri, Baklit, Plastik, Logam. Suplier dan Perdagangan Umum', 0, 1, 'C')
    
    pdf.set_font('Times', '', 10)
    pdf.cell(0, 5, 'Komp. Puspa Regency Blok B 76 Batujajar Bandung 40561', 0, 1, 'C')
    pdf.cell(0, 5, 'Telp. 022-92214220, 86861444, Fax. 6868463', 0, 1, 'C')
    pdf.cell(0, 5, 'Hp. 08122054444', 0, 1, 'C')
    
    pdf.ln(2)
    x_start = pdf.get_x()
    y_start = pdf.get_y()
    pdf.set_line_width(0.5)
    pdf.line(x_start, y_start, 200, y_start) 
    pdf.set_line_width(0.2)
    pdf.line(x_start, y_start + 1, 200, y_start + 1) 
    pdf.ln(8)

def create_invoice_pdf(invoice_no, date, customer_name, customer_addr, items, grand_total):
    class PDF(FPDF):
        def header(self):
            draw_header(self)

    pdf = PDF()
    pdf.set_margins(15, 15, 15)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Times", "B", 11)
    start_y = pdf.get_y()
    
    pdf.cell(30, 6, "FAKTUR No.", 0, 0); pdf.cell(5, 6, ":", 0, 0)
    pdf.set_font("Times", "", 11); pdf.cell(60, 6, invoice_no, 0, 1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(30, 6, "D/O.No.", 0, 0); pdf.cell(5, 6, ":", 0, 0)
    pdf.set_font("Times", "", 11); pdf.cell(60, 6, ".......................", 0, 1)

    pdf.set_xy(120, start_y)
    pdf.set_font("Times", "B", 11)
    pdf.cell(30, 6, "TANGGAL", 0, 0); pdf.cell(5, 6, ":", 0, 0)
    pdf.set_font("Times", "", 11); pdf.cell(0, 6, f"Bandung, {date.strftime('%d %b %y')}", 0, 1)
    
    pdf.set_xy(120, pdf.get_y())
    pdf.set_font("Times", "B", 11)
    pdf.cell(30, 6, "KEPADA YTH.", 0, 0); pdf.cell(5, 6, ":", 0, 0)
    pdf.set_font("Times", "B", 11); pdf.cell(0, 6, customer_name, 0, 1)
    pdf.set_xy(155, pdf.get_y()); pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, customer_addr)
    pdf.ln(10)

    pdf.set_font("Times", "B", 11)
    pdf.cell(30, 8, "BANYAKNYA", 1, 0, 'C')
    pdf.cell(85, 8, "NAMA BARANG", 1, 0, 'C')
    pdf.cell(35, 8, "HARGA", 1, 0, 'C')
    pdf.cell(35, 8, "JUMLAH", 1, 1, 'C')

    pdf.set_font("Times", "", 11)
    for _, row in items.iterrows():
        qty = int(row['Banyaknya'])
        nama = str(row['Nama Barang'])
        harga = int(row['Harga Satuan'])
        total = qty * harga
        
        x_start = pdf.get_x()
        y_start = pdf.get_y()

        pdf.set_xy(x_start + 30, y_start)
        pdf.multi_cell(85, 8, nama, border='LTR', align='L')
        
        y_end = pdf.get_y()
        row_height = y_end - y_start

        pdf.set_xy(x_start, y_start)
        pdf.cell(30, row_height, str(qty), border='LTR', align='C') # Qty
        
        pdf.set_xy(x_start + 30 + 85, y_start)
        pdf.cell(35, row_height, f"Rp. {harga:,.0f},-", border='LTR', align='R') # Harga
        
        pdf.set_xy(x_start + 30 + 85 + 35, y_start)
        pdf.cell(35, row_height, f"Rp. {total:,.0f},-", border='LTR', align='R') # Jumlah

        pdf.set_xy(x_start, y_end)

    pdf.cell(185, 0, '', 'T', 1) 
    
    # Total
    pdf.ln(1)
    pdf.set_font("Times", "B", 12)
    pdf.cell(150, 10, "TOTAL RP.", 0, 0, 'R')
    pdf.cell(35, 10, f"Rp. {grand_total:,.0f},-", 1, 1, 'R')
    
    pdf.ln(5)
    terbilang_text = num2words(grand_total, lang='id').title() + " Rupiah"
    pdf.set_font("Times", "", 11)
    pdf.multi_cell(0, 6, f"Terbilang: {terbilang_text}", 0, 'L')

    pdf.ln(15)
    pdf.set_xy(120, pdf.get_y())
    pdf.set_font("Times", "B", 11)
    pdf.cell(60, 5, "GITHA PERSADA TEHNIK", 0, 1, 'C')
    pdf.ln(25)
    pdf.set_xy(120, pdf.get_y())
    pdf.cell(60, 5, "( .................................... )", 0, 0, 'C')

    return pdf.output(dest='S').encode('latin-1')

def create_offer_pdf(date, customer_name, opening_context, items, signer_name):
    class PDF(FPDF):
        def header(self):
            draw_header(self)

    pdf = PDF()
    pdf.set_margins(20, 15, 20)
    pdf.add_page()
    
    pdf.set_font("Times", "", 11)
    pdf.cell(0, 6, "Kepada Yth.", 0, 1)
    pdf.set_font("Times", "B", 11)
    pdf.cell(0, 6, customer_name, 0, 1)
    pdf.set_font("Times", "", 11)
    pdf.cell(0, 6, "di Tempat.", 0, 1)
    pdf.ln(8)
    
    pdf.cell(0, 6, "Dengan hormat,", 0, 1)
    pdf.multi_cell(0, 6, f"Sehubungan dengan permintaan {customer_name} mengenai {opening_context}, bersama ini kami ajukan penawaran harga sebagai berikut:")
    pdf.ln(5)
    
    pdf.set_font("Times", "B", 11)
    # Definisi Lebar Kolom
    w_no = 15
    w_nama = 100
    w_harga = 55
    
    pdf.cell(w_no, 8, "No", 1, 0, 'C')
    pdf.cell(w_nama, 8, "Nama Barang", 1, 0, 'C')
    pdf.cell(w_harga, 8, "Harga", 1, 1, 'C')
    
    pdf.set_font("Times", "", 11)
    no = 1
    for _, row in items.iterrows():
        nama = str(row['Nama Barang'])
        
        raw_harga = row['Harga / Satuan']
        try:
            harga = f"Rp. {float(raw_harga):,.0f}"
        except:
            harga = str(raw_harga)
        
        x_start = pdf.get_x()
        y_start = pdf.get_y()
        
        pdf.set_xy(x_start + w_no, y_start) 
        pdf.multi_cell(w_nama, 8, nama, border=1, align='L')
        
        y_end = pdf.get_y()
        
        row_height = y_end - y_start
        
        pdf.set_xy(x_start, y_start)
        pdf.cell(w_no, row_height, str(no), border=1, align='C')

        pdf.set_xy(x_start + w_no + w_nama, y_start)
        pdf.cell(w_harga, row_height, harga, border=1, align='L')
        
        pdf.set_xy(x_start, y_end)
        
        no += 1

    pdf.ln(5)
    
    pdf.multi_cell(0, 6, "Demikian surat penawaran ini kami ajukan, atas perhatian dan kerja samanya kami ucapkan terimakasih.")
    pdf.ln(10)
    
    pdf.cell(0, 6, f"Bandung, {date.strftime('%d %b %y')}", 0, 1)
    pdf.cell(0, 6, "Hormat Kami,", 0, 1)
    
    pdf.ln(25) 
    
    pdf.set_font("Times", "B", 11)
    width_name = pdf.get_string_width(signer_name)
    pdf.cell(width_name, 6, signer_name, 0, 1, 'L')
    
    x_line = pdf.get_x()
    y_line = pdf.get_y()
    pdf.line(20, y_line, 20 + width_name + 5, y_line)

    return pdf.output(dest='S').encode('latin-1')

st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Menu:", ["📝 Buat Faktur", "📩 Buat Surat Penawaran"])

st.title("Pembuatan Surat Penawaran Githa Persada Tehnik")
st.markdown("---")

if menu == "📝 Buat Faktur":
    st.header("Buat Faktur Penjualan")
    
    if 'data_faktur' not in st.session_state:
            st.session_state['data_faktur'] = pd.DataFrame(columns=["Banyaknya", "Nama Barang", "Harga Satuan"])

    with st.sidebar:
        st.markdown("---")
        st.subheader("Info Faktur")
        no_faktur = st.text_input("No. Faktur", placeholder="Contoh: 295/GPT/XII/25")
        tgl_faktur = st.date_input("Tanggal Faktur", datetime.now())
        cust_name = st.text_input("Nama Customer (PT)")
        cust_addr = st.text_area("Alamat Customer")

    col_config = {
        "Banyaknya": st.column_config.NumberColumn("Qty", min_value=1),
        "Nama Barang": st.column_config.TextColumn("Nama Barang", width="large"),
        "Harga Satuan": st.column_config.NumberColumn("Harga (Rp)", format="Rp %d"),
    }
    
    df_faktur = st.data_editor(st.session_state['data_faktur'], column_config=col_config, num_rows="dynamic", use_container_width=True, hide_index=True)

    if not df_faktur.empty:
        total = (df_faktur["Banyaknya"] * df_faktur["Harga Satuan"]).sum()
        st.markdown(f"<h3 style='text-align:right'>Total: Rp {total:,.0f}</h3>", unsafe_allow_html=True)
        
        if st.button("🖨️ Download PDF Faktur", type="primary"):
            if cust_name:
                pdf_bytes = create_invoice_pdf(no_faktur, tgl_faktur, cust_name, cust_addr, df_faktur, total)
                st.download_button("⬇️ Klik Disini", pdf_bytes, f"Faktur_{cust_name}.pdf", "application/pdf")
            else:
                st.error("Isi Nama Customer dulu di sidebar!")

elif menu == "📩 Buat Surat Penawaran":
    st.header("Buat Surat Penawaran Harga")
    
    if 'data_offer' not in st.session_state:
            st.session_state['data_offer'] = pd.DataFrame(columns=["Nama Barang", "Harga / Satuan"])

    col_input1, col_input2 = st.columns(2)
    with col_input1:
        offer_cust = st.text_input("Kepada Yth (Nama PT)", placeholder="Contoh: PT. Indorama")
        offer_context = st.text_input("Mengenai (Context)", placeholder="Contoh: Suku cadang mesin")
    with col_input2:
        offer_date = st.date_input("Tanggal Surat", datetime.now())
        signer_name = st.text_input("Penandatangan", placeholder="Contoh:Dadan S.")

    st.subheader("Item Penawaran")
    
    col_config_offer = {
            "Nama Barang": st.column_config.TextColumn("Nama Barang", width="large", required=True),
            "Harga / Satuan": st.column_config.NumberColumn(
                "Harga (Rp)", 
                width="medium", 
                required=True,
                format="Rp %d", 
                min_value=0
            ),
        }
    
    df_offer = st.data_editor(st.session_state['data_offer'], column_config=col_config_offer, num_rows="dynamic", use_container_width=True, hide_index=True)

    st.markdown("---")
    if st.button("🖨️ Download Surat Penawaran", type="primary"):
        if offer_cust:
            pdf_bytes = create_offer_pdf(offer_date, offer_cust, offer_context, df_offer, signer_name)
            st.download_button("⬇️ Klik Disini", pdf_bytes, f"Penawaran_{offer_cust}.pdf", "application/pdf")
        else:
            st.error("Mohon isi 'Kepada Yth' terlebih dahulu.")
