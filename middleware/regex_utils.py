import re

def mask_tckn(text: str) -> str:
    return re.sub(r'\b(\d{8})(\d{3})\b', r'********\2', text)

def mask_credit_card(text: str) -> str:
    return re.sub(r'\b(\d{12})(\d{4})\b', r'****-****-****-\2', text)

def mask_email(text: str) -> str:
    def _repl(match):
        user, domain = match.group(1), match.group(2)
        masked_user = user[0] + "***" if len(user) > 0 else "***"
        return f"{masked_user}@{domain}"
    return re.sub(r'([a-zA-Z0-9_.+-]+)@([a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', _repl, text)

def apply_all_masks(text: str) -> str:
    if not text:
        return text
    text = mask_tckn(text)
    text = mask_credit_card(text)
    text = mask_email(text)
    return text