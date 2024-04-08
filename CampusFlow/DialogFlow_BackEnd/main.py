from fastapi import FastAPI, HTTPException
from fastapi import Request
import db_helper
from fastapi.responses import JSONResponse
import json

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    try:
        payload = await request.json()

        intent = payload['queryResult']['intent']['displayName']
        parameters = payload['queryResult']['parameters']
        output_contexts = payload['queryResult']['outputContexts']

        if intent == "bus.fees":
            return get_fees(parameters)
        elif intent == "bus.time":
            return get_time(parameters)
        elif intent == "bus.names":
            return get_bus_name(parameters)
        elif intent == "room.loc":
            return get_room_loc(parameters)
        elif intent == "lecturer.loc":
            return get_lec_loc(parameters)
        elif intent == "file.link":
            return get_link(parameters)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def get_fees(parameters: dict):
    destination_name = parameters['destination-names']
    fees = db_helper.get_bus_fee(destination_name)

    if fees:
        fulfillment_text = f"The fees for bus from {destination_name} is ₹{fees}."
    else:
        fulfillment_text = f"Could not find destination."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def get_time(parameters: dict):
    destination_name = parameters['destination-names']
    bus_name = parameters['bus-names']
    time = db_helper.get_bus_time(destination_name, bus_name)

    if time:
        fulfillment_text = f"Bus {bus_name} reaches {destination_name} at {time} AM."
    else:
        fulfillment_text = f"The destination or bus name that you have entered is incorrect."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def get_bus_name(parameters: dict):
    destination_name = parameters['destination-names']
    bus_names = db_helper.get_all_bus_names(destination_name)

    if bus_names:
        if len(bus_names) == 1:
            fulfillment_text = f"Bus {bus_names[0]} has a stop at {destination_name}."
        else:
            bus_names_str = ', '.join(bus_names)
            fulfillment_text = f"Buses {bus_names_str} have stops at {destination_name}."
    else:
        fulfillment_text = f"Sorry, the destination cannot be found."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def get_room_loc(parameters: dict):
    room_name = parameters['room-names']
    room_info = db_helper.get_room_info(room_name)

    if room_info:
        fulfillment_text = (
            f"{room_info['Floor']}, "
            f"{room_info['BlockName']}, "
            f"{room_info['Landmark']}."
        )
    else:
        fulfillment_text = f"Could not find the room."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def get_lec_loc(parameters: dict):
    lec_name = parameters['lecturer-name']
    lec_info = db_helper.get_lec_info(lec_name)

    if lec_info:
        fulfillment_text = (
            f"{lec_name} :  "
            f"{lec_info['Floor']}, "
            f"{lec_info['BlockName']}, "
            f"{lec_info['Landmark']}."
        )
    else:
        fulfillment_text = f"Could not find the room."

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })



def get_link(parameters: dict):
    link_name = parameters['file-names']
    link_type = parameters['file-type']
    link_url = db_helper.get_link_helper(link_name,link_type)

    if link_url is not None:
        custom_payload = {
            "richContent": [
                [
                    {
                        "type": "button",
                        "icon": {
                            "type": "insert_link",
                            "color": "#ff9800"
                        },
                        "text": link_name+" "+link_type,
                        "link": link_url
                    }
                ]
            ]
        }

        response_data = {
            "fulfillmentMessages": [
                {
                    "payload": custom_payload
                }
            ]
        }

        return JSONResponse(content=response_data)

        # not_found_response = {
        #     "fulfillmentText": f"{link_url}"
        # }
        # return JSONResponse(content=not_found_response)


    else:
        not_found_response = {
            "fulfillmentText": "Sorry, the requested file was not found."
        }
        return JSONResponse(content=not_found_response)