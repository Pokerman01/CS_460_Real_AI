import json
import os
from io import BytesIO

import google.generativeai as genai
import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

from database import (
    delete_all_receipts,
    delete_receipt,
    get_receipts_for_user,
    init_db,
    insert_receipt,
)


load_dotenv()
init_db()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

LANGUAGE_OPTIONS = ["English", "ไทย"]

CATEGORY_OPTIONS = [
    "Food & Beverages",
    "Travel",
    "Office Supplies",
    "Utilities",
    "Software",
    "Equipment",
    "Other",
]
TAX_OPTIONS = ["Deductible", "Non-Deductible", "Review Needed"]
STATUS_OPTIONS = ["Verified", "Needs Review", "Rejected"]

CATEGORY_LABELS = {
    "English": {
        "Food & Beverages": "Food & Beverages",
        "Travel": "Travel",
        "Office Supplies": "Office Supplies",
        "Utilities": "Utilities",
        "Software": "Software",
        "Equipment": "Equipment",
        "Other": "Other",
        "Uncategorized": "Uncategorized",
    },
    "ไทย": {
        "Food & Beverages": "อาหารและเครื่องดื่ม",
        "Travel": "การเดินทาง",
        "Office Supplies": "อุปกรณ์สำนักงาน",
        "Utilities": "ค่าสาธารณูปโภค",
        "Software": "ซอฟต์แวร์",
        "Equipment": "อุปกรณ์",
        "Other": "อื่น ๆ",
        "Uncategorized": "ไม่ระบุหมวดหมู่",
    },
}

TAX_LABELS = {
    "English": {
        "Deductible": "Deductible",
        "Non-Deductible": "Non-Deductible",
        "Review Needed": "Review Needed",
    },
    "ไทย": {
        "Deductible": "หักเป็นค่าใช้จ่ายได้",
        "Non-Deductible": "หักเป็นค่าใช้จ่ายไม่ได้",
        "Review Needed": "ต้องตรวจสอบ",
    },
}

STATUS_LABELS = {
    "English": {
        "Verified": "Verified",
        "Needs Review": "Needs Review",
        "Rejected": "Rejected",
    },
    "ไทย": {
        "Verified": "ตรวจสอบแล้ว",
        "Needs Review": "ต้องตรวจสอบ",
        "Rejected": "ไม่ผ่าน",
    },
}

TRANSLATIONS = {
    "English": {
        "language_setting": "Language / ภาษา",
        "workspace_caption": "Smart receipt and tax workspace",
        "guest_mode": "Guest mode",
        "signed_in": "Signed in",
        "auth_info": "{auth_mode}: {username}",
        "back_to_landing": "Back to landing",
        "log_out": "Log out",
        "upload_receipt": "Upload receipt",
        "choose_receipt_file": "Choose a receipt image or PDF",
        "analyze_receipt": "Analyze receipt",
        "ready_upload": "Ready for receipt upload",
        "loaded_file": "Loaded: {filename}",
        "hero_title": "Receipt intelligence dashboard",
        "hero_copy": "Scan receipts, verify AI extraction, save clean records, and review tax-ready analytics.",
        "receipt_viewer_title": "Receipt image viewer",
        "receipt_viewer_copy": "Upload a receipt image. JPG and PNG files render directly for verification.",
        "upload_preview_info": "Upload a receipt to preview it here.",
        "pdf_warning": "PDF upload is stored by Streamlit, but this Vision API flow supports JPG/PNG images only.",
        "verification_title": "Verification & correction",
        "verification_copy": "Analyze the uploaded receipt, then review and correct the extracted fields before saving.",
        "guest_save_warning": "Guest mode can analyze receipts, but saving to the database is disabled.",
        "analyze_receipt_main": "Analyze Receipt",
        "upload_before_analyzing": "Please upload a receipt image before analyzing.",
        "jpg_png_warning": "Please upload a JPG, JPEG, or PNG receipt image.",
        "ai_spinner": "AI working: analyzing receipt image and extracting structured fields...",
        "ai_extraction_ready": "AI extraction ready for review. Source: {filename}",
        "saved_to_database": "Receipt #{receipt_id} saved to database.",
        "click_analyze_info": "Click Analyze Receipt to generate editable verification fields.",
        "date": "Date",
        "store_name": "Store Name",
        "items": "Items",
        "category": "Category",
        "total_amount": "Total Amount",
        "vat": "VAT",
        "tax_deductible": "Tax Deductible",
        "status": "Status",
        "save_to_database": "Save to Database",
        "login_again_save": "Please log in again before saving receipts.",
        "receipt_saved_success": "Receipt #{receipt_id} saved successfully.",
        "tax_suggestion_deductible": "**System suggestion: this tax can be deductible.** You can still change the choice below.",
        "tax_suggestion_non_deductible": "**System suggestion: this tax is likely non-deductible.** You can still change the choice below.",
        "tax_suggestion_review": "**System suggestion: this tax needs review.** Please choose the final answer below.",
        "search_filter": "Search & filter",
        "search_store_name": "Search by Store Name",
        "search_placeholder": "Example: Manee Food",
        "filter_category": "Filter by Category",
        "tax_year_dashboard": "Tax year dashboard",
        "total_expenses_all": "Total Expenses (All)",
        "total_tax_deductible": "Total Tax Deductible",
        "total_vat": "Total VAT",
        "expense_breakdown": "Expense breakdown by category",
        "no_chart_data": "No chart data available for the current filters.",
        "export_data": "Export data",
        "no_filtered_export": "No filtered receipts available to export.",
        "download_csv": "Download filtered data as CSV",
        "download_pdf": "Download filtered report as PDF",
        "receipt_history": "Receipt history",
        "no_receipts": "No receipts found for the current filters.",
        "manage_receipts": "Manage receipts",
        "delete_saved_receipts": "Delete saved receipts",
        "guest_delete_warning": "Guest users cannot delete saved receipts. Please register an account.",
        "delete_one": "Delete one",
        "delete_all": "Delete all",
        "delete_caption": "Select one receipt, review it, then confirm deletion. This action cannot be undone.",
        "receipt_to_delete": "Receipt to delete",
        "confirm_delete_receipt": "I understand this will permanently delete this receipt.",
        "delete_selected_receipt": "Delete selected receipt",
        "receipt_deleted": "Receipt #{receipt_id} deleted.",
        "delete_failed": "Could not delete that receipt. It may have already been removed.",
        "delete_all_warning": "This will permanently delete every receipt in your account, not just filtered receipts.",
        "type_delete_all": "Type DELETE ALL to confirm",
        "delete_all_permanently": "Delete all receipts permanently",
        "deleted_count": "Deleted {count} receipt(s).",
        "login_again_history": "Please log in again to view receipt history.",
        "pdf_error": "PDF export requires reportlab. Install it with: pip install reportlab",
        "pdf_title": "Taxara Receipt Export",
        "pdf_receipts_exported": "Receipts exported: {count}",
        "pdf_total_expenses": "Total Expenses: THB {amount}",
        "pdf_total_deductible": "Total Tax Deductible: THB {amount}",
        "pdf_total_vat": "Total VAT: THB {amount}",
        "pdf_col_date": "Date",
        "pdf_col_store": "Store",
        "pdf_col_category": "Category",
        "pdf_col_amount": "Amount",
        "pdf_col_vat": "VAT",
        "pdf_col_tax": "Tax",
        "col_id": "ID",
        "col_date": "Date",
        "col_store_name": "Store Name",
        "col_items": "Items",
        "col_category": "Category",
        "col_total_amount": "Total Amount",
        "col_vat": "VAT",
        "col_tax_deductible": "Tax Deductible",
        "col_status": "Status",
    },
    "ไทย": {
        "language_setting": "ภาษา / Language",
        "workspace_caption": "พื้นที่จัดการใบเสร็จและภาษีอัจฉริยะ",
        "guest_mode": "โหมดผู้เยี่ยมชม",
        "signed_in": "เข้าสู่ระบบแล้ว",
        "auth_info": "{auth_mode}: {username}",
        "back_to_landing": "กลับไปหน้าแรก",
        "log_out": "ออกจากระบบ",
        "upload_receipt": "อัปโหลดใบเสร็จ",
        "choose_receipt_file": "เลือกไฟล์ใบเสร็จรูปภาพหรือ PDF",
        "analyze_receipt": "วิเคราะห์ใบเสร็จ",
        "ready_upload": "พร้อมอัปโหลดใบเสร็จ",
        "loaded_file": "โหลดไฟล์แล้ว: {filename}",
        "hero_title": "แดชบอร์ดวิเคราะห์ใบเสร็จ",
        "hero_copy": "สแกนใบเสร็จ ตรวจสอบข้อมูลจาก AI บันทึกข้อมูล และดูสรุปภาษีได้ในที่เดียว",
        "receipt_viewer_title": "ตัวอย่างรูปใบเสร็จ",
        "receipt_viewer_copy": "อัปโหลดรูปใบเสร็จ ไฟล์ JPG และ PNG จะแสดงตัวอย่างเพื่อให้ตรวจสอบได้",
        "upload_preview_info": "อัปโหลดใบเสร็จเพื่อดูตัวอย่างที่นี่",
        "pdf_warning": "ระบบรับไฟล์ PDF ได้ แต่การวิเคราะห์ด้วย Vision API รองรับเฉพาะ JPG/PNG เท่านั้น",
        "verification_title": "ตรวจสอบและแก้ไขข้อมูล",
        "verification_copy": "วิเคราะห์ใบเสร็จ แล้วตรวจสอบหรือแก้ไขข้อมูลก่อนบันทึก",
        "guest_save_warning": "โหมดผู้เยี่ยมชมสามารถวิเคราะห์ใบเสร็จได้ แต่ไม่สามารถบันทึกลงฐานข้อมูลได้",
        "analyze_receipt_main": "วิเคราะห์ใบเสร็จ",
        "upload_before_analyzing": "กรุณาอัปโหลดรูปใบเสร็จก่อนวิเคราะห์",
        "jpg_png_warning": "กรุณาอัปโหลดไฟล์ JPG, JPEG หรือ PNG",
        "ai_spinner": "AI กำลังวิเคราะห์ใบเสร็จและดึงข้อมูล...",
        "ai_extraction_ready": "AI วิเคราะห์ข้อมูลเสร็จแล้ว โปรดตรวจสอบอีกครั้ง ไฟล์: {filename}",
        "saved_to_database": "บันทึกใบเสร็จ #{receipt_id} ลงฐานข้อมูลแล้ว",
        "click_analyze_info": "กดวิเคราะห์ใบเสร็จเพื่อสร้างข้อมูลที่สามารถแก้ไขได้",
        "date": "วันที่",
        "store_name": "ชื่อร้านค้า",
        "items": "รายการสินค้า",
        "category": "หมวดหมู่",
        "total_amount": "ยอดรวม",
        "vat": "ภาษีมูลค่าเพิ่ม",
        "tax_deductible": "การหักเป็นค่าใช้จ่ายทางภาษี",
        "status": "สถานะ",
        "save_to_database": "บันทึกลงฐานข้อมูล",
        "login_again_save": "กรุณาเข้าสู่ระบบอีกครั้งก่อนบันทึกใบเสร็จ",
        "receipt_saved_success": "บันทึกใบเสร็จ #{receipt_id} สำเร็จ",
        "tax_suggestion_deductible": "**คำแนะนำจากระบบ: รายการนี้น่าจะหักเป็นค่าใช้จ่ายทางภาษีได้** คุณยังสามารถเปลี่ยนคำตอบด้านล่างได้",
        "tax_suggestion_non_deductible": "**คำแนะนำจากระบบ: รายการนี้น่าจะหักเป็นค่าใช้จ่ายทางภาษีไม่ได้** คุณยังสามารถเปลี่ยนคำตอบด้านล่างได้",
        "tax_suggestion_review": "**คำแนะนำจากระบบ: รายการนี้ควรตรวจสอบเพิ่มเติม** โปรดเลือกคำตอบสุดท้ายด้านล่าง",
        "search_filter": "ค้นหาและกรองข้อมูล",
        "search_store_name": "ค้นหาตามชื่อร้านค้า",
        "search_placeholder": "ตัวอย่าง: Manee Food",
        "filter_category": "กรองตามหมวดหมู่",
        "tax_year_dashboard": "แดชบอร์ดภาษีประจำปี",
        "total_expenses_all": "รายจ่ายทั้งหมด",
        "total_tax_deductible": "ยอดที่หักเป็นค่าใช้จ่ายได้",
        "total_vat": "ภาษีมูลค่าเพิ่มรวม",
        "expense_breakdown": "สัดส่วนรายจ่ายตามหมวดหมู่",
        "no_chart_data": "ไม่มีข้อมูลสำหรับแสดงกราฟตามตัวกรองปัจจุบัน",
        "export_data": "ส่งออกข้อมูล",
        "no_filtered_export": "ไม่มีใบเสร็จที่กรองไว้สำหรับส่งออก",
        "download_csv": "ดาวน์โหลดข้อมูลที่กรองเป็น CSV",
        "download_pdf": "ดาวน์โหลดรายงานที่กรองเป็น PDF",
        "receipt_history": "ประวัติใบเสร็จ",
        "no_receipts": "ไม่พบใบเสร็จตามตัวกรองปัจจุบัน",
        "manage_receipts": "จัดการใบเสร็จ",
        "delete_saved_receipts": "ลบใบเสร็จที่บันทึกไว้",
        "guest_delete_warning": "ผู้เยี่ยมชมไม่สามารถลบใบเสร็จที่บันทึกไว้ได้ กรุณาสมัครบัญชีผู้ใช้",
        "delete_one": "ลบทีละรายการ",
        "delete_all": "ลบทั้งหมด",
        "delete_caption": "เลือกใบเสร็จหนึ่งรายการ ตรวจสอบข้อมูล แล้วกดยืนยันการลบ การลบนี้ไม่สามารถย้อนกลับได้",
        "receipt_to_delete": "ใบเสร็จที่ต้องการลบ",
        "confirm_delete_receipt": "ฉันเข้าใจว่าการลบนี้จะลบใบเสร็จอย่างถาวร",
        "delete_selected_receipt": "ลบใบเสร็จที่เลือก",
        "receipt_deleted": "ลบใบเสร็จ #{receipt_id} แล้ว",
        "delete_failed": "ไม่สามารถลบใบเสร็จนี้ได้ อาจถูกลบไปแล้ว",
        "delete_all_warning": "การดำเนินการนี้จะลบใบเสร็จทั้งหมดในบัญชีของคุณ ไม่ใช่เฉพาะรายการที่กรองอยู่",
        "type_delete_all": "พิมพ์ DELETE ALL เพื่อยืนยัน",
        "delete_all_permanently": "ลบใบเสร็จทั้งหมดอย่างถาวร",
        "deleted_count": "ลบใบเสร็จแล้ว {count} รายการ",
        "login_again_history": "กรุณาเข้าสู่ระบบอีกครั้งเพื่อดูประวัติใบเสร็จ",
        "pdf_error": "การส่งออก PDF ต้องใช้ reportlab ติดตั้งด้วยคำสั่ง: pip install reportlab",
        "pdf_title": "รายงานใบเสร็จ Taxara",
        "pdf_receipts_exported": "จำนวนใบเสร็จที่ส่งออก: {count}",
        "pdf_total_expenses": "รายจ่ายทั้งหมด: THB {amount}",
        "pdf_total_deductible": "ยอดที่หักเป็นค่าใช้จ่ายได้: THB {amount}",
        "pdf_total_vat": "ภาษีมูลค่าเพิ่มรวม: THB {amount}",
        "pdf_col_date": "วันที่",
        "pdf_col_store": "ร้านค้า",
        "pdf_col_category": "หมวดหมู่",
        "pdf_col_amount": "ยอดรวม",
        "pdf_col_vat": "VAT",
        "pdf_col_tax": "ภาษี",
        "col_id": "รหัส",
        "col_date": "วันที่",
        "col_store_name": "ชื่อร้านค้า",
        "col_items": "รายการสินค้า",
        "col_category": "หมวดหมู่",
        "col_total_amount": "ยอดรวม",
        "col_vat": "VAT",
        "col_tax_deductible": "การหักภาษี",
        "col_status": "สถานะ",
    },
}


def current_language():
    language = st.session_state.get("language", "English")
    if language not in LANGUAGE_OPTIONS:
        return "English"
    return language


def t(key, **kwargs):
    language = current_language()
    text = TRANSLATIONS.get(language, TRANSLATIONS["English"]).get(
        key,
        TRANSLATIONS["English"].get(key, key),
    )

    if kwargs:
        return text.format(**kwargs)

    return text


def category_label(category):
    return CATEGORY_LABELS.get(current_language(), CATEGORY_LABELS["English"]).get(
        category,
        category,
    )


def tax_label(tax_deductible):
    return TAX_LABELS.get(current_language(), TAX_LABELS["English"]).get(
        tax_deductible,
        tax_deductible,
    )


def status_label(status):
    return STATUS_LABELS.get(current_language(), STATUS_LABELS["English"]).get(
        status,
        status,
    )


def is_guest_user():
    return bool(st.session_state.get("is_guest", False)) or st.session_state.get("auth_mode") == "guest"


def current_user_id():
    return st.session_state.get("user_id")


def logout_user():
    for key in ["is_authenticated", "is_guest", "auth_mode", "user_id", "username"]:
        st.session_state.pop(key, None)

    st.session_state.page = "landing"
    st.query_params.clear()
    st.rerun()


def go_home():
    st.session_state.page = "landing"
    st.query_params.clear()
    st.rerun()


def remove_auth_ripples():
    components.html(
        """
        <script>
          if (window.parent.__taxaraRippleCleanup) {
            window.parent.__taxaraRippleCleanup();
          }

          const canvas = window.parent.document.getElementById("auth-ripple-canvas");
          if (canvas) {
            canvas.remove();
          }
        </script>
        """,
        height=0,
    )


def init_dashboard_state():
    defaults = {
        "language": "English",
        "verification_ready": False,
        "extracted_receipt": None,
        "last_saved_receipt_id": None,
        "active_receipt_upload": None,
        "ai_tax_deductible_suggestion": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def remember_uploaded_file(source_key):
    uploaded = st.session_state.get(source_key)
    if uploaded is not None:
        st.session_state.active_receipt_upload = source_key


def current_uploaded_file():
    active_key = st.session_state.get("active_receipt_upload")
    if active_key:
        return st.session_state.get(active_key)

    return st.session_state.get("sidebar_receipt_upload") or st.session_state.get(
        "main_receipt_upload"
    )


def upload_widget(key, label_visibility="visible"):
    return st.file_uploader(
        t("choose_receipt_file"),
        type=["jpg", "jpeg", "png", "pdf"],
        key=key,
        label_visibility=label_visibility,
        on_change=remember_uploaded_file,
        args=(key,),
    )


def clean_json_text(text):
    cleaned = text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").strip()

    if cleaned.endswith("```"):
        cleaned = cleaned.removesuffix("```").strip()

    return cleaned


def infer_tax_deductible(category, store_name, items):
    text = f"{store_name} {items}".lower()

    personal_keywords = [
        "personal",
        "gift",
        "fine",
        "penalty",
        "movie",
        "cinema",
        "spa",
        "beauty",
        "alcohol",
        "ส่วนตัว",
        "ของขวัญ",
        "ค่าปรับ",
    ]

    business_meeting_keywords = [
        "meeting",
        "client",
        "customer",
        "catering",
        "seminar",
        "conference",
        "training",
        "ประชุม",
        "ลูกค้า",
        "สัมมนา",
        "อบรม",
        "จัดเลี้ยง",
    ]

    if any(keyword in text for keyword in personal_keywords):
        return "Non-Deductible"

    if category in ["Office Supplies", "Software", "Equipment", "Utilities"]:
        return "Deductible"

    if category == "Food & Beverages":
        if any(keyword in text for keyword in business_meeting_keywords):
            return "Review Needed"
        return "Non-Deductible"

    if category == "Travel":
        return "Review Needed"

    return "Review Needed"


def normalize_receipt_data(data):
    category = data.get("category", "Other")
    if category not in CATEGORY_OPTIONS:
        category = "Other"

    store_name = str(data.get("store_name", ""))
    items = str(data.get("items", ""))

    ai_tax_deductible = data.get("tax_deductible", "Review Needed")
    if ai_tax_deductible not in TAX_OPTIONS:
        ai_tax_deductible = "Review Needed"

    rule_tax_deductible = infer_tax_deductible(category, store_name, items)

    if ai_tax_deductible == "Review Needed":
        tax_deductible = rule_tax_deductible
    elif category in ["Office Supplies", "Software", "Equipment", "Utilities"]:
        tax_deductible = "Deductible"
    elif category == "Food & Beverages":
        tax_deductible = rule_tax_deductible
    else:
        tax_deductible = ai_tax_deductible

    status = data.get("status", "Needs Review")
    if status not in STATUS_OPTIONS:
        status = "Needs Review"

    return {
        "date": str(data.get("date", "")),
        "store_name": store_name,
        "items": items,
        "category": category,
        "total_amount": float(data.get("total_amount", 0) or 0),
        "vat": float(data.get("vat", 0) or 0),
        "tax_deductible": tax_deductible,
        "status": status,
    }


def is_image_file(uploaded_file):
    if uploaded_file is None:
        return False

    return uploaded_file.name.lower().endswith((".jpg", ".jpeg", ".png"))


def analyze_receipt_image(uploaded_file):
    if uploaded_file is None:
        raise ValueError("No receipt image was uploaded.")

    if not is_image_file(uploaded_file):
        raise ValueError("Only JPG, JPEG, and PNG receipt images can be analyzed.")

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing. Add it to your .env file.")

    genai.configure(api_key=GEMINI_API_KEY)

    uploaded_file.seek(0)
    image_bytes = uploaded_file.read()

    prompt = """
Analyze this Thai receipt. Extract the following fields and return ONLY a valid JSON object:
- "date": string (format YYYY-MM-DD)
- "store_name": string
- "items": string (summarize all items)
- "category": string (choose from: Food & Beverages, Travel, Office Supplies, Utilities, Software, Equipment, Other)
- "total_amount": float
- "vat": float
- "tax_deductible": string (choose from: Deductible, Non-Deductible, Review Needed)
- "status": string (always "Needs Review")

Rules for "tax_deductible":
Evaluate conservatively for a Thai SME/freelancer business expense.

Return "Deductible" when the receipt clearly appears business-related and the category is:
- Office Supplies
- Software
- Equipment
- Utilities

Return "Non-Deductible" when:
- the receipt appears personal
- the expense is clearly unrelated to business
- the receipt is a personal gift, personal meal, fine, penalty, or non-business purchase
- Food & Beverages appears to be a normal personal meal

Return "Review Needed" when:
- Food & Beverages appears related to a business meeting, client meeting, catering, seminar, or event
- the receipt is Travel, transport, hotel, fuel, or vehicle-related
- the receipt does not clearly show whether it was for business or personal use
- VAT claimability is unclear

Important:
- A full Tax Invoice / ใบกำกับภาษี affects VAT claim evidence, but do not mark normal business categories as Review Needed only because the receipt is not a full tax invoice.
- Do not give tax/legal advice.
- If uncertain, choose "Review Needed".
- Return only valid JSON.
- Do not include markdown formatting, code fences, or explanatory text.
"""

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            [
                prompt,
                {
                    "mime_type": uploaded_file.type or "image/jpeg",
                    "data": image_bytes,
                },
            ]
        )

        parsed_json = json.loads(clean_json_text(response.text))
        return normalize_receipt_data(parsed_json)

    except json.JSONDecodeError as exc:
        raise RuntimeError("Gemini response was not valid JSON. Please try again.") from exc
    except Exception as exc:
        raise RuntimeError(f"Gemini API request failed: {exc}") from exc


def load_verification_state(data):
    st.session_state.extracted_receipt = data
    st.session_state.verification_ready = True

    st.session_state.verify_date = data["date"]
    st.session_state.verify_store_name = data["store_name"]
    st.session_state.verify_items = data["items"]
    st.session_state.verify_category = data["category"]
    st.session_state.verify_total_amount = float(data["total_amount"])
    st.session_state.verify_vat = float(data["vat"])
    st.session_state.verify_tax_deductible = data["tax_deductible"]
    st.session_state.verify_status = data["status"]
    st.session_state.ai_tax_deductible_suggestion = data["tax_deductible"]


def show_tax_deductible_suggestion(tax_deductible):
    if tax_deductible == "Deductible":
        st.success(t("tax_suggestion_deductible"))
    elif tax_deductible == "Non-Deductible":
        st.warning(t("tax_suggestion_non_deductible"))
    else:
        st.info(t("tax_suggestion_review"))


def render_styles():
    st.markdown(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;700&family=Syne:wght@600;700;800&family=Inter:wght@400;500;600&family=Noto+Sans+Thai:wght@300;400;500;600;700;800&display=swap');

          #MainMenu, header, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {
            display: none !important;
          }

          .stApp {
            background:
              radial-gradient(circle at 24% 8%, rgba(124,58,237,0.28), transparent 32%),
              radial-gradient(circle at 86% 20%, rgba(59,130,246,0.18), transparent 30%),
              linear-gradient(180deg, #030305 0%, #080810 42%, #050509 100%) !important;
            color: #f4f4f5 !important;
            font-family: 'Noto Sans Thai', 'DM Sans', sans-serif;
          }

          .stApp::before {
            content: "";
            position: fixed;
            inset: 0;
            pointer-events: none;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.72' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='1'/%3E%3C/svg%3E");
            opacity: 0.035;
            z-index: 0;
          }

          [data-testid="stMainBlockContainer"] {
            max-width: 1220px !important;
            padding: 36px 46px 52px !important;
          }

          section[data-testid="stSidebar"] {
            display: block !important;
            visibility: visible !important;
            background: rgba(3,3,5,0.92) !important;
            border-right: 1px solid rgba(139,92,246,0.18) !important;
          }

          [data-testid="stSidebarCollapsedControl"] {
            display: flex !important;
            visibility: visible !important;
          }

          section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding-top: 28px;
          }

          h1, h2, h3 {
            font-family: 'Noto Sans Thai', 'Syne', sans-serif !important;
            letter-spacing: 0 !important;
          }

          h1 {
            font-size: clamp(2.4rem, 5vw, 4.6rem) !important;
            line-height: 1.08 !important;
            margin: 0 !important;
            background: linear-gradient(160deg, #ffffff 0%, #e0e7ff 32%, #c4b5fd 68%, #93c5fd 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
          }

          .stButton > button,
          .stDownloadButton > button {
            min-height: 44px;
            border-radius: 999px !important;
            border: 1px solid rgba(139,92,246,0.38) !important;
            background: rgba(139,92,246,0.12) !important;
            color: #e9d5ff !important;
            font-weight: 600 !important;
          }

          .stButton > button:hover,
          .stDownloadButton > button:hover {
            background: rgba(139,92,246,0.2) !important;
            color: #ffffff !important;
          }

          .stButton > button[kind="primary"] {
            border: none !important;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 52%, #3b82f6 100%) !important;
            color: #ffffff !important;
            box-shadow: 0 16px 42px rgba(79,70,229,0.34) !important;
          }

          .stFileUploader [data-testid="stFileUploaderDropzone"] {
            background: rgba(255,255,255,0.035) !important;
            border: 1px dashed rgba(167,139,250,0.46) !important;
            border-radius: 18px !important;
            min-height: 132px;
          }

          [data-testid="stMetric"] {
            padding: 18px;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.035);
          }

          .hero-panel,
          .panel,
          .step-card {
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.08);
            background: rgba(255,255,255,0.04);
          }

          .hero-panel {
            padding: clamp(28px, 5vw, 46px);
            margin-bottom: 28px;
            background:
              linear-gradient(135deg, rgba(255,255,255,0.072), rgba(255,255,255,0.026)),
              radial-gradient(circle at 82% 12%, rgba(124,58,237,0.34), transparent 36%);
          }

          .eyebrow {
            display: inline-flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 22px;
            padding: 7px 14px;
            border-radius: 999px;
            border: 1px solid rgba(139,92,246,0.36);
            background: rgba(139,92,246,0.12);
            color: #c4b5fd;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
          }

          .eyebrow-dot {
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: #7c3aed;
            box-shadow: 0 0 10px #7c3aed;
          }

          .hero-copy,
          .panel-copy,
          .step-card p {
            color: rgba(203,213,225,0.72);
            line-height: 1.6;
          }

          .panel {
            padding: 24px;
            margin: 10px 0 26px;
          }

          .panel-title,
          .section-title {
            font-family: 'Noto Sans Thai', 'Syne', sans-serif;
            font-weight: 700;
            color: #f8fafc;
          }

          div[data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.08);
          }

          @media (max-width: 760px) {
            [data-testid="stMainBlockContainer"] {
              padding: 24px 18px 40px !important;
            }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar():
    st.markdown("### Taxara")
    st.caption(t("workspace_caption"))

    language_index = LANGUAGE_OPTIONS.index(current_language())
    st.selectbox(
        t("language_setting"),
        LANGUAGE_OPTIONS,
        index=language_index,
        key="language",
    )

    username = st.session_state.get("username", "Guest")
    auth_mode = t("guest_mode") if is_guest_user() else t("signed_in")
    st.info(t("auth_info", auth_mode=auth_mode, username=username))

    st.button(t("back_to_landing"), on_click=go_home, use_container_width=True)
    st.button(t("log_out"), on_click=logout_user, use_container_width=True)
    st.divider()

    st.markdown(f"**{t('upload_receipt')}**")
    upload_widget("sidebar_receipt_upload", label_visibility="collapsed")

    analyze_btn = st.button(
        t("analyze_receipt"),
        type="primary",
        use_container_width=True,
        key="sidebar_analyze",
    )

    return analyze_btn


def render_top_nav():
    _, back_col = st.columns([0.78, 0.22])
    with back_col:
        st.button(t("back_to_landing"), on_click=go_home, use_container_width=True)


def render_hero(uploaded_file):
    upload_status = t("ready_upload")
    if uploaded_file is not None:
        upload_status = t("loaded_file", filename=uploaded_file.name)

    st.markdown(
        f"""
        <div class="hero-panel">
          <div class="eyebrow"><span class="eyebrow-dot"></span>{upload_status}</div>
          <h1>{t("hero_title")}</h1>
          <p class="hero-copy">
            {t("hero_copy")}
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_receipt_viewer():
    st.markdown(
        f"""
        <div class="panel-title">{t("receipt_viewer_title")}</div>
        <p class="panel-copy">
          {t("receipt_viewer_copy")}
        </p>
        """,
        unsafe_allow_html=True,
    )

    upload_widget("main_receipt_upload")
    uploaded_file = current_uploaded_file()

    if uploaded_file is None:
        st.info(t("upload_preview_info"))
    elif is_image_file(uploaded_file):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
    else:
        st.warning(t("pdf_warning"))

    return uploaded_file


def render_verification_panel(uploaded_file, sidebar_analyze_clicked):
    st.markdown(
        f"""
        <div class="panel-title">{t("verification_title")}</div>
        <p class="panel-copy">
          {t("verification_copy")}
        </p>
        """,
        unsafe_allow_html=True,
    )

    if is_guest_user():
        st.warning(t("guest_save_warning"))

    analyze_clicked = st.button(
        t("analyze_receipt_main"),
        type="primary",
        use_container_width=True,
        key="main_analyze_receipt",
    )

    if analyze_clicked or sidebar_analyze_clicked:
        if uploaded_file is None:
            st.warning(t("upload_before_analyzing"))
            return

        if not is_image_file(uploaded_file):
            st.warning(t("jpg_png_warning"))
            return

        with st.spinner(t("ai_spinner")):
            try:
                extracted_data = analyze_receipt_image(uploaded_file)
                load_verification_state(extracted_data)
                st.success(t("ai_extraction_ready", filename=uploaded_file.name))
            except Exception as exc:
                st.error(str(exc))
                return

    if st.session_state.get("last_saved_receipt_id"):
        st.success(t("saved_to_database", receipt_id=st.session_state.last_saved_receipt_id))

    if not st.session_state.verification_ready:
        st.info(t("click_analyze_info"))
        return

    with st.form("receipt_verification_form"):
        verified_date = st.text_input(t("date"), key="verify_date")
        verified_store_name = st.text_input(t("store_name"), key="verify_store_name")
        verified_items = st.text_input(t("items"), key="verify_items")

        verified_category = st.selectbox(
            t("category"),
            CATEGORY_OPTIONS,
            key="verify_category",
            format_func=category_label,
        )

        verified_total_amount = st.number_input(
            t("total_amount"),
            min_value=0.0,
            step=1.0,
            format="%.2f",
            key="verify_total_amount",
        )

        verified_vat = st.number_input(
            t("vat"),
            min_value=0.0,
            step=1.0,
            format="%.2f",
            key="verify_vat",
        )

        ai_suggestion = st.session_state.get(
            "ai_tax_deductible_suggestion",
            st.session_state.get("verify_tax_deductible", "Review Needed"),
        )
        show_tax_deductible_suggestion(ai_suggestion)

        verified_tax_deductible = st.selectbox(
            t("tax_deductible"),
            TAX_OPTIONS,
            key="verify_tax_deductible",
            format_func=tax_label,
        )

        verified_status = st.selectbox(
            t("status"),
            STATUS_OPTIONS,
            key="verify_status",
            format_func=status_label,
        )

        submitted = st.form_submit_button(t("save_to_database"), type="primary")

    if submitted:
        if is_guest_user():
            st.warning(t("guest_save_warning"))
            return

        user_id = current_user_id()
        if user_id is None:
            st.error(t("login_again_save"))
            return

        receipt_id = insert_receipt(
            user_id=user_id,
            date=verified_date,
            store_name=verified_store_name,
            items=verified_items,
            category=verified_category,
            total_amount=verified_total_amount,
            vat=verified_vat,
            tax_deductible=verified_tax_deductible,
            status=verified_status,
        )

        st.session_state.last_saved_receipt_id = receipt_id
        st.session_state.verification_ready = False
        st.session_state.extracted_receipt = None
        st.session_state.ai_tax_deductible_suggestion = None
        st.success(t("receipt_saved_success", receipt_id=receipt_id))


def apply_history_filters(df, search_query, selected_categories):
    filtered_df = df.copy()

    if search_query:
        filtered_df = filtered_df[
            filtered_df["store_name"].fillna("").str.contains(search_query, case=False, na=False)
        ]

    if selected_categories:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

    return filtered_df


def render_analytics_metrics(filtered_df):
    total_expenses = filtered_df["total_amount"].sum() if not filtered_df.empty else 0.0
    total_vat = filtered_df["vat"].sum() if not filtered_df.empty else 0.0

    if filtered_df.empty:
        total_deductible = 0.0
    else:
        deductible_mask = (
            filtered_df["tax_deductible"]
            .fillna("")
            .astype(str)
            .str.lower()
            .eq("deductible")
        )
        total_deductible = filtered_df.loc[deductible_mask, "total_amount"].sum()

    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric(t("total_expenses_all"), f"THB {total_expenses:,.2f}")
    metric_2.metric(t("total_tax_deductible"), f"THB {total_deductible:,.2f}")
    metric_3.metric(t("total_vat"), f"THB {total_vat:,.2f}")


def format_history_dataframe(df):
    if df.empty:
        return df

    display_df = df[
        [
            "id",
            "date",
            "store_name",
            "items",
            "category",
            "total_amount",
            "vat",
            "tax_deductible",
            "status",
        ]
    ].copy()

    display_df["category"] = display_df["category"].fillna("Uncategorized").apply(category_label)
    display_df["tax_deductible"] = display_df["tax_deductible"].fillna("Review Needed").apply(tax_label)
    display_df["status"] = display_df["status"].fillna("Needs Review").apply(status_label)

    return display_df.rename(
        columns={
            "id": t("col_id"),
            "date": t("col_date"),
            "store_name": t("col_store_name"),
            "items": t("col_items"),
            "category": t("col_category"),
            "total_amount": t("col_total_amount"),
            "vat": t("col_vat"),
            "tax_deductible": t("col_tax_deductible"),
            "status": t("col_status"),
        }
    )


def render_category_chart(filtered_df):
    if filtered_df.empty:
        st.info(t("no_chart_data"))
        return

    chart_df = filtered_df.copy()
    chart_df["category"] = chart_df["category"].fillna("Uncategorized")
    chart_df["category_label"] = chart_df["category"].apply(category_label)

    category_totals = (
        chart_df.groupby("category_label", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
    )

    fig = px.pie(
        category_totals,
        names="category_label",
        values="total_amount",
        hole=0.42,
        color_discrete_sequence=["#7c3aed", "#3b82f6", "#10b981", "#f59e0b", "#ef4444"],
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff",
        margin=dict(t=24, r=24, b=24, l=24),
        legend=dict(font=dict(color="#cbd5e1")),
    )

    fig.update_traces(
        textfont_color="#ffffff",
        marker=dict(line=dict(color="#09090b", width=2)),
    )

    st.plotly_chart(fig, use_container_width=True)


def render_delete_controls(filtered_receipts):
    if filtered_receipts.empty:
        return

    st.markdown(f'<div class="section-title">{t("manage_receipts")}</div>', unsafe_allow_html=True)

    with st.expander(t("delete_saved_receipts"), expanded=False):
        if is_guest_user():
            st.warning(t("guest_delete_warning"))
            return

        single_tab, all_tab = st.tabs([t("delete_one"), t("delete_all")])

        with single_tab:
            st.caption(t("delete_caption"))

            delete_options = {}
            for row in filtered_receipts.itertuples(index=False):
                amount = float(getattr(row, "total_amount", 0) or 0)
                label = f"{row.store_name} - {row.date} - THB {amount:,.2f}"
                delete_options[label] = int(row.id)

            selected_label = st.selectbox(
                t("receipt_to_delete"),
                options=list(delete_options.keys()),
                key="delete_receipt_selection",
            )

            selected_id = delete_options[selected_label]
            selected_row = filtered_receipts[filtered_receipts["id"] == selected_id]

            if not selected_row.empty:
                row = selected_row.iloc[0]

                preview_1, preview_2, preview_3 = st.columns(3)
                preview_1.metric(t("store_name"), row["store_name"])
                preview_2.metric(t("date"), row["date"])
                preview_3.metric(t("total_amount"), f"THB {float(row['total_amount']):,.2f}")
                st.info(
                    f"{t('category')}: {category_label(row['category'])} | "
                    f"{t('status')}: {status_label(row['status'])}"
                )

            confirm_delete = st.checkbox(
                t("confirm_delete_receipt"),
                key="confirm_delete_receipt",
            )

            delete_clicked = st.button(
                t("delete_selected_receipt"),
                disabled=not confirm_delete,
                use_container_width=True,
                key="delete_receipt_button",
            )

            if delete_clicked:
                if delete_receipt(selected_id, current_user_id()):
                    st.success(t("receipt_deleted", receipt_id=selected_id))
                    st.rerun()
                else:
                    st.error(t("delete_failed"))

        with all_tab:
            st.warning(t("delete_all_warning"))

            confirm_text = st.text_input(
                t("type_delete_all"),
                key="delete_all_confirm_text",
            )

            delete_all_clicked = st.button(
                t("delete_all_permanently"),
                disabled=confirm_text != "DELETE ALL",
                use_container_width=True,
                key="delete_all_receipts_button",
            )

            if delete_all_clicked:
                deleted_count = delete_all_receipts(current_user_id())
                st.success(t("deleted_count", count=deleted_count))
                st.rerun()


def get_export_dataframe(filtered_df):
    export_df = format_history_dataframe(filtered_df)

    if export_df.empty:
        return export_df

    return export_df


def find_thai_font_path():
    candidates = [
        r"C:\Windows\Fonts\tahoma.ttf",
        r"C:\Windows\Fonts\Tahoma.ttf",
        r"C:\Windows\Fonts\LeelawUI.ttf",
        r"C:\Windows\Fonts\NotoSansThai-Regular.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf",
        "/System/Library/Fonts/Supplemental/Thonburi.ttf",
    ]

    for path in candidates:
        if os.path.exists(path):
            return path

    return None


def pdf_font_names():
    if current_language() != "ไทย":
        return "Helvetica", "Helvetica-Bold"

    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
    except ImportError:
        return "Helvetica", "Helvetica-Bold"

    font_path = find_thai_font_path()
    if not font_path:
        return "Helvetica", "Helvetica-Bold"

    try:
        pdfmetrics.getFont("ThaiFont")
    except KeyError:
        pdfmetrics.registerFont(TTFont("ThaiFont", font_path))

    return "ThaiFont", "ThaiFont"


def build_receipts_pdf(filtered_df):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    except ImportError as exc:
        raise RuntimeError(t("pdf_error")) from exc

    base_font, bold_font = pdf_font_names()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=28, leftMargin=28, topMargin=28, bottomMargin=28)
    styles = getSampleStyleSheet()
    styles["Title"].fontName = bold_font
    styles["Normal"].fontName = base_font
    story = []

    total_expenses = filtered_df["total_amount"].sum() if not filtered_df.empty else 0.0
    total_vat = filtered_df["vat"].sum() if not filtered_df.empty else 0.0

    deductible_mask = (
        filtered_df["tax_deductible"]
        .fillna("")
        .astype(str)
        .str.lower()
        .eq("deductible")
    ) if not filtered_df.empty else []

    total_deductible = filtered_df.loc[deductible_mask, "total_amount"].sum() if not filtered_df.empty else 0.0

    story.append(Paragraph(t("pdf_title"), styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(t("pdf_receipts_exported", count=len(filtered_df)), styles["Normal"]))
    story.append(Paragraph(t("pdf_total_expenses", amount=f"{total_expenses:,.2f}"), styles["Normal"]))
    story.append(Paragraph(t("pdf_total_deductible", amount=f"{total_deductible:,.2f}"), styles["Normal"]))
    story.append(Paragraph(t("pdf_total_vat", amount=f"{total_vat:,.2f}"), styles["Normal"]))
    story.append(Spacer(1, 18))

    table_data = [[
        t("pdf_col_date"),
        t("pdf_col_store"),
        t("pdf_col_category"),
        t("pdf_col_amount"),
        t("pdf_col_vat"),
        t("pdf_col_tax"),
    ]]

    for row in filtered_df.itertuples(index=False):
        table_data.append(
            [
                str(row.date),
                str(row.store_name)[:28],
                category_label(str(row.category)),
                f"THB {float(row.total_amount):,.2f}",
                f"THB {float(row.vat):,.2f}",
                tax_label(str(row.tax_deductible)),
            ]
        )

    table = Table(table_data, repeatRows=1, colWidths=[64, 132, 88, 78, 68, 82])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), bold_font),
                ("FONTNAME", (0, 1), (-1, -1), base_font),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    story.append(table)
    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()


def render_export_controls(filtered_receipts):
    st.markdown(f'<div class="section-title">{t("export_data")}</div>', unsafe_allow_html=True)

    if filtered_receipts.empty:
        st.info(t("no_filtered_export"))
        return

    export_df = get_export_dataframe(filtered_receipts)

    csv_data = export_df.to_csv(index=False).encode("utf-8-sig")

    col_1, col_2 = st.columns(2)

    with col_1:
        st.download_button(
            label=t("download_csv"),
            data=csv_data,
            file_name="Taxara_Filtered_Receipts.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_2:
        try:
            pdf_data = build_receipts_pdf(filtered_receipts)
            st.download_button(
                label=t("download_pdf"),
                data=pdf_data,
                file_name="Taxara_Receipt_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except RuntimeError as exc:
            st.warning(str(exc))


def render_history_tab():
    st.markdown(f'<div class="section-title">{t("search_filter")}</div>', unsafe_allow_html=True)

    if is_guest_user():
        all_receipts = get_receipts_for_user(None)
    else:
        user_id = current_user_id()
        if user_id is None:
            st.error(t("login_again_history"))
            return

        all_receipts = get_receipts_for_user(user_id)

    filter_col_1, filter_col_2 = st.columns([0.5, 0.5])

    with filter_col_1:
        search_query = st.text_input(
            t("search_store_name"),
            placeholder=t("search_placeholder"),
            key="history_store_search",
        )

    with filter_col_2:
        category_options = []
        if not all_receipts.empty:
            category_options = sorted(
                category
                for category in all_receipts["category"].dropna().unique()
                if str(category).strip()
            )

        selected_categories = st.multiselect(
            t("filter_category"),
            options=category_options,
            key="history_category_filter",
            format_func=category_label,
        )

    filtered_receipts = apply_history_filters(
        all_receipts,
        search_query,
        selected_categories,
    )

    st.markdown(f'<div class="section-title">{t("tax_year_dashboard")}</div>', unsafe_allow_html=True)
    render_analytics_metrics(filtered_receipts)

    st.markdown(f'<div class="section-title">{t("expense_breakdown")}</div>', unsafe_allow_html=True)
    render_category_chart(filtered_receipts)

    render_export_controls(filtered_receipts)

    st.markdown(f'<div class="section-title">{t("receipt_history")}</div>', unsafe_allow_html=True)

    if filtered_receipts.empty:
        st.info(t("no_receipts"))
    else:
        st.dataframe(
            format_history_dataframe(filtered_receipts),
            use_container_width=True,
            hide_index=True,
        )
        render_delete_controls(filtered_receipts)


def show_page():
    init_dashboard_state()
    render_styles()
    remove_auth_ripples()

    with st.sidebar:
        sidebar_analyze_clicked = render_sidebar()

    uploaded_file = current_uploaded_file()

    render_top_nav()
    render_hero(uploaded_file)

    scanner_tab, history_tab = st.tabs(["Scanner & Verification", "History & Analytics"])

    with scanner_tab:
        left_col, right_col = st.columns([0.48, 0.52], gap="large")

        with left_col:
            uploaded_file = render_receipt_viewer()

        with right_col:
            render_verification_panel(uploaded_file, sidebar_analyze_clicked)

    with history_tab:
        render_history_tab()