from datetime import datetime
from dateutil.relativedelta import relativedelta
from core import db

def get_next_due_date(last_due_date, interval_type):
    """Calculates the next due date based on the interval."""
    if interval_type == 'Weekly':
        return last_due_date + relativedelta(weeks=1)
    elif interval_type == 'Monthly':
        return last_due_date + relativedelta(months=1)
    elif interval_type == 'Quarterly':
        return last_due_date + relativedelta(months=3)
    elif interval_type == 'Yearly':
        return last_due_date + relativedelta(years=1)
    else:
        return None

def update_recurring_dues():
    """
    Processes all recurring funds to create new payment logs for the next period.
    It also compounds any unpaid amounts from the previous period.
    Returns the number of new logs created.
    """
    today = datetime.now().date()
    new_logs_created = 0
    
    recurring_funds = db.get_recurring_funds()
    all_memberships = db.get_memberships()

    for fund in recurring_funds.itertuples():
        fund_members = all_memberships[all_memberships['List_ID'] == fund.List_ID]
        
        for member in fund_members.itertuples():
            latest_log = db.get_latest_payment_log(member.User_ID, fund.List_ID)
            
            if not latest_log:
                continue

            last_due_date = datetime.strptime(latest_log['DueDate'], '%Y-%m-%d').date()
            
            # Keep generating new logs until the next due date is in the future
            while True:
                next_due_date = get_next_due_date(last_due_date, fund.Interval_Type)
                
                if not next_due_date or next_due_date > today:
                    break # Stop if we've caught up to the present

                # Check if a log for this next period already exists to prevent duplicates
                if not db.payment_log_exists(member.User_ID, fund.List_ID, next_due_date.strftime('%Y-%m-%d')):
                    
                    new_amount = fund.Amount
                    # Check if the last period's due is unpaid and compound it
                    last_log_for_compounding = db.get_latest_payment_log(member.User_ID, fund.List_ID)
                    if last_log_for_compounding and last_log_for_compounding['Status'] in ['Unpaid', 'Rejected']:
                        new_amount += last_log_for_compounding['Amount']
                    
                    # Create the new payment log for the next period
                    db.create_payment_log(
                        user_id=member.User_ID,
                        list_id=fund.List_ID,
                        amount=new_amount,
                        due_date=next_due_date.strftime('%Y-%m-%d')
                    )
                    new_logs_created += 1
                
                last_due_date = next_due_date # Move to the next period to check again

    return new_logs_created
