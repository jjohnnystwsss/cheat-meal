# Cheat Meal Picker — Claude Notes

## Zeabur Deployment

- **Project Name:** cheatmeal
- **Project ID:** `69d8e26186ea5714a4e52639`
- **Dashboard:** https://zeabur.com/projects/69d8e26186ea5714a4e52639
- **Server:** Tencent Cloud Tokyo (`69d8e1caf2ab61f5dd649fd1`) — 2 vCPU / 4 GB RAM / 60 GB SSD / $3/mo

### Services

| Service | Service ID | Environment ID | URL |
|---------|-----------|----------------|-----|
| cheatmeal (combined) | `69d8e5ef86ea5714a4e5278a` | `69d8e261474db8a99d6de7d4` | https://cheatmeal-app.zeabur.app |

### Redeploy Command

```bash
# From root directory
npx zeabur@latest deploy --project-id 69d8e26186ea5714a4e52639 --service-id 69d8e5ef86ea5714a4e5278a --json -i=false
```
