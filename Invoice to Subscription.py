import os, time, random
from hubspot import HubSpot
from pprint import pprint
from hubspot.crm.associations.v4 import ApiException
from hubspot.crm.objects import PublicObjectSearchRequest, ApiException

def main(event):
    time.sleep(random.randint(1, 10))  # Simulate random delay for API rate-limiting

    client = HubSpot(access_token=os.getenv('RevOps'))

    subscription_id = event.get('inputFields', {}).get('subscription_id')
    invoice_id = event.get('inputFields', {}).get('invoice_id')

    if not subscription_id or not invoice_id:
        print("Missing subscription_id or invoice_id.")
        return

    # Define the search request
    public_object_search_request = PublicObjectSearchRequest(
        limit=1,
        after=0,
        sorts=["desc"],
        properties=["hs_object_id"],
        filter_groups=[{
            "filters": [{"propertyName": "subscription_id", "value": subscription_id, "operator": "EQ"}]
        }]
    )

    try:
        # Search for subscription object
        api_response = client.crm.objects.search_api.do_search(
            object_type="2-14800898",
            public_object_search_request=public_object_search_request
        )
        if not api_response.results:
            print("No matching subscription found.")
            return

        subscription_id = api_response.results[0].id
        print(f"Found subscription_id: {subscription_id}")
    except ApiException as e:
        print(f"Exception during search_api->do_search: {e}")
        return

    try:
        # Associate subscription with invoice
        api_response = client.crm.associations.v4.basic_api.create_default(
            from_object_type="2-14800898",
            from_object_id=subscription_id,
            to_object_type="2-37766506",
            to_object_id=invoice_id
        )
        pprint(api_response)
    except ApiException as e:
        print(f"Exception during basic_api->create_default: {e}")
