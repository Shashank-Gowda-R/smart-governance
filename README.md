# Blockchain Model for Smart Governance using Logistic Regression, Solidity, and Polygon Testnet

## Overview
This project aims to develop a blockchain model for smart governance, incorporating logistic regression, Solidity, and the Polygon testnet. The model facilitates transparent and efficient resource allocation by leveraging advanced technologies and machine learning algorithms.

### Project Components
- **Citizen Interface**: Allows citizens to create accounts, apply for schemes or loans, and receive notifications.
- **Government ML Model**: Utilizes logistic regression to assess citizen eligibility for schemes or loans.
- **Blockchain**: Provides a secure and transparent ledger for storing and tracking all transactions.

### Workflow
1. Citizen creates an account and enters basic details.
2. Account creation triggers blockchain account creation and notification to the citizen.
3. Citizen applies for schemes or loans.
4. Government ML model assesses citizen eligibility.
5. If eligible, citizen is granted the scheme or loan.
6. Blockchain is updated to reflect the transaction.
7. Citizen receives confirmation of grant or loan.

## Loan Application Process
This project includes a loan application process with the following steps:
1. **User Logged In**: Applicant is logged into the system.
2. **Grant Application Completed**: Applicant completes the loan application form.
3. **List of User Validation**: System performs eligibility checks.
4. **Admin Logged In**: Authorized administrator reviews the application.
5. **Decision Point (Grant/Failure)**: Application is approved or rejected.
   - If granted:
     - **Get Score and Max Credit**: System retrieves credit score and determines maximum loan amount.
     - **Loan Avail Requested Loan Amount**: Applicant selects loan amount within approved limit.
     - **Grant Success**: Loan is disbursed to applicant.
   - If failed: Process ends with a "Grant Failure" outcome.

## Features
- **Login System**: Users can sign up for accounts and log in securely.
- **Payment Methods**: Multiple payment methods are supported, including username, phone number, bank transfer, and QR code.
- **Loan Management**: Citizens can apply for and repay loans, with eligibility and credit checks performed using logistic regression.
- **Admin Panel**: Admins can monitor earnings, disburse grants, and manage the system.

## Usage
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up environment variables for Twilio credentials and database connection.
4. Run the Flask server using `python server.py`.
5. Access the application through the provided URL.

## Dependencies
- Flask
- Flask SQLAlchemy
- Flask Login
- Twilio
- Forex Python

## Configuration
- Set up Twilio account credentials in the environment variables: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`.
- Configure the database connection URI in the Flask application.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request with any enhancements or bug fixes.
<!-- 
## License
[MIT License](LICENSE) -->
