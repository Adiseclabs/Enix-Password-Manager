# 🔐 Enix Password Manager

**Enix Password Manager v1.0.0** is a secure, lightweight, and fully local password management application designed to protect sensitive credentials using strong encryption and modern cryptographic practices.

> 🛡️ Built with security-first principles — your data never leaves your device.

---

## 🚀 Features

### 🔑 Core Security

* **AES-256 Encryption (Fernet)** — military-grade protection for stored credentials
* **PBKDF2-SHA256 Key Derivation** — brute-force resistant hashing with **390,000 iterations**
* **32-byte Random Salt per Vault** — prevents rainbow table attacks
* **Master Password Authentication** — vault remains locked until verified

---

### 💾 Data Protection

* **100% Local Storage** — no cloud, no data leaks
* **Encrypted Local Database** — all credentials stored securely on-device
* **Encrypted Backup & Restore** — export/import vaults using separate backup password (`.enixbackup`)

---

### ⚙️ Usability Features

* **Secure Password Generator** — customizable length & character sets
* **Real-Time Password Strength Meter** — visual entropy-based feedback
* **Password Visibility Toggle** — reveal/hide with one click
* **Copy to Clipboard** — instant credential copying
* **Search & Filter** — quickly find credentials by category or keyword

---

## 🧠 Security Highlights

* Strong cryptographic standards used for encryption and key derivation
* Protection against brute-force and rainbow-table attacks
* No external API calls — fully offline security model

---

## 📦 Backup & Recovery

* Export encrypted vaults securely
* Import anytime using a dedicated backup password
* Ensures safe migration and recovery

---

## ⚡ Why Enix?

* Lightweight & fast
* No internet dependency
* Privacy-focused design
* Beginner-friendly yet security-grade implementation

---

## 🛠️ Tech Stack

* Python
* Cryptography (Fernet, PBKDF2)
* Local file-based storage

---

## 📌 Version

**v1.0.0**

---

## 👨‍💻 Developer

**Aditya Bhosale**


---

## ⚠️ Disclaimer

This tool is developed for educational and personal security purposes. Always follow best practices while handling sensitive data.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!
