# Setup dev environment with conda

```bash
conda create --name ne-one-automate python=3.9
conda activate ne-one-automate
pip install -r requirements.txt
pip install -r requirements-dev.txt
docker compose up -d
```

# Configure BING API key

```
edit app/config.py
```

# Overview endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | /dashboard | Return metrics for the dashboard view |
| GET | /change-requests | Return list of all (filtered) change requests |
| GET | /change-requests/{id} | Return a change request |
| POST | /change-requests/{id}/approve | Approve change request |
| GET | /rules | Return list of all rules |
| GET | /rules/{id} | Return a rule |
| POST | /rules | Create a new rule |
| PUT | /rules/{id} | Update a rule |
| DELETE | /rules/{id} | Delete a rule |

