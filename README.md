To run the application, navigate to the project directory in your terminal and execute the following command:

```bash
streamlit run app.py
```

**Testing the changes:**

1.  **Log in or Register:** Log in with an existing member account or register a new one.
2.  **Select a Due:** Navigate to the "My Payments" tab and select an outstanding due to pay.
3.  **Upload a Payment Screenshot:** Upload a screenshot of a payment confirmation.
4.  **Observe Verification:**
    *   If the payment is rejected, expand the "OCR Debugging Info" section. You should now see more accurate detection of the Amount, VPA, and potentially a Transaction ID.
    *   If the payment is approved or sent for manual verification, it indicates the OCR successfully extracted the required information.
5.  **Check Database (Optional):** You can use a SQLite browser to inspect the `welfare.db` file and verify that the `Transaction_ID` column in the `Payment_Logs` table is being populated with the extracted transaction IDs.

These steps will help confirm that the OCR improvements are working as expected and that the transaction ID is being correctly stored.