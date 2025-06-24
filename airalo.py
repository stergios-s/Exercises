import requests
import credentials

# Step 0: Define debug log variables
token_debug_logs = True
order_debug_logs = True
list_debug_logs = True

# Step 1: Get the access token
token_url = "https://sandbox-partners-api.airalo.com/v2/token"
token_headers = {
    "Accept": "application/json"
}
token_data = {
    "client_id": credentials.data['client_id'],
    "client_secret": credentials.data['client_secret'],
    "grant_type": "client_credentials"
}

token_response = requests.post(token_url, headers=token_headers, data=token_data)
if token_response.status_code != 200:
    error_msg = f"Expected Status code 200 but received {token_response.status_code}."
    raise ValueError(error_msg)
token_json = token_response.json()
access_token = token_json["data"]["access_token"]

print(f"\n==> Debug logs Step 1: Status code = {token_response.status_code}") if token_debug_logs else ""
print(f"==> Debug logs Step 1: Complete json response = {token_response.json()}") if token_debug_logs else ""
print(f"==> Debug logs Step 1: Access token = {access_token}") if token_debug_logs else ""


# Step 2: Order 6 "merhaba-7days-1gb" eSIMs
order_url = "https://sandbox-partners-api.airalo.com/v2/orders"
order_headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}"
}
order_data = {
    "quantity": "6",
    "package_id": "merhaba-7days-1gb",
    "type": "sim",
    "description": "Order 6 sim cards merhaba-7days-1gb"
}

order_response = requests.post(order_url, headers=order_headers, data=order_data)
if order_response.status_code != 200:
    error_msg = f"Expected Status code 200 but received {order_response.status_code}."
    raise ValueError(error_msg)

order_json = order_response.json()

order_code = order_json["data"]["code"]
order_date = order_json["data"]["created_at"].split()[0]
order_package = order_json["data"]["package_id"]
if order_package != "merhaba-7days-1gb":
    error_msg = f"Expected order_package 'merhaba-7days-1gb' but received {order_package}."
    raise ValueError(error_msg)
order_quantity = order_json["data"]["quantity"]
if order_quantity != 6:
    error_msg = f"Expected order_quantity 6 but received {order_quantity}."
    raise ValueError(error_msg)

print(f"\n==> Debug logs Step 2: Status code = {order_response.status_code}") if order_debug_logs else ""
print(f"==> Debug logs Step 2: Complete json response = {order_response.json()}") if order_debug_logs else ""
print(f"==> Debug logs Step 2: Order code = {order_code}") if order_debug_logs else ""
print(f"==> Debug logs Step 2: Order date = {order_date}") if order_debug_logs else ""


# Step 3: List eSIMs and related order info
def get_filtered_esims(access_token, order_code, target_package_id):
    """
    Filter eSIMs with order code and package id
    """

    list_url = "https://sandbox-partners-api.airalo.com/v2/sims"
    list_headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    list_params = {
        "include": "order",
        "page": "1",
        "filter[code]": order_code,
        "filter[created_at]": f"{order_date} - {order_date}"
    }

    matching_esims = []

    while True:
        list_response = requests.get(list_url, headers=list_headers, params=list_params)
        if list_response.status_code != 200:
            error_msg = f"Expected Status code 200 but received {list_response.status_code}."
            raise ValueError(error_msg)
        list_data = list_response.json().get("data", [])
        # print(f"\n==> Debug logs Step 3: Raw data batch: {list_data}")

        for esim in list_data:
            if esim["simable"]["code"] == order_code and esim["simable"]["package_id"] == target_package_id:
                matching_esims.append(esim)

        if not list_response.json().get("links", {}).get("next"):
            break

        list_params["page"] = str(int(list_params["page"]) + 1)

    return matching_esims


target_package_id = "merhaba-7days-1gb"

filtered_esims = get_filtered_esims(access_token, order_code, target_package_id)

print(f"\n==> Debug logs Step 3: Found {len(filtered_esims)} eSIMs with package_id 'merhaba-7days-1gb' and order code "
      f"{order_code}")
for idx, esim in enumerate(filtered_esims, start=1):
    print(f"   {idx}. eSIM ID: {esim.get('id')}")

if len(filtered_esims) != 6:
    error_msg = f"Expected 6 eSIMs with package_id '{target_package_id}' and order code {order_code}, but found " \
                f"{len(filtered_esims)}."
    raise ValueError(error_msg)



