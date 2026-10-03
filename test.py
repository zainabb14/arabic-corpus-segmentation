import hashlib


# Given data
order_number = "38729"
order_amount = "169,43"
order_currency = "AED"
order_description = "Payment Order #38729 in the store https://canadapharmahub.com/"
password = "ebcf58649e5d867f0da72b4346eba24a"

# Create the MD5 string
md5_string = order_number + order_amount + order_currency + order_description + password
md5_encoded = hashlib.md5(md5_string.upper().encode()).hexdigest()

# Create the SHA1 hash of the MD5 encoded string (uppercase)
sha1_hash = hashlib.sha1(md5_encoded.encode()).hexdigest()


print(sha1_hash)
