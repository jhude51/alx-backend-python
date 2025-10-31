# 🧩 0. Getting started with python generators

This script (`seed.py`) initializes the **PostgreSQL** database `ALX_prodev`, creates the `user_data` table, and efficiently populates it with data from a CSV file using **Python generators** for memory-efficient processing.

---

## 🚀 Features
- Automatically creates the database and table (if not existing)
- Streams data from `user_data.csv` instead of loading it all at once
- Inserts rows individually and skips duplicates using `ON CONFLICT (email) DO NOTHING`
- Uses UUIDs for globally unique user IDs

---

## ⚙️ Setup Instructions

1. **Install dependencies**
   ```bash
   pip install psycopg2-binary
   ```

## 🧠 About Generators

This script uses a **Python generator** to process CSV data efficiently.  
Instead of loading the entire file into memory at once, a generator reads and yields **one row at a time** — greatly improving performance and reducing memory usage.

In large-scale applications, this approach helps maintain consistent memory consumption even when dealing with thousands of records.  
Each row is read → transformed → inserted → and then discarded from memory.

### ⚡ Why It Matters
- **Efficient:** Handles large CSV files without memory spikes.  
- **Scalable:** Suitable for production data imports.  
- **Simple:** Uses Python’s `yield` to stream data seamlessly.

---

## ✅ Example Output
- ✅ Connected to 'ALX_prodev' database successfully.
- ✅ Table 'user_data' created or already exists.
- ✅ Inserted 5 new rows from 'user_data.csv' (streamed).
- 🎉 Data seeding complete (using generators).
---
## 💡 Key Benefits
| Feature | Benefit |
|----------|----------|
| **Memory Efficiency** | Streams rows using generators |
| **Scalability** | Handles large files efficiently |
| **Idempotent Inserts** | Prevents duplicate data |
| **Production-Ready** | Clean, modular, and safe seeding workflow |

---