# 🚀 EVOLANCE DEPLOYMENT GUIDE

## 📋 **DEPLOYMENT OPTIONS**

### 1. **Docker Compose (Local/Server)**
```bash
# Clone repository
git clone <your-repo>
cd evolancewebapp

# Set environment variables
cp .env.production.example .env.production
# Edit .env.production with your values

# Deploy
chmod +x deploy.sh
./deploy.sh
```

### 2. **AWS Deployment**

#### **Option A: AWS ECS (Recommended)**
```bash
# Install AWS CLI and configure
aws configure

# Create ECS cluster
aws ecs create-cluster --cluster-name evolance-cluster

# Deploy using AWS CLI
aws ecs create-service \
  --cluster evolance-cluster \
  --service-name evolance-service \
  --task-definition evolance-task \
  --desired-count 2
```

#### **Option B: AWS EC2**
```bash
# Launch EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name your-key-pair

# SSH and deploy
ssh -i your-key.pem ubuntu@your-instance-ip
git clone <your-repo>
cd evolancewebapp
./deploy.sh
```

### 3. **Google Cloud Platform**

#### **Option A: GKE (Kubernetes)**
```bash
# Create GKE cluster
gcloud container clusters create evolance-cluster \
  --zone us-central1-a \
  --num-nodes 3

# Deploy to GKE
kubectl apply -f kubernetes/
```

#### **Option B: Cloud Run**
```bash
# Deploy backend
gcloud run deploy evolance-backend \
  --source ./backend \
  --platform managed \
  --region us-central1

# Deploy frontend
gcloud run deploy evolance-frontend \
  --source ./frontend \
  --platform managed \
  --region us-central1
```

### 4. **Azure Deployment**

#### **Option A: Azure Container Instances**
```bash
# Create resource group
az group create --name evolance-rg --location eastus

# Deploy containers
az container create \
  --resource-group evolance-rg \
  --name evolance-backend \
  --image your-registry/evolance-backend:latest
```

#### **Option B: Azure Kubernetes Service**
```bash
# Create AKS cluster
az aks create \
  --resource-group evolance-rg \
  --name evolance-aks \
  --node-count 3

# Deploy to AKS
kubectl apply -f kubernetes/
```

### 5. **DigitalOcean**

#### **Option A: DigitalOcean App Platform**
```bash
# Install doctl
brew install doctl

# Deploy using App Platform
doctl apps create --spec app.yaml
```

#### **Option B: DigitalOcean Droplets**
```bash
# Create droplet
doctl compute droplet create evolance \
  --size s-2vcpu-4gb \
  --image ubuntu-20-04-x64 \
  --ssh-keys your-ssh-key

# SSH and deploy
ssh root@your-droplet-ip
git clone <your-repo>
cd evolancewebapp
./deploy.sh
```

### 6. **Heroku**
```bash
# Install Heroku CLI
brew install heroku

# Login to Heroku
heroku login

# Create apps
heroku create evolance-backend
heroku create evolance-frontend

# Deploy
git push heroku main
```

---

## 🔧 **ENVIRONMENT SETUP**

### **Required Environment Variables**
```bash
# MongoDB
MONGO_URL=mongodb+srv://waitlist:unumau@evolance-waitlist.oy1zgcg.mongodb.net/
DB_NAME=evolance_webapp

# AI Services
GEMINI_API_KEY=your-gemini-api-key

# Security
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# URLs
BACKEND_URL=https://api.evolance.com
FRONTEND_URL=https://evolance.com
```

### **SSL Certificate Setup**
```bash
# Using Let's Encrypt
sudo certbot --nginx -d evolance.com -d www.evolance.com

# Using Cloudflare (recommended)
# 1. Add domain to Cloudflare
# 2. Set SSL/TLS to "Full (strict)"
# 3. Enable "Always Use HTTPS"
```

---

## 📊 **MONITORING & LOGGING**

### **Prometheus Configuration**
```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'evolance-backend'
    static_configs:
      - targets: ['backend:8000']

  - job_name: 'evolance-frontend'
    static_configs:
      - targets: ['frontend:3000']
```

### **Grafana Dashboards**
- **System Metrics:** CPU, Memory, Disk usage
- **Application Metrics:** Request rate, response time, error rate
- **AI Metrics:** Gemini API usage, model training progress
- **User Metrics:** Active users, chat sessions, emolytics updates

---

## 🔒 **SECURITY CHECKLIST**

- [ ] **SSL/TLS:** HTTPS enabled with valid certificates
- [ ] **Environment Variables:** All secrets properly configured
- [ ] **Rate Limiting:** API endpoints protected
- [ ] **CORS:** Properly configured for production domains
- [ ] **Database:** MongoDB Atlas with proper access controls
- [ ] **Monitoring:** Logs and metrics collection enabled
- [ ] **Backup:** Database backup strategy implemented
- [ ] **Updates:** Automated security updates enabled

---

## 🚀 **DEPLOYMENT STEPS**

### **Pre-Deployment**
1. **Code Review:** Ensure all features are tested
2. **Environment Setup:** Configure production environment variables
3. **Database Migration:** Ensure MongoDB schema is up to date
4. **SSL Certificates:** Obtain and configure SSL certificates
5. **Domain Setup:** Configure DNS records

### **Deployment**
1. **Build Images:** Create production Docker images
2. **Deploy Services:** Start all services with proper configuration
3. **Health Checks:** Verify all services are running
4. **SSL Setup:** Configure HTTPS and redirects
5. **Monitoring:** Enable logging and monitoring

### **Post-Deployment**
1. **Testing:** Verify all features work in production
2. **Performance:** Monitor system performance
3. **Security:** Run security scans
4. **Backup:** Test backup and recovery procedures
5. **Documentation:** Update deployment documentation

---

## 📞 **SUPPORT & TROUBLESHOOTING**

### **Common Issues**
1. **Database Connection:** Check MongoDB Atlas network access
2. **SSL Errors:** Verify certificate configuration
3. **Memory Issues:** Monitor container resource usage
4. **API Rate Limits:** Check Gemini API quotas

### **Emergency Procedures**
1. **Rollback:** `docker-compose down && git checkout previous-version`
2. **Database Recovery:** Restore from MongoDB Atlas backups
3. **Service Restart:** `docker-compose restart service-name`

---

**Ready to deploy! Choose your preferred platform and follow the guide above.** 🎯 