"""
Module 01 - Activity 1: Token Counter
======================================
See how AI breaks text into tokens.
Compare English vs Arabic cost.

Run: python activity-01-tokens.py
"""

import tiktoken

# GPT-4o tokenizer
enc = tiktoken.encoding_for_model("gpt-4o")

# --- Same incident report in two languages ---

english_report = "Vehicle collision reported on Highway 7 near exit 3. Two vehicles involved. One driver reported minor injuries. Police and ambulance dispatched at 14:30."

arabic_report = "تم الإبلاغ عن تصادم مركبات على الطريق السريع ٧ بالقرب من المخرج ٣. مركبتان متورطتان. أفاد أحد السائقين بإصابات طفيفة. تم إرسال الشرطة والإسعاف الساعة ١٤:٣٠."

# --- Count tokens ---

en_tokens = enc.encode(english_report)
ar_tokens = enc.encode(arabic_report)

print("=" * 60)
print("TOKEN COMPARISON: Same Incident Report")
print("=" * 60)
print()
print(f"English: {len(en_tokens)} tokens")
print(f"Arabic:  {len(ar_tokens)} tokens")
print(f"Ratio:   Arabic is {len(ar_tokens)/len(en_tokens):.1f}x more tokens")
print()

# --- Cost calculation ---

PRICE_INPUT = 2.50   # $ per 1M tokens (GPT-4o input)
PRICE_OUTPUT = 10.0  # $ per 1M tokens (GPT-4o output)
REPORTS_PER_DAY = 1000

print("=" * 60)
print("COST ESTIMATE: 1,000 reports/day")
print("=" * 60)
print()

en_daily_tokens = len(en_tokens) * REPORTS_PER_DAY
ar_daily_tokens = len(ar_tokens) * REPORTS_PER_DAY

en_cost = (en_daily_tokens / 1_000_000) * PRICE_INPUT
ar_cost = (ar_daily_tokens / 1_000_000) * PRICE_INPUT

print(f"English: {en_daily_tokens:,} tokens/day → ${en_cost:.2f}/day → ${en_cost*30:.0f}/month")
print(f"Arabic:  {ar_daily_tokens:,} tokens/day → ${ar_cost:.2f}/day → ${ar_cost*30:.0f}/month")
print()

# --- TRY IT YOURSELF ---

print("=" * 60)
print("YOUR TURN: Edit the text below and run again!")
print("=" * 60)
print()

your_report = "Write your own incident report here in any language"
your_tokens = enc.encode(your_report)
print(f"Your report: {len(your_tokens)} tokens")
