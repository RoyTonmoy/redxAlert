from sqlite3 import connect
import mysql.connector
from dotenv import load_dotenv
import os
import automate_alert
from datetime import date
from datetime import timedelta

# loading env file
load_dotenv()

# creating connection with MySql database
connection = mysql.connector.connect(
    host = os.environ.get('prodHost'),
    user = os.environ.get('prodUser'),
    password = os.environ.get('prodPassword')
)

# alert function to check the action
def createAlert(action):
    print(action + " cron has been started")
    query = "SELECT COUNT(id) as count, shop_id, (SELECT shop_name from shopuplite.sl_shops where id = shop_id) as shop_name FROM shopuplite.sl_logistics_shop_audit_log where created_at BETWEEN %s and %s AND action=%s group by shop_id order by created_at desc;"

    endDate = date.today()
    startDate = endDate - timedelta(days=7)
    

    print(startDate)
    print(endDate)

    mycursor = connection.cursor()
    mycursor.execute(query, (startDate, endDate, action))
    myresult = mycursor.fetchall()

    # specify channel name
    channelName = "#redx-ffrm-alert"

    for x in range(0,len(myresult)):
        for i in myresult:
            if myresult[x][0] > 2:
                print(f"This shop id {myresult[x][1]} performed action={action} more than twice")
                alertText = "Shop ID: "+ str(myresult[x][1])+ "\nShop Name: "+str(myresult[x][2])+ "\n Following action="+ action +" has been performed more than twice"
                automate_alert.sendAlertMessage(alertText, channelName)
            else:
                print("no issue " + action)
            break
    print(action+" cron has been finished")

bkashNoAction = 'BKASH_NUMBER_CHANGED'
branchIdAction = 'BRANCH_ID_CHANGED'
branchNameAction = 'BRANCH_NAME_CHANGED'
bankNameChangeAction = 'BANK_NAME_CHANGED'
bankIdChangeAction = 'BANK_ID_CHANGED'
disbursmentBankAction = 'DISBURSEMENT_BANK_CHANGED'
merchantTypeAction = 'MERCHANT_TYPE_CHANGED'
paymentMethodchangeAction = 'PAYMENT_METHOD_CHANGED'
paymentTypeChangeAction = 'PAYMENT_TYPE_CHANGED'


def callAlert():
    createAlert(bkashNoAction)
    createAlert(branchIdAction)
    createAlert(branchNameAction)
    createAlert(bankNameChangeAction)
    createAlert(bankIdChangeAction)
    createAlert(disbursmentBankAction)
    createAlert(merchantTypeAction)
    createAlert(paymentMethodchangeAction)
    createAlert(paymentTypeChangeAction)

callAlert()

# schedule.every(180).minutes.do(callAlert)
# schedule.every().day.at("00:00").do(callAlert)
# schedule.every().day.at("17:05").do(callAlert)


# while True:
#     schedule.run_pending()
#     time.sleep(1)