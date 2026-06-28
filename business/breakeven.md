# breakeven.md

## Unit Economics & Break-even Analysis for HTTP-Audit

### Cost per Active User
- **Compute Costs**: $0.10/user/month (based on average cloud compute pricing for monitoring tools)
- **Storage Costs**: $0.05/user/month (average storage cost for logs and data retention)
- **Bandwidth Costs**: $0.02/user/month (average data transfer cost for HTTP interactions)

**Total Cost per Active User**:  
**$0.10 + $0.05 + $0.02 = $0.17/user/month**

---

### Pricing Tiers
1. **Basic Tier**: $5/month
   - Features: Basic HTTP monitoring, anomaly detection alerts, 1 GB log storage, email support.
  
2. **Pro Tier**: $15/month
   - Features: Advanced monitoring, real-time alerts, 5 GB log storage, priority email support, integration with SIEM tools.
  
3. **Enterprise Tier**: $50/month
   - Features: Comprehensive monitoring, custom anomaly detection rules, 20 GB log storage, dedicated account manager, SLA support.

---

### Customer Acquisition Cost (CAC) Range
- **CAC Estimate**: $20 - $50 per user (includes marketing, sales, and onboarding costs)

---

### Lifetime Value (LTV) Estimate
- **Average Revenue per User (ARPU)**: 
  - Basic Tier: $5/month
  - Pro Tier: $15/month
  - Enterprise Tier: $50/month
- **Average Customer Lifespan**: 24 months (based on industry average for SaaS)
  
**LTV Calculation**:
- Basic Tier: $5 * 24 = $120
- Pro Tier: $15 * 24 = $360
- Enterprise Tier: $50 * 24 = $1200

---

### Break-even Users Count
- **Total Monthly Costs**: $1,700 (fixed costs including development, support, and overhead)
  
**Break-even Calculation**:
- Break-even Users = Total Monthly Costs / (Price per User - Cost per Active User)
  
1. Basic Tier:  
   Break-even Users = $1,700 / ($5 - $0.17) = 360 users

2. Pro Tier:  
   Break-even Users = $1,700 / ($15 - $0.17) = 115 users

3. Enterprise Tier:  
   Break-even Users = $1,700 / ($50 - $0.17) = 34 users

---

### Path to $10K MRR
- **Target Monthly Recurring Revenue (MRR)**: $10,000

**Required Users Calculation**:
1. Basic Tier:  
   Users Needed = $10,000 / $5 = 2,000 users

2. Pro Tier:  
   Users Needed = $10,000 / $15 = 667 users

3. Enterprise Tier:  
   Users Needed = $10,000 / $50 = 200 users

**Optimal Path**:  
To achieve $10K MRR, focus on the Pro Tier with 667 users or the Enterprise Tier with 200 users, as they provide higher revenue per user and lower break-even points.