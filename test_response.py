import logging
import os

import collections
import json
import requests
import urllib.parse


logger = logging.getLogger(__name__)


if __name__ == "__main__":
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname('data.json')))
    with open(os.path.join(__location__, 'data.json')) as datafile:
        data = json.load(datafile)

    urlPrefix = 'https://www.vroomly.com/backend_challenge/labour_times/'

    quotations = []
    for intervention in data['interventions']:
        quotation = dict()
        for part_spec in intervention['parts_spec']:
            for part in data['parts']:
                if part['type'] == part_spec['type']:
                    for workshop in data['workshops']:
                        quotation['car_id'] = part['car_id']
                        quotation['workshop_id'] = workshop['id']
                        quotation['intervention_id'] = intervention['id']
                        quotation['parts_price'] = part['price'] * part_spec['count']
        quotations.append(quotation)

    for quotation in quotations:
        try:
            response = requests.get(
                urllib.parse.urljoin(urlPrefix, str(quotation['car_id']), str(quotation['intervention_id'])),
                timeout=10,
            )
            response.raise_for_status()
            quotation['services_price'] = response['services_price']
        except requests.RequestException as e:
            logger.info('Error while getting services price: %s(%s)', type(e), e)

    print(quotations)
