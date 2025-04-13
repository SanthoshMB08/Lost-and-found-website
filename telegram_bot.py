from datetime import datetime
import os
import re
import requests
from dotenv import load_dotenv
from mongo_queries import get_customer_by_name, get_product_by_name, list_all_customers, list_all_products
from invoice_generator import create_invoice
from nlp_utils import fuzzy_match

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
user_sessions = {}

def process_telegram_update(update):
    message = update.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if not chat_id or not text:
        return

    if text.lower().startswith("/start"):
        return send_message(chat_id, "👋 Hi! You can generate an invoice like:\n`/generate invoice for Amira: 4 Augmentin 625 Duo Tablet, 1 Azithral 500`")
    
    if text.lower().startswith("/generate"):
        handle_invoice_creation(chat_id, text)
        return

    if chat_id in user_sessions:
        session = user_sessions[chat_id]
        if session.get("awaiting_customer_selection"):
            handle_customer_selection(chat_id, text)
            return
        if session.get("awaiting_product_selection"):
            handle_product_selection(chat_id, text)
            return
        if session.get("pending_confirmation"):
            handle_confirmation(chat_id, text)
            return

    send_message(chat_id, "⚠️ I didn’t understand that. Try `/start`.")

def handle_invoice_creation(chat_id, text):
    try:
        # Parse command
        customer_part, products_part = re.split(r'\s*:\s*', text, maxsplit=1)
        customer_query = re.sub(r'^/generate\s+invoice\s+for\s+', '', customer_part, flags=re.IGNORECASE).strip()
        
        # Parse products
        products = []
        for item in re.finditer(r'(\d+)\s+([^,]+)(?:,|$)', products_part):
            qty, product = item.groups()
            products.append((product.strip(), int(qty)))

        # Fuzzy match customers
        all_customers = list_all_customers()
        customer_matches = fuzzy_match(customer_query, all_customers, threshold=80, limit=5)
        
        if not customer_matches:
            return send_message(chat_id, "❌ No matching customers found")
        
        if len(customer_matches) > 1:
            user_sessions[chat_id] = {
                "state": "awaiting_customer_selection",
                "customer_matches": [m[0] for m in customer_matches],
                "products": products,
                "current_product_idx": 0,
                "matched_products": [],
                "missing_products": [],
                "awaiting_customer_selection": True
            }
            return send_customer_options(chat_id, customer_matches)
        
        # Single match found
        user_sessions[chat_id] = {
            "matched_customer": customer_matches[0][0],
            "products": products,
            "current_product_idx": 0,
            "matched_products": [],
            "missing_products": [],
            "state": "processing_products"
        }
        start_product_matching(chat_id)

    except Exception as e:
        send_message(chat_id, f"⚠️ Error: {str(e)}")
        print(f"Error: {str(e)}")

def send_customer_options(chat_id, matches):
    options = "\n".join([f"{i+1}. {name}" for i, (name, _) in enumerate(matches)])
    msg = f"🔍 Multiple customers found:\n{options}\n\nPlease select the correct one (1-{len(matches)}):"
    send_message(chat_id, msg)

def handle_customer_selection(chat_id, text):
    try:
        session = user_sessions[chat_id]
        matches = session["customer_matches"]
        
        if not text.isdigit() or not (1 <= int(text) <= len(matches)):
            return send_message(chat_id, "⚠️ Invalid selection. Please try again.")
        
        selected_idx = int(text) - 1
        session["matched_customer"] = matches[selected_idx]
        session["state"] = "processing_products"
        del session["customer_matches"]
        del session["awaiting_customer_selection"]
        
        start_product_matching(chat_id)
        
    except Exception as e:
        send_message(chat_id, f"⚠️ Error: {str(e)}")
        print(f"Customer selection error: {str(e)}")

def start_product_matching(chat_id):
    session = user_sessions[chat_id]
    products = session["products"]
    all_products = list_all_products()
    
    if session["current_product_idx"] >= len(products):
        finalize_invoice_preview(chat_id)
        return
    
    prod_query, qty = products[session["current_product_idx"]]
    clean_query = re.sub(r'\s*(?:,|and|or|also|need|for|purchasing)\b.*$', '', prod_query, flags=re.IGNORECASE).strip()
    
    product_matches = fuzzy_match(clean_query, all_products, threshold=80, limit=5)
    
    if not product_matches:
        session["missing_products"].append(prod_query)
        session["current_product_idx"] += 1
        start_product_matching(chat_id)
        return
    
    if len(product_matches) == 1:
        session["matched_products"].append((product_matches[0][0], qty))
        session["current_product_idx"] += 1
        start_product_matching(chat_id)
        return
    
    # Multiple product matches
    session["state"] = "awaiting_product_selection"
    session["current_product_matches"] = [m[0] for m in product_matches]
    session["awaiting_product_selection"] = True
    send_product_options(chat_id, product_matches, qty)

def send_product_options(chat_id, matches, qty):
    options = "\n".join([f"{i+1}. {name}" for i, (name, _) in enumerate(matches)])
    msg = f"🔍 Multiple products found for quantity {qty}:\n{options}\n\nPlease select the correct one (1-{len(matches)}):"
    send_message(chat_id, msg)

def handle_product_selection(chat_id, text):
    try:
        session = user_sessions[chat_id]
        matches = session["current_product_matches"]
        
        if not text.isdigit() or not (1 <= int(text) <= len(matches)):
            return send_message(chat_id, "⚠️ Invalid selection. Please try again.")
        
        selected_idx = int(text) - 1
        selected_product = matches[selected_idx]
        qty = session["products"][session["current_product_idx"]][1]
        
        session["matched_products"].append((selected_product, qty))
        session["current_product_idx"] += 1
        del session["current_product_matches"]
        del session["awaiting_product_selection"]
        session["state"] = "processing_products"
        
        start_product_matching(chat_id)
        
    except Exception as e:
        send_message(chat_id, f"⚠️ Error: {str(e)}")
        print(f"Product selection error: {str(e)}")

def finalize_invoice_preview(chat_id):
    session = user_sessions[chat_id]
    
    msg = "📝 Invoice Preview:\n"
    msg += f"Customer: *{session['matched_customer']}*\n\n"
    msg += "Items:\n" + "\n".join([f"- {qty} x {name}" for name, qty in session['matched_products']])
    
    if session['missing_products']:
        msg += f"\n\n❌ Missing products:\n{', '.join(session['missing_products'])}"
    
    msg += "\n\n✅ Confirm with 'yes' or cancel with 'no'"
    
    session["pending_confirmation"] = True
    del session["current_product_idx"]
    send_message(chat_id, msg)

def handle_confirmation(chat_id, text):
    session = user_sessions.get(chat_id)
    if not session:
        return send_message(chat_id, "⚠️ Session expired. Start over.")

    text = text.lower().strip()
    if text not in ['yes', 'no']:
        return send_message(chat_id, "⚠️ Please respond with 'yes' or 'no'")

    if text == 'no':
        user_sessions.pop(chat_id)
        return send_message(chat_id, "❌ Invoice cancelled.")

    try:
        # Get validated customer
        customer = get_customer_by_name(session['matched_customer'])
        if not customer:
            return send_message(chat_id, "❌ Customer not found in database")

        # Validate all products
        final_products = []
        for prod_name, qty in session['matched_products']:
            product = get_product_by_name(prod_name)
            if not product:
                return send_message(chat_id, f"❌ Product not found: {prod_name}")
            final_products.append({
                "name": product['name'],
                "quantity": qty,
                "unit_price": product['unit_price'],
                "subtotal": product['unit_price'] * qty
            })

        # Calculate totals
        subtotal = sum(p['subtotal'] for p in final_products)
        tax_rate = float(os.getenv("TAX_RATE", 18))
        tax = subtotal * tax_rate / 100
        total = subtotal + tax

        # Generate PDF
        safe_name = re.sub(r'[^a-zA-Z0-9]+', '_', customer['name']).strip('_')
        filename = f"invoices/{safe_name}_{int(datetime.now().timestamp())}.pdf"
        create_invoice(customer, final_products, total, tax, filename)
        
        # Send and cleanup
        send_pdf(chat_id, filename)
        user_sessions.pop(chat_id)
        return

    except Exception as e:
        send_message(chat_id, f"⚠️ Error generating invoice: {str(e)}")
        user_sessions.pop(chat_id)
        print(f"Confirmation error: {str(e)}")

def send_message(chat_id, text, parse_mode='Markdown'):
    try:
        requests.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            },
            timeout=10
        )
    except Exception as e:
        print(f"Message send error: {str(e)}")

def send_pdf(chat_id, file_path):
    try:
        with open(file_path, 'rb') as f:
            requests.post(
                f"{BASE_URL}/sendDocument",
                files={'document': f},
                data={'chat_id': chat_id},
                timeout=20
            )
    except Exception as e:
        print(f"PDF send error: {str(e)}")
        send_message(chat_id, "⚠️ Failed to send PDF. Please try again.")