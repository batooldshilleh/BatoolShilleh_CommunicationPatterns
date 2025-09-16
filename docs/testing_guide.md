
# Testing Guide: FoodFast Platform (Terminal-Based)

## Feature 1: Customer Account Management

**Endpoints Tested:**

* `POST /api/auth/register`
* `POST /api/auth/login`
* `PUT /api/auth/update-profile/<user_id>`

---

### 1. Register a New User

**Test Steps:**

1. Open terminal and run:

```bash
curl -X POST http://localhost:5070/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser","email":"test@example.com"}'
```

2. Verify that the terminal output shows:

```json
{"message": "User registered successfully"}
```

**Screenshot Placeholder:**
![Register Terminal Screenshot](./asset/f1/image.png)

**Negative Test Case:**

* Attempt to register the same email twice:

```bash
curl -X POST http://localhost:5070/api/auth/register \
-H "Content-Type: application/json" \
-d '{"username":"testuser","email":"test@example.com"}'
```

* **Expected Result:** Terminal shows:

```json
{"message": "Email already registered"}
```

**Screenshot Placeholder:**

![Register Duplicate Terminal Screenshot](./asset/f1/image-1.png)
---

### 2. Login Existing User

**Test Steps:**

1. Run in terminal:

```bash
curl -X POST http://localhost:5070/api/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"test@example.com"}'
```

2. Verify output:

```json
{
  "message": "Login successful",
  "user_id": <actual_user_id>
}
```

**Screenshot Placeholder:**

![Login Terminal Screenshot](./asset/f1/image-2.png)
**Negative Test Case:**

* Use unregistered email:

```bash
curl -X POST http://localhost:5070/api/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"unknown@example.com"}'
```

* **Expected Result:**

```json
{"message": "Invalid credentials"}
```

**Screenshot Placeholder:**

![Login Invalid Terminal Screenshot](./asset/f1/image-3.png)
---

### 3. Update User Profile

**Test Steps:**

1. Run in terminal (replace `<user_id>` with actual ID):

```bash
curl -X PUT http://localhost:5070/api/auth/update-profile/<user_id> \
-H "Content-Type: application/json" \
```

2. Verify output:

```json
{"message": "Profile updated successfully"}
```

**Screenshot Placeholder:**
![Update Profile Terminal Screenshot](./asset/f1/image-4.png)

**Negative Test Case:**

* Use non-existent `user_id`:

```bash
curl -X PUT http://localhost:5070/api/auth/update-profile/9999 \
-H "Content-Type: application/json" \
-d '{"username":"updateduser"}'
```

* **Expected Result:** HTTP 404 Not Found

**Screenshot Placeholder:**
![Update Profile Invalid Terminal Screenshot](./asset/f1/image-5.png)
---

# Feature 2: Order Tracking

**Endpoints Tested:**

* `POST /api/restaurants`
* `POST /api/orders`
* `GET /api/orders/<order_id>/status`
* `PUT /api/orders/<order_id>/status`

---

### 1. Create a Restaurant

**Test Steps:**

1. Run in terminal:

```bash
curl -X POST http://localhost:5070/api/restaurants \
-H "Content-Type: application/json" \
-d '{"name":"Test Restaurant"}'
```

2. Expected output:

```json
{
  "message": "Restaurant created successfully",
  "restaurant_id": 1,
  "name": "Test Restaurant"
}
```

**Screenshot Placeholder:**
![Create Restaurant Terminal Screenshot](./asset/f2/image.png)

**Negative Test Case:**

* Missing name field:

```bash
curl -X POST http://localhost:5070/api/restaurants \
-H "Content-Type: application/json" \
-d '{}'
```

* **Expected Result:**

```json
{"error": "Restaurant name is required"}
```
**Screenshot Placeholder:**
![Create Restaurant Negative Test Case Terminal Screenshot](./asset/f2/image%20copy.png)

---

### 2. Create a New Order

**Test Steps:**

1. Run in terminal (replace `<user_id>` and `<restaurant_id>` with actual IDs):

```bash
curl -X POST http://localhost:5070/api/orders \
-H "Content-Type: application/json" \
-d '{"user_id":1,"restaurant_id":1}'
```

2. Expected output:

```json
{
  "message": "Order created successfully",
  "order_id": 1,
  "status": "Confirmed"
}
```

**Screenshot Placeholder:**
![Create Order Terminal Screenshot](./asset/f2/image%20copy%202.png)

**Negative Test Case:**

* Invalid user or restaurant ID:

```bash
curl -X POST http://localhost:5070/api/orders \
-H "Content-Type: application/json" \
-d '{"user_id":999,"restaurant_id":1}'
```

* **Expected Result:**

```json
{"error": "User or Restaurant not found"}
```
**Screenshot Placeholder:**
![Create Order Negative Test Case Terminal Screenshot](./asset/f2/image%20copy%203.png)

---

### 3. Get Order Status (Long Polling)

**Test Steps:**

1. Run in terminal:

```bash
curl -X GET "http://localhost:5070/api/orders/1/status?last_status=Pending"
```

2. Expected output:

```json
{"order_id": 1, "status": "Confirmed"}
```

**Screenshot Placeholder:**
![Get Order Status Terminal Screenshot](./asset/f2/image%20copy%204.png)

---

### 4. Update Order Status

**Test Steps:**

1. Run in terminal:

```bash
curl -X PUT http://localhost:5070/api/orders/1/status \
-H "Content-Type: application/json" \
-d '{"status":"Delivered"}'
```

2. Expected output:

```json
{"order_id": 1, "status": "Delivered"}
```

**Screenshot Placeholder:**
[Watch the video](./asset/f2/Screencast%20from%202025-09-16%2022-33-54.mp4)


**Negative Test Case:**

* Missing status field:

```bash
curl -X PUT http://localhost:5070/api/orders/1/status \
-H "Content-Type: application/json" \
-d '{}'
```

* **Expected Result:**

```json
{"error": "Missing status"}
```
![Update Order Status Negative Test Case Terminal Screenshot](./asset/f2/image%20copy%205.png)
---

