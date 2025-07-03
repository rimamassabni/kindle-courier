from azure.communication.email import EmailClient
from azure.core.exceptions import HttpResponseError
import logging
import os
import base64


def encode_file_to_base64(file_path) -> bytes:
    """
    Encodes the contents of a file to base64.
    :param file_path: Path to the file to be encoded.
    :return: Base64 encoded string of the file contents.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        file_contents = file.read()

    file_bytes_b64 = base64.b64encode(bytes(file_contents, "utf-8"))
    return file_bytes_b64


def send_email(files):
    connection_string = os.environ["EMAIL_CONNECTION_STRING"]
    email_client = EmailClient.from_connection_string(connection_string)

    message = {
        "content": {"subject": "Kindle Courier Daily Digest", "plainText": ""},
        "recipients": {"to": [{"address": os.environ["KINDLE_ACCOUNT_EMAIL"]}]},
        "senderAddress": "DoNotReply@79fec668-f8bf-462e-b586-f4858808e86e.azurecomm.net",
        "attachments": [],
    }

    for file_path in files:
        logging.info(f"Processing file: {file_path}")
        file_bytes_b64 = encode_file_to_base64(file_path)
        attachment = {
            "name": os.path.basename(file_path),
            "attachmentType": "text/html",
            "contentType": "text/html",
            "contentInBase64": file_bytes_b64.decode(),
        }
        message["attachments"].append(attachment)

    logging.info(f"Sending email with {len(message['attachments'])} attachments.")
    try:
        poller = email_client.begin_send(message)
        result = poller.result()
        logging.info(f"Email sent successfully with result: {result}")
    except HttpResponseError as ex:
        logging.exception(ex)
