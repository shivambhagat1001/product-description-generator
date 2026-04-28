import pandas as pd
import sys


try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable, **kwargs):
        total = kwargs.get('total', len(iterable) if hasattr(iterable, '__len__') else '?')
        for i, item in enumerate(iterable, 1):
            print(f"\r  {i}/{total}", end='', flush=True)
            yield item
        print()

INPUT_CSV  = "input.csv"
OUTPUT_CSV = "output.csv"

def parse_additional_attributes(attr_string):
    data = {}
    if pd.isna(attr_string):
        return data
    for part in str(attr_string).split('|'):
        if '=' in part:
            key, value = part.split('=', 1)
            data[key.strip()] = value.strip()
    return data

def extract_fields(product):
    attrs = parse_additional_attributes(product.get('additional_attributes', ''))

    def get(col, fallback_key=None):
        v = product.get(col, '') or (attrs.get(col, '') if fallback_key is None else attrs.get(fallback_key, ''))
        return str(v).replace('.0', '').strip() if v and str(v) != 'nan' else ''

    brand     = get('mgs_brand')
    tyre_size = get('tyre_size')
    pattern   = product.get('pattern', '') or attrs.get('display_name', '') or ''
    pattern   = str(pattern).strip() if str(pattern) != 'nan' else ''
    load      = get('load_index')
    year      = get('year')
    country   = get('country') or 'UAE'
    rim       = get('rim')
    tyre_type = get('tyre_type')
    category  = get('tyres_category')
    warranty  = get('warranty_period') or '1 Year Warranty'
    price     = get('price') or get('price_per_item')

    return brand, tyre_size, pattern, load, year, country, rim, tyre_type, category, warranty, price


def generate_description(brand, tyre_size, pattern, load, year, country, rim, tyre_type, category, warranty, price, variant):
    if variant == 0:
        return (
            f"<p>Upgrade your vehicle's performance with the <strong>{brand} {pattern}</strong>. "
            f"Specifically engineered for reliability, this <strong>{tyre_size}</strong> tyre features "
            f"a load index of <strong>{load}</strong>, making it an ideal choice for drivers seeking "
            f"stability and durability on UAE roads. Manufactured in <strong>{country}</strong>, this "
            f"<strong>{year}</strong> production model is built to withstand high temperatures while "
            f"providing a smooth driving experience.</p>"
            f"<ul>"
            f"<li>Tyre Size: {tyre_size}</li>"
            f"<li>Load Index: {load}</li>"
            f"<li>Rim Size: {rim}\"</li>"
            f"<li>Year of Manufacture: {year}</li>"
            f"<li>Country of Origin: {country}</li>"
            f"<li>Category: {category}</li>"
            f"</ul>"
            f"<p>At TyresCart.ae, we ensure you receive 100% authentic products backed by a "
            f"<strong>{warranty}</strong> and professional installation across our UAE network. "
            f"The listed price of <strong>AED {price}</strong> is a fully fitted price per item.</p>"
        )
    elif variant == 1:
        return (
            f"<p>The <strong>{brand} {pattern}</strong> in size <strong>{tyre_size}</strong> is built "
            f"for UAE drivers who demand performance and longevity. With a load index of <strong>{load}</strong> "
            f"and <strong>{year}</strong> manufacturing standards, this tyre delivers confident handling "
            f"on Dubai's highways and city roads alike.</p>"
            f"<ul>"
            f"<li>Size: {tyre_size} | Rim: {rim}\"</li>"
            f"<li>Load Index: {load}</li>"
            f"<li>Manufactured: {year} | Origin: {country}</li>"
            f"<li>Type: {tyre_type} | Range: {category}</li>"
            f"</ul>"
            f"<p>Sourced from <strong>{country}</strong> and sold exclusively as genuine stock, every "
            f"purchase at TyresCart.ae includes a <strong>{warranty}</strong> and full fitting service "
            f"at our UAE locations. Price shown — <strong>AED {price}</strong> — is a fully fitted price per item.</p>"
        )
    else:
        return (
            f"<p>Designed for the demands of UAE roads, the <strong>{brand} {pattern}</strong> "
            f"({tyre_size}) combines durability with everyday comfort. The <strong>{load}</strong> "
            f"load index ensures it handles everything from light city driving to highway cruising with ease.</p>"
            f"<ul>"
            f"<li>Tyre Size: {tyre_size}</li>"
            f"<li>Load &amp; Speed Rating: {load}</li>"
            f"<li>Rim Diameter: {rim}\"</li>"
            f"<li>Production Year: {year} | Made in: {country}</li>"
            f"<li>Vehicle Type: {tyre_type} | Segment: {category}</li>"
            f"</ul>"
            f"<p>As a <strong>{year}</strong> model manufactured in <strong>{country}</strong>, it meets "
            f"modern heat-resistance standards essential for the Gulf climate. TyresCart.ae offers this tyre "
            f"at <strong>AED {price}</strong> (fully fitted price per item) with a guaranteed "
            f"<strong>{warranty}</strong> and professional fitting included.</p>"
        )


def generate_faq(brand, tyre_size, pattern, load, year, country, tyre_type, category, warranty, price, variant):
    if variant == 0:
        return (
            f'<div class="product-faqs"><h3>Frequently Asked Questions</h3>'
            f'<div class="faq-item"><h4>Is the {brand} {pattern} suitable for UAE weather?</h4>'
            f"<p>Yes, the {brand} {pattern} is designed to handle diverse road conditions. The {year} model "
            f"includes compound materials that offer heat resistance, essential for the climate in Dubai and the wider UAE.</p></div>"
            f'<div class="faq-item"><h4>What is included in the price of the {tyre_size} {brand} tyre?</h4>'
            f"<p>The fully fitted price of AED {price} includes professional fitting, wheel balancing, "
            f"a new standard valve, and eco-friendly disposal of your old tyres — no hidden charges.</p></div>"
            f'<div class="faq-item"><h4>Does this tyre come with a warranty?</h4>'
            f"<p>Every {brand} tyre purchased from TyresCart.ae comes with a <strong>{warranty}</strong>, "
            f"ensuring peace of mind regarding manufacturing defects.</p></div>"
            f'<div class="faq-item"><h4>Where is the {brand} {pattern} manufactured?</h4>'
            f"<p>This tyre is manufactured in <strong>{country}</strong> and meets international quality "
            f"standards. All products sold on TyresCart.ae are 100% authentic.</p></div>"
            f'<div class="faq-item"><h4>Is this tyre compatible with my vehicle?</h4>'
            f"<p>The {tyre_size} size with a {load} load index fits a wide range of {tyre_type.lower()} "
            f"vehicles. If you are unsure, contact our team at TyresCart.ae for guidance.</p></div></div>"
        )
    elif variant == 1:
        return (
            f'<div class="product-faqs"><h3>Frequently Asked Questions</h3>'
            f'<div class="faq-item"><h4>Can the {brand} {pattern} handle Dubai\'s summer heat?</h4>'
            f"<p>Absolutely. The {brand} {pattern} ({year}) is engineered with heat-resistant compounds "
            f"suited for the extreme summer temperatures in the UAE and Gulf region.</p></div>"
            f'<div class="faq-item"><h4>Does the {tyre_size} price include fitting and balancing?</h4>'
            f"<p>Yes. The listed price of AED {price} is a fully fitted price that covers professional "
            f"mounting, dynamic wheel balancing, a new valve, and responsible disposal of your existing tyres.</p></div>"
            f'<div class="faq-item"><h4>What warranty do I get with this {brand} tyre?</h4>'
            f"<p>All {brand} tyres from TyresCart.ae are covered by a <strong>{warranty}</strong> against "
            f"manufacturing defects. Our team will assist you with any warranty claim.</p></div>"
            f'<div class="faq-item"><h4>Is this a {year} production tyre?</h4>'
            f"<p>Yes, the {brand} {pattern} listed here is a <strong>{year}</strong> production model. "
            f"TyresCart.ae only stocks fresh inventory to ensure safety and longevity.</p></div>"
            f'<div class="faq-item"><h4>Which vehicles does the {tyre_size} fit?</h4>'
            f"<p>This tyre size — {tyre_size} with load index {load} — is compatible with many "
            f"{tyre_type.lower()} models. Check your vehicle door placard or contact us to confirm.</p></div></div>"
        )
    else:
        return (
            f'<div class="product-faqs"><h3>Frequently Asked Questions</h3>'
            f'<div class="faq-item"><h4>How does the {brand} {pattern} perform on UAE roads?</h4>'
            f"<p>The {brand} {pattern} is well-suited to UAE road conditions — from smooth highways to "
            f"urban roads. Its {load} rating ensures stable performance even when fully loaded.</p></div>"
            f'<div class="faq-item"><h4>What fitting services come with my {brand} {pattern} purchase?</h4>'
            f"<p>Your AED {price} includes everything: expert tyre fitting, computerised wheel balancing, "
            f"new valve installation, and eco-disposal of old tyres — a complete, hassle-free service.</p></div>"
            f'<div class="faq-item"><h4>How long is the warranty on this tyre?</h4>'
            f"<p>TyresCart.ae provides a <strong>{warranty}</strong> on the {brand} {pattern}. This covers "
            f"manufacturing faults and gives you confidence in your purchase.</p></div>"
            f'<div class="faq-item"><h4>Is the {brand} {pattern} a budget or premium tyre?</h4>'
            f"<p>The {brand} {pattern} falls in the <strong>{category}</strong> category, offering reliable "
            f"performance and value for money — ideal for everyday driving in the UAE.</p></div>"
            f'<div class="faq-item"><h4>Can I verify the authenticity of this tyre?</h4>'
            f"<p>Yes. All tyres on TyresCart.ae are sourced directly from authorised distributors. "
            f"The {brand} {pattern} (made in {country}, {year}) comes with original manufacturer markings.</p></div></div>"
        )


def generate_short_description(brand, tyre_size, pattern, load, year, country, category, warranty, price, variant):
    if variant == 0:
        return (f"The {brand} {pattern} ({tyre_size}) is a {category.lower()} range tyre "
                f"manufactured in {country} ({year}), rated {load}. "
                f"Priced at AED {price} — fully fitted price including balancing and valve.")
    elif variant == 1:
        return (f"Shop the {brand} {pattern} in size {tyre_size} — a {year} {category.lower()} tyre "
                f"from {country} with a {load} load rating. "
                f"AED {price} fully fitted at TyresCart.ae UAE locations.")
    else:
        return (f"{brand} {pattern} {tyre_size} — {year} model, made in {country}, "
                f"load index {load}. Available at AED {price} (fully fitted price) "
                f"with {warranty} at TyresCart.ae.")

print(f"📂 Reading {INPUT_CSV}...")
df = pd.read_csv(INPUT_CSV, low_memory=False)
print(f"   → {len(df)} rows loaded\n")

print("🚀 Generating descriptions and FAQs...")
for i in tqdm(range(len(df))):
    product = df.iloc[i].to_dict()
    brand, tyre_size, pattern, load, year, country, rim, tyre_type, category, warranty, price = extract_fields(product)

    desc_variant  = i % 3
    faq_variant   = (i + 1) % 3
    short_variant = i % 3

    description = (
        generate_description(brand, tyre_size, pattern, load, year, country, rim, tyre_type, category, warranty, price, desc_variant)
        + "\n"
        + generate_faq(brand, tyre_size, pattern, load, year, country, tyre_type, category, warranty, price, faq_variant)
    )

    df.at[i, 'description']       = description
    df.at[i, 'short_description'] = generate_short_description(brand, tyre_size, pattern, load, year, country, category, warranty, price, short_variant)

df.to_csv(OUTPUT_CSV, index=False)
print(f"\n✅ Done! {len(df)} products processed.")
print(f"📤 Output saved as: {OUTPUT_CSV}")
print(f"\n📥 Magento Import:")
print(f"   Admin → System → Data Transfer → Import")
print(f"   Entity Type: Products → Choose File → {OUTPUT_CSV} → Check Data → Import")
