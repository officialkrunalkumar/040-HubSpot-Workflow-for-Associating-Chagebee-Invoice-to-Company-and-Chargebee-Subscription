import os, time, random
from hubspot import HubSpot
from pprint import pprint
from hubspot.crm.associations.v4 import ApiException
from hubspot.crm.companies import PublicObjectSearchRequest, ApiException

def main(event):
  time.sleep(random.randint(1, 10))
  
  client = HubSpot(access_token=os.getenv('RevOps'))

  customer_id = event.get('inputFields').get('customer_id')

  invoice_id = event.get('inputFields').get('invoice_id')

  public_object_search_request = PublicObjectSearchRequest(limit=1, after=0, sorts=["desc"], properties=["hs_object_id"], filter_groups=[{"filters":[{"propertyName":"chargebee_customer_id","value":customer_id,"operator":"EQ"}]}])

  try:
    api_response = client.crm.companies.search_api.do_search(public_object_search_request=public_object_search_request)
    pprint(api_response)

    company_id = api_response.results[0].id
    print(company_id)
  except ApiException as e:
    print("Exception when calling search_api->do_search: %s\n" % e)

  try:
    api_response = client.crm.associations.v4.basic_api.create_default(from_object_type="companies", from_object_id=company_id, to_object_type="2-37766506", to_object_id=invoice_id)
    pprint(api_response)
  except ApiException as e:
    print("Exception when calling basic_api->create_default: %s\n" % e)
