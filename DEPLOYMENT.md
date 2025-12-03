# 🚀 Guía de Despliegue - CI/CD

Esta guía explica cómo configurar el despliegue automático del proyecto LaborDoc.

## 📋 Estrategia de Ramas

- **`main`** → Producción (automático)
- **`develop`** → Desarrollo (automático)
- **Feature branches** → Pull Request a `develop`

## 🔧 Configuración Inicial

### 1. Secrets de GitHub

Ve a: `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

#### Para Producción:
```
PROD_SSH_KEY         # Clave privada SSH del servidor de producción
PROD_SERVER_HOST     # IP o dominio del servidor (ej: prod.labordoc.com)
PROD_SERVER_USER     # Usuario SSH (ej: ubuntu, root)
```

#### Para Desarrollo:
```
DEV_SSH_KEY          # Clave privada SSH del servidor de desarrollo
DEV_SERVER_HOST      # IP o dominio del servidor (ej: dev.labordoc.com)
DEV_SERVER_USER      # Usuario SSH (ej: ubuntu)
```

#### Para Docker (opcional):
```
DOCKER_USERNAME      # Usuario de Docker Hub
DOCKER_PASSWORD      # Contraseña o token de Docker Hub
```

### 2. Generar SSH Keys

```bash
# En tu máquina local
ssh-keygen -t rsa -b 4096 -C "labordoc-deploy" -f ~/.ssh/labordoc_deploy

# Copiar clave pública al servidor
ssh-copy-id -i ~/.ssh/labordoc_deploy.pub user@servidor.com

# Copiar clave privada a GitHub Secrets
cat ~/.ssh/labordoc_deploy
# Copia todo el contenido (incluyendo BEGIN/END) y pégalo en GitHub Secrets
```

## 🐳 Opciones de Despliegue

### Opción 1: Servidor VPS (Ubuntu/Debian)

#### Preparación del Servidor

```bash
# Conectar al servidor
ssh user@servidor.com

# Instalar dependencias
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx

# Crear directorios
sudo mkdir -p /var/www/labordoc-prod/{backend,frontend}
sudo mkdir -p /var/www/labordoc-dev/{backend,frontend}
sudo chown -R $USER:$USER /var/www/labordoc-*

# Configurar entorno virtual para producción
cd /var/www/labordoc-prod/backend
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn pydantic

# Crear servicio systemd para backend
sudo nano /etc/systemd/system/labordoc-backend.service
```

**Contenido de `labordoc-backend.service`:**
```ini
[Unit]
Description=LaborDoc Backend API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/var/www/labordoc-prod/backend
Environment="PATH=/var/www/labordoc-prod/backend/venv/bin"
ExecStart=/var/www/labordoc-prod/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Habilitar y arrancar servicio
sudo systemctl daemon-reload
sudo systemctl enable labordoc-backend
sudo systemctl start labordoc-backend
```

**Configurar Nginx:**
```bash
sudo nano /etc/nginx/sites-available/labordoc-prod
```

```nginx
server {
    listen 80;
    server_name labordoc.com www.labordoc.com;

    # Frontend
    location / {
        root /var/www/labordoc-prod/frontend;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

```bash
# Activar sitio
sudo ln -s /etc/nginx/sites-available/labordoc-prod /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Opción 2: Docker + Docker Compose

```bash
# En el servidor
cd /opt
git clone https://github.com/devpfan/LaborDoc.git
cd LaborDoc

# Producción
docker-compose -f docker-compose.prod.yml up -d

# Desarrollo
docker-compose -f docker-compose.dev.yml up -d
```

### Opción 3: Plataformas Cloud

#### Heroku
```bash
# Instalar Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login
heroku login

# Crear apps
heroku create labordoc-prod
heroku create labordoc-dev

# Desplegar
git push heroku main:main           # A producción
git push heroku develop:main        # A desarrollo
```

#### Railway
1. Conecta tu repo de GitHub
2. Crea dos proyectos: `labordoc-prod` y `labordoc-dev`
3. Configura variables de entorno
4. Railway detectará automáticamente los Dockerfiles

#### Vercel (Solo Frontend)
```bash
# Instalar Vercel CLI
npm i -g vercel

cd frontend
vercel --prod    # Para producción desde main
vercel           # Para preview desde develop
```

## 🔄 Workflow de Desarrollo

```bash
# 1. Crear feature branch
git checkout develop
git pull
git checkout -b feature/nueva-funcionalidad

# 2. Hacer cambios y commit
git add .
git commit -m "feat: agregar nueva funcionalidad"

# 3. Push a GitHub
git push origin feature/nueva-funcionalidad

# 4. Crear Pull Request a develop
# (En GitHub UI)

# 5. Después de merge, develop se despliega automáticamente a DEV

# 6. Cuando esté listo para producción
git checkout main
git pull
git merge develop
git push origin main

# 7. main se despliega automáticamente a PROD
```

## 📊 Monitoreo del Despliegue

### Ver logs de GitHub Actions
1. Ve a tu repositorio en GitHub
2. Pestaña `Actions`
3. Selecciona el workflow que corrió
4. Ver logs detallados de cada step

### Ver logs en el servidor
```bash
# Logs del backend
sudo journalctl -u labordoc-backend -f

# Logs de nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Logs de Docker
docker logs -f labordoc-backend-prod
docker logs -f labordoc-frontend-prod
```

## 🧪 Probar Localmente con Docker

```bash
# Build y run
docker-compose -f docker-compose.dev.yml up --build

# Acceder
# Frontend: http://localhost:4200
# Backend: http://localhost:8001
```

## 🔒 Consideraciones de Seguridad

1. **Usar HTTPS** con Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d labordoc.com -d www.labordoc.com
```

2. **Variables de entorno**: Nunca commitear `.env` files
3. **Secrets**: Usar GitHub Secrets para credenciales
4. **Firewall**: Configurar UFW
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## 📝 Comandos Útiles

```bash
# Verificar estado del despliegue
systemctl status labordoc-backend
docker ps
nginx -t

# Reiniciar servicios
sudo systemctl restart labordoc-backend
sudo systemctl restart nginx
docker-compose -f docker-compose.prod.yml restart

# Ver recursos
htop
docker stats
```

## 🆘 Troubleshooting

### Error: "Permission denied" en SSH
```bash
# Verificar permisos de la clave
chmod 600 ~/.ssh/labordoc_deploy
```

### Error: "Port already in use"
```bash
# Encontrar proceso usando el puerto
sudo lsof -i :8000
sudo kill -9 <PID>
```

### Error en build de Docker
```bash
# Limpiar caché de Docker
docker system prune -a
docker-compose -f docker-compose.prod.yml build --no-cache
```

## 🎯 Roadmap de Mejoras

- [ ] Agregar tests automatizados
- [ ] Configurar rollback automático en caso de fallo
- [ ] Implementar blue-green deployment
- [ ] Agregar monitoring con Prometheus/Grafana
- [ ] Configurar alertas en Slack/Discord
- [ ] Implementar database migrations automáticas

---

**¡Tu pipeline de CI/CD está listo! 🎉**
