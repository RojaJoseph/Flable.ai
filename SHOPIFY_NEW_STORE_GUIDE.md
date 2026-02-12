# 🛍️ SHOPIFY SETUP - Quick Guide for New Store

## Your Situation:
- ✅ New Shopify store created
- ✅ Client ID and Secret in .env
- ❓ Want to see analytics

---

## 📋 Step-by-Step Guide (10 Minutes)

### STEP 1: Connect Your Store (3 min)

1. **Make sure credentials are in .env:**
   ```
   Open: F:\flable.ai\backend\.env
   
   Check these lines are filled:
   SHOPIFY_CLIENT_ID=your_actual_id
   SHOPIFY_CLIENT_SECRET=your_actual_secret
   ```

2. **Set Redirect URI in Shopify Partners:**
   ```
   Go to: https://partners.shopify.com
   → Click your app
   → App setup
   → Allowed redirection URL(s)
   → Add: http://localhost:8000/api/v1/integrations/shopify/callback
   → Save
   ```

3. **Restart backend:**
   ```bash
   # Stop (Ctrl+C), then:
   cd F:\flable.ai\backend
   venv\Scripts\activate
   python -m uvicorn main:app --reload
   ```

4. **Connect via UI:**
   ```
   Go to: http://localhost:3000/integrations
   Click: "Connect Shopify"
   Enter: your-store-name (without .myshopify.com)
   Approve on Shopify
   Done! ✅
   ```

---

### STEP 2: Add Sample Data (5 min)

**Your store is empty, so add test data:**

#### Option A: Via Shopify Admin (Easiest)

1. **Go to your store admin:**
   ```
   https://your-store-name.myshopify.com/admin
   ```

2. **Add 3 Products:**
   ```
   Products → Add product
   
   Product 1:
   - Title: "Wireless Headphones"
   - Price: $79.99
   - Save
   
   Product 2:
   - Title: "Smart Watch"
   - Price: $199.99
   - Save
   
   Product 3:
   - Title: "Phone Case"
   - Price: $24.99
   - Save
   ```

3. **Create 2 Test Orders:**
   ```
   Orders → Create order
   
   Order 1:
   - Add "Wireless Headphones"
   - Customer: test@example.com
   - Mark as paid
   - Create order
   
   Order 2:
   - Add "Smart Watch"
   - Customer: john@example.com
   - Mark as paid
   - Create order
   ```

#### Option B: Use Sample Data Import

Shopify can add sample products automatically:
```
Settings → Files → Import products
Or search for "Add sample products" in Shopify Admin
```

---

### STEP 3: Test Connection (2 min)

Run the test script I created:

```bash
cd F:\flable.ai\backend
venv\Scripts\activate
python test_shopify.py
```

This will show:
- ✅ If connection works
- 📦 How many products you have
- 🛒 How many orders you have
- 👥 How many customers you have

---

### STEP 4: Sync Data to Flable.ai (1 min)

1. **Go to integrations:**
   ```
   http://localhost:3000/integrations
   ```

2. **Click "Sync Now"** on your Shopify connection

3. **Wait 10-30 seconds**

4. **Refresh page** - You'll see:
   - Products count
   - Orders count
   - Revenue total

---

### STEP 5: View Analytics (1 min)

1. **Go to analytics:**
   ```
   http://localhost:3000/analytics
   ```

2. **You'll see:**
   - Revenue charts
   - Product performance
   - Order trends
   - Customer data

---

## 🎯 What You'll See

### If Store is Empty:
```
Products: 0
Orders: 0
Revenue: $0
Analytics: No data to display
```
**Solution:** Add products and orders (Step 2)

### If Store Has Data:
```
Products: 3
Orders: 2
Revenue: $279.98
Analytics: Charts showing trends
```
**Perfect!** ✅

---

## 🧪 Quick Test Commands

After connecting, test everything:

```bash
# Test 1: Check connection
cd backend
python test_shopify.py

# Test 2: Check API directly
curl http://localhost:8000/api/v1/integrations

# Test 3: Sync data
# Go to http://localhost:3000/integrations
# Click "Sync Now"
```

---

## 📊 Analytics Timeline

**Immediate (after sync):**
- ✅ Products list
- ✅ Orders count
- ✅ Revenue total

**After campaigns run:**
- 📈 Campaign performance
- 🎯 ROI calculations
- 📊 Attribution data

**After 1 month:**
- 📈 Trend analysis
- 📊 Growth charts
- 🎯 Predictions

---

## ⚠️ Common Issues

### Issue 1: "No integration found"
**Solution:** Connect store via UI first
```
http://localhost:3000/integrations → Connect Shopify
```

### Issue 2: "Invalid credentials"
**Solution:** Check .env file has correct Client ID and Secret

### Issue 3: "No data showing"
**Solution:** Add products and orders in Shopify Admin, then sync

### Issue 4: "Redirect URI mismatch"
**Solution:** In Shopify Partners, set exact URL:
```
http://localhost:8000/api/v1/integrations/shopify/callback
```

---

## 🎯 Your Next Steps

**Right Now (10 min):**
1. ✅ Connect store (Step 1)
2. ✅ Add 3 products (Step 2)
3. ✅ Create 2 test orders (Step 2)
4. ✅ Run test script (Step 3)
5. ✅ Sync data (Step 4)
6. ✅ View analytics (Step 5)

**This Week:**
- Add real products
- Start marketing
- Get real customers
- Track campaigns

**This Month:**
- Analyze trends
- Optimize campaigns
- Scale up

---

## 💡 Pro Tips

1. **Use Shopify's test mode** for development
2. **Mark test orders as paid** to see them in analytics
3. **Add varied data** to see different chart types
4. **Sync regularly** to keep data fresh
5. **Check logs** if sync fails

---

## 🚀 Ready?

Run this NOW:

```bash
# Terminal 1: Make sure backend is running
cd F:\flable.ai\backend
venv\Scripts\activate
python -m uvicorn main:app --reload

# Terminal 2: Test connection
cd F:\flable.ai\backend
venv\Scripts\activate
python test_shopify.py

# Browser:
http://localhost:3000/integrations
→ Connect Shopify
→ Sync Now
→ View Analytics!
```

---

**Let me know when you've connected and I'll help you with analytics!** 🎉
