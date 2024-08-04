import pyotp
import qrcode
import io

def gen2fa(user_name):
    key = pyotp.random_base32()
    otp_string=f"otpauth://totp/{user_name}?secret={key}&issuer=Antecam"

    qr = qrcode.QRCode()
    qr.add_data(otp_string)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
    return key

def check2fa(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)