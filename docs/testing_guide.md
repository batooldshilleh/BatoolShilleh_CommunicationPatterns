
# FoodFast Platform - Testing Guide

## Overview
This guide explains how to test all API endpoints of Features 1, 2, and 3 using curl and WebSocket clients from the terminal. Screenshots from Postman or terminal output can be added to validate responses.

- **Server URL:** `http://127.0.0.1:5070`
- **Shared Database & Models:** All features use the same PostgreSQL database and shared `User` and `Order` models.

---

# Feature 1 - Customer Account Management

## Endpoints
- `POST /api/auth/register` → Register a new user
- `POST /api/auth/login` → User login
- `PUT /api/auth/update-profile/<user_id>` → Update user profile

### 1️⃣ Register a New User
```bash
curl -X POST http://127.0.0.1:5070/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"batool","email":"batool@example.com","password":"securepassword"}'
````

**Expected Response:**

```json
{
    "message": "User registered successfully"
}
```

### 2️⃣ Login with Registered User

```bash
curl -X POST http://127.0.0.1:5070/api/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"batool@example.com","password":"securepassword"}'
```

**Expected Response:**

```json
{
    "message": "Login successful",
    "user_id": 1
}
```

### 3️⃣ Update Profile

```bash
curl -X PUT http://127.0.0.1:5070/api/auth/update-profile/1 \
-H "Content-Type: application/json" \
-d '{"username":"batool_updated","payment_method":"Visa **** 1234"}'
```

**Expected Response:**

```json
{
    "message": "Profile updated successfully"
}
```

---

# Feature 2 - Order Tracking for Customers

## Endpoints

* `POST /api/orders` → Create a new order
* `GET /api/orders/<order_id>/status?last_status=<status>` → Check order status (long polling)
* `PUT /api/orders/<order_id>/status` → Update order status

### 1️⃣ Create a New Order

```bash
curl -X POST http://127.0.0.1:5070/api/orders \
-H "Content-Type: application/json" \
-d '{"user_id":1}'
```

**Expected Response:**

```json
{
  "message": "Order created successfully",
  "order_id": 1,
  "status": "Confirmed"
}
```

### 2️⃣ Check Order Status (Long Polling)

```bash
curl -X GET "http://127.0.0.1:5070/api/orders/1/status?last_status=Confirmed"
```

* Waits until the order status changes or times out (60 seconds).

**Expected Response Example:**

```json
{
  "order_id": 1,
  "status": "Preparing"
}
```

### 3️⃣ Update Order Status

```bash
curl -X PUT http://127.0.0.1:5070/api/orders/1/status \
-H "Content-Type: application/json" \
-d '{"status":"Preparing"}'
```

* Simulate status changes through the sequence:

```
Confirmed → Preparing → Ready → Picked up → Delivered
```

---

# Feature 3 - Driver Location Updates

## Overview

Customers can track the delivery driver's location in real-time using WebSockets.

### 3.1 Install WebSocket Client (Optional for Testing)

```bash
pip install "python-socketio[client]"
```

### 3.2 Test Driver Location Updates

Create a test client (e.g., `test_client.py`) in `implementations/feature3_driver_location`:

```python
import socketio
import time

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.on("joined")
def on_joined(data):
    print("Joined room:", data)

@sio.on("driver_location")
def on_location(data):
    print("Driver location:", data)

@sio.on("error")
def on_error(data):
    print("Error:", data)

sio.connect("http://127.0.0.1:5070")

# Customer joins room for order 1, user 1
sio.emit("join_order_room", {"order_id": 1, "user_id": 1})

# Send sample driver location updates
sio.emit("update_driver_location", {"order_id": 1, "lat": 40.7128, "lng": -74.0060})
time.sleep(5)
sio.emit("update_driver_location", {"order_id": 1, "lat": 40.7138, "lng": -74.0050})

time.sleep(10)
sio.disconnect()
```

### 3.3 Run the Test Client

```bash
cd implementations/feature3_driver_location
python test_client.py
```

* You should see messages confirming:

  * Room joined
  * Driver location updates received
* You can simulate multiple location updates to see the driver's movement.

---

## Notes

* All features share **one database** and **one Flask server**.
* Docker must be running before starting the Flask server.
* Multiple terminals can simulate multiple customers tracking orders while updating driver locations.
* Ensure order IDs and user IDs match created entries.
* Screenshots can be added from Postman, terminal outputs, or WebSocket client logs.

---

End of Testing Guide for Features 1, 2 & 3
