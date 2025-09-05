Per‑taste honey images required by shop/templates/shop_products.html

Place the following files in this folder (static/images). These exact filenames are referenced by the template to display the correct image for each taste. If a file is missing, the template will fall back to honey.jpg.

Expected filenames:
- honey_akacja.jpg       # Miód Akacjowy (taste == "Akacja")
- honey_rzepak.jpg       # Miód Rzepakowy (taste == "Rzepak")
- honey_spadz.jpg        # Miód Spadziowy (taste == "Spadź")
- honey_facelia.jpg      # Miód Faceliowy (taste == "Facelia")
- honey_gryka.jpg        # Miód Gryczany (taste == "Gryka")
- honey_lipa.jpg         # Miód Lipowy (taste == "Lipa")
- honey_malina.jpg       # Miód Malinowy (taste == "Malina")
- honey_imbir.jpg        # Miód Imbir z cytryną (taste == "Imbir")
- honey_zurawina.jpg     # Miód Żurawinowy (taste == "Żurawina")
- honey_porzeczka.jpg    # Miód Porzeczkowy (taste == "Porzeczka")

Already present, used elsewhere:
- honey.jpg              # Generic fallback image for honey
- bee_product.webp       # Generic image for non-honey bee products

Recommendations:
- Format: JPG (RGB), quality ~80–85; keep file sizes low (< 200 KB) for faster loads.
- Dimensions: around 800×600 px or similar aspect ratio used by your card layout.
- Filenames must match exactly (lowercase, underscores, Polish characters normalized as used above).
- After adding images, run: python manage.py collectstatic (in production) so they’re available via the static files pipeline.

Where this is used:
- shop/templates/shop_products.html — conditional blocks choose one of these images based on honey.taste.taste.

If you don’t have final photos yet:
- You can temporarily copy honey.jpg to the required filenames, or ask to auto-generate simple placeholders.
