# Welcome to RipaPay, a NEXTGEN Payments infrustructure powered by the QUBIC Blockchain, meant to revolutionize payments in Africa and Beyond!

## Project info

**URL**: https://ripapay.netlify.app/

## How can I edit this code?

There are several ways of editing your application.

**Use Lovable**

Simply visit https://ripapay.netlify.app/ and join the waitlist.

Successful Changes made on the codebase will be committed automatically to this repo.

**Use your preferred IDE**

If you want to work locally using your own IDE, you can clone this repo and push changes. Pushed changes will also be reflected in Lovable.

The only requirement is having Node.js & npm installed - [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)

Follow these steps:

```sh
# Step 1: Clone the repository using the project's Git URL.
git clone <YOUR_GIT_URL>

# Step 2: Navigate to the project directory.
cd <YOUR_PROJECT_NAME>

# Step 3: Install the necessary dependencies.
npm i

# Step 4: Start the development server with auto-reloading and an instant preview.
npm run dev
```

**Edit a file directly in GitHub**

- Navigate to the desired file(s).
- Click the "Edit" button (pencil icon) at the top right of the file view.
- Make your changes and commit the changes.

**Use GitHub Codespaces**

- 

## What technologies are used for this project?

This project is built with .

- Vite
- TypeScript
- React
- shadcn-ui
- Tailwind CSS

## API Endpoints

### Business Registration Endpoints
- `POST /business/register` - Register a new business and receive an 8-digit business UUID
- `GET /business/{uuid}` - Get business details by UUID (8-digit format)

### Analytics & Reporting Endpoints
- `GET /analytics/transactions/{business_uuid}` - Get comprehensive transaction analytics (8-digit UUID)
- `POST /analytics/export` - Export transaction data in CSV or JSON format
- `GET /analytics/customer-insights/{business_uuid}` - Get customer behavior analytics (8-digit UUID)
- `GET /analytics/growth-metrics/{business_uuid}` - Get business growth analytics (8-digit UUID)

### UUID Format
All business UUIDs in the system follow an 8-digit numeric format:
- Example: 16789045
- First 6 digits: Timestamp-based
- Last 2 digits: Random for uniqueness

### Wallet Endpoints
- `POST /wallet/connect` - Connect to Qubic wallet
- `POST /wallet/balance` - Get wallet balance
- `POST /wallet/transactions` - Get wallet transaction history

### Dashboard Endpoints
- `GET /dashboard/metrics/{business_uuid}` - Get business dashboard metrics
- `GET /dashboard/transactions/{business_uuid}` - Get business transaction monitoring

### Payment Endpoints
- `POST /transactions` - Create a new transaction
- `POST /qr/generate` - Generate QR code for payment
- `POST /qr/verify` - Verify QR payment data
- `POST /payment/link` - Generate payment link

### System Endpoints
- `GET /` - API root endpoint
- `GET /health` - System health check

### Account Management Endpoints
- `POST /accounts/create` - Create a new account with mnemonic
- `GET /accounts/{address}` - Get account details
- `POST /accounts/backup` - Backup account data
- `POST /accounts/restore` - Restore account from backup
- `POST /accounts/cloud-integration` - Integrate account with cloud storage (Google Drive)

### Transaction Tracking Endpoints
- `GET /transactions/inbound` - Get inbound transactions for an address
- `GET /transactions/outbound` - Get outbound transactions for an address
- `GET /transactions/{transaction_id}` - Get detailed transaction information

### B2B Payment Endpoints
- `POST /b2b/transfer` - Execute business-to-business transfer
- `GET /b2b/supported-chains` - Get list of supported blockchain networks
- `POST /b2b/register-chain` - Register new blockchain network for B2B transfers

All endpoints return JSON responses and include proper error handling. For detailed API documentation, visit our [API Documentation](https://ripapay.netlify.app/api-docs).

## How can I deploy this project?

