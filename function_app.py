import logging
import azure.functions as func
import feed_collector
import email_dispatcher

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 8 * * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Executing python timer trigger function.")
    files = feed_collector.collect()
    email_dispatcher.send_email(files)
    logging.info("Python timer trigger function executed.")
