## SOX-EINvoicing App

The **SOX-EINvoicing App** is a simple end‑to‑end electronic invoicing system.  
It consists of:

- **Backend API** (`se2021-23t1-einvoicing-api-h13a-sox-sending-api`): Python service that exposes endpoints for creating, sending, storing, authenticating, and reporting on invoices.
- **Frontend UI** (`se2021-23t1-einvoicing-frontend-h13a-sox-sending-api`): React single‑page application for users to log in, create invoices, send them, view inbox/storage, and see confirmations.

The typical flow is:

1. User logs in via the frontend.
2. User creates or selects an invoice.
3. The frontend calls the backend API to send, authenticate, store, or delete invoices.
4. The backend persists data and returns status information to be displayed in the UI.

---

## Repository Structure

- `se2021-23t1-einvoicing-api-h13a-sox-sending-api/` – Python backend service
  - `src/` – application code (`server`, `send_invoice`, `attach_invoice`, `generate_report`, etc.)
  - `tests/` – unit/integration tests for the API
  - `README.md` – backend‑specific usage instructions
- `se2021-23t1-einvoicing-frontend-h13a-sox-sending-api/` – React frontend
  - `src/components/` – views such as `Login`, `Home`, `CreateInvoice`, `SendInvoice`, `Inbox`, `InvoiceStorage`, etc.
  - `README.md` – standard Create React App documentation

---

## Prerequisites

- **Backend**
  - Python 3.9+ (Python 3.10/3.11 also work based on compiled bytecode)
  - `pip` for installing dependencies

- **Frontend**
  - Node.js (LTS) and npm

---

## Backend Setup & Usage

Change into the backend directory:

```bash
cd se2021-23t1-einvoicing-api-h13a-sox-sending-api
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the API server

```bash
python3 -m src.server
```

By default, the server listens on **port 9090**:

- Base URL: `http://localhost:9090/`

You can confirm or change this in `src/config.py`.

### Run backend tests

See the backend `README.md` for full details, but in short:

```bash
# Terminal 1 – start server
python3 -m src.server

# Terminal 2 – run pytest
python3 -m pytest path/to/test_file.py
```

The backend README also documents coverage and linting commands.

---

## Frontend Setup & Usage

Change into the frontend directory:

```bash
cd se2021-23t1-einvoicing-frontend-h13a-sox-sending-api
```

### Install dependencies

```bash
npm install
```

### Start the development server

```bash
npm start
```

This runs the React app on **http://localhost:3000** (default for Create React App).  
Ensure the backend is running on `http://localhost:9090` so the UI can communicate with the API.

### Frontend tests & builds

Standard Create React App scripts are available:

- `npm test` – run unit tests in watch mode
- `npm run build` – production build into the `build` folder

Refer to the frontend `README.md` for more CRA‑specific information.

---

## Typical Development Workflow

1. **Start backend**  
   - From the backend directory: `python3 -m src.server`
2. **Start frontend**  
   - From the frontend directory: `npm start`
3. **Develop features**  
   - Modify backend endpoints under `src/` or React components under `src/components/`.
4. **Run tests**  
   - Backend: `python3 -m pytest ...`  
   - Frontend: `npm test`

---

## Notes

- Both subprojects have their own `.gitignore` and configuration; consult each sub‑README for deeper details.
- The backend exposes its endpoints and sample documentation via `src/static/swagger.yaml`, which you can use as reference when integrating or extending the API.

