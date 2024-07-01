import requests
import os
from datetime import datetime

import logging
import src.parameters as param
from src.db_schema.ticket_schema import Tickets_Schema
logger = logging.getLogger(param.LOGGER_NAME)

# def regular_report(dict):

def send_message(header:str, message:str=""):

    TOKEN = param.TELEGRAM_BOT_TOKEN
    chat_id = param.TELEGRAM_CHAT_ID
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message =  f"{current_date_time} - {param.NODE_NAME} - {header} \n{message}"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

    # logger.debug(url)
    result = url
    if(param.SEND_NOTIF == 1):
        result = requests.get(url).json()
    else:
        logger.info(f'SENDING NOTIFICATION\n\n {message}')
    # logging.info(result)

    return url

def send_reguler_report(report_input:dict):
    logger.debug(report_input)
    msg = ""
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_date_time = (datetime.now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
    msg += f'Start Time: {start_date_time}\n'
    msg += f'End Time: {current_date_time}\n'
    for key in report_input.keys():
        msg += f'{key.upper()} \n'

        logger.debug(report_input[key])
        for ca_name, value in report_input[key].items():
            value_ = round(int(value), 2)
        
            if(value_ < 100 and value_ >= 50):
                msg += f'\U000026A0 {ca_name} : {value_}% \n'
            elif(value_ < 50):
                msg += f'\U0001F525 {ca_name} : {value_}% \n'
            else:
                msg += f'\U00002705 {ca_name} : {value_}% \n'
                
        
        msg += "\n"
    
    send_message("Reguler Report", msg)
    return msg

def send_ticket_notification(ticket_:Tickets_Schema):
    msg = ""
    ticket = to_dict_notifications(ticket_)
    if(ticket["resolve"]):
        msg += f'\U00002705 {ticket["message"]} \n'
        msg += f'Created : {ticket["start"]} \n'
        msg += f'Resolved : {ticket["end"]}'
        send_message("Ticket Resolve", msg)
    else:
        msg += f'\U0001F525 {ticket["message"]} \n'
        msg += f'Created : {ticket["start"]}\n'
        send_message("Ticket Created", msg)

    return msg

def to_dict_notifications(ticket: Tickets_Schema):
    ret_ = ticket.__dict__
    res = {}
    for key, value in ret_.items():
        if(isinstance(value, datetime)):
            val = None if value == "" else datetime.strftime(value, "%Y-%m-%d %H:%M:%S")
        else:
            val = value
        res[key] = val
    
    return res