import qrcode
import os

def generate_qr_code(violation_id, vehicle_number):

    # QR link
    data = f"http://10.15.30.154/status/{violation_id}"

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#dc3545", back_color="white")

    # 🔥 correct folder
    folder = "app/static/qrcodes"
    os.makedirs(folder, exist_ok=True)

    filename = f"qr_{violation_id}_{vehicle_number.replace(' ', '')}.png"
    filepath = os.path.join(folder, filename)

    img.save(filepath)

    # 🔥 IMPORTANT → ONLY RELATIVE PATH
    return f"qrcodes/{filename}"