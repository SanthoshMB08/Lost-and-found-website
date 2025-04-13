import re

def parse_invoice_command(text):
    try:
        # Match command format with flexible text
        match = re.match(
            r'^/generate\s+invoice\s+for\s+(.+?)\s*:\s*(.+)', 
            text, 
            re.IGNORECASE
        )
        
        if not match:
            return {"customer": None, "products": []}

        customer_part, products_part = match.groups()
        
        # Clean customer name
        customer = re.sub(r'\s+', ' ', customer_part.strip()).title()
        
        # Improved product-quantity parsing with lookahead for quantities
        products = []
        # Split on numbers followed by whitespace (potential quantities)
        parts = re.split(r'(?<=\D)(?=\s*\d+\s)', products_part)
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
                
            # Match first quantity in each segment
            match = re.match(r'^\D*?(\d+)\s+(.+)$', part)
            if match:
                qty, product = match.groups()
                products.append((product.strip(), int(qty)))
        
        return {
            "customer": customer,
            "products": products
        }

    except Exception as e:
        print(f"Parsing error: {str(e)}")
        return {"customer": None, "products": []}