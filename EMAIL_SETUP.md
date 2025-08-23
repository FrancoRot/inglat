# Configuración del Sistema de Email - INGLAT

## Problema Identificado

El error "Hubo un problema al enviar el formulario" se debe principalmente a que la configuración de email no está completa, especialmente la variable `EMAIL_HOST_PASSWORD` que está vacía.

## Soluciones Implementadas

### 1. Mejoras en el Código

- **Vista de Contacto Mejorada**: Ahora verifica la configuración antes de intentar enviar emails
- **Manejo de Errores Específicos**: Captura errores SMTP específicos y los registra
- **Fallback Graceful**: Si el email falla, el mensaje se guarda y se notifica al usuario
- **Logging Mejorado**: Logs específicos para debugging de email

### 2. Comando de Prueba

Se creó un comando para probar la configuración de email:

```bash
python manage.py test_email --to tu-email@ejemplo.com
```

### 3. Configuración Automática

En desarrollo, si `EMAIL_HOST_PASSWORD` no está configurado, se usa el backend de consola automáticamente.

## Configuración Requerida

### Opción 1: SpaceMail (Recomendado)

1. **Crear archivo `.env`** en la raíz del proyecto:

```env
# Configuración de Email - SpaceMail
EMAIL_HOST=mail.spacemail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=info@inglat.com
EMAIL_HOST_PASSWORD=tu-password-de-spacemail
DEFAULT_FROM_EMAIL=info@inglat.com
NOTIFICATION_EMAIL=contacto@inglat.com
```

2. **Obtener credenciales de SpaceMail**:
   - Acceder al panel de control de SpaceMail
   - Ir a "Email Accounts" o "Cuentas de Email"
   - Crear o usar una cuenta existente
   - Obtener la contraseña de la cuenta

### Opción 2: Gmail (Alternativa)

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_SSL=False
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password-de-gmail
DEFAULT_FROM_EMAIL=tu-email@gmail.com
```

**Nota para Gmail**: Necesitas habilitar "Contraseñas de aplicación" en la configuración de seguridad de Google.

### Opción 3: Outlook/Hotmail

```env
EMAIL_HOST=smtp-mail.outlook.com
EMAIL_PORT=587
EMAIL_USE_SSL=False
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@outlook.com
EMAIL_HOST_PASSWORD=tu-password-de-outlook
DEFAULT_FROM_EMAIL=tu-email@outlook.com
```

## Pasos para Configurar

### 1. Crear archivo .env

```bash
# En la raíz del proyecto
cp env.example .env
```

### 2. Editar .env con tus credenciales

```bash
# Editar el archivo .env y agregar tus credenciales reales
nano .env
```

### 3. Probar la configuración

```bash
# Probar con tu email
python manage.py test_email --to tu-email@ejemplo.com
```

### 4. Verificar logs

```bash
# Ver logs de email
tail -f logs/email.log
```

## Troubleshooting

### Error: "EMAIL_HOST_PASSWORD no configurado"

**Solución**: Configurar la variable `EMAIL_HOST_PASSWORD` en el archivo `.env`

### Error: "Error de autenticación SMTP"

**Posibles causas**:
- Contraseña incorrecta
- Usuario incorrecto
- Configuración de seguridad del proveedor de email

**Soluciones**:
1. Verificar credenciales
2. Para Gmail: Usar contraseña de aplicación
3. Para SpaceMail: Verificar configuración en el panel

### Error: "Error de conexión SMTP"

**Posibles causas**:
- Host o puerto incorrecto
- Firewall bloqueando conexión
- Proveedor de email no disponible

**Soluciones**:
1. Verificar host y puerto
2. Probar con otro proveedor de email
3. Verificar conectividad de red

### Error: "Respuesta del servidor no es JSON válido"

**Causa**: Error en el servidor Django que no devuelve JSON válido

**Solución**: Verificar logs de Django en `logs/django.log`

## Configuración de Producción

Para producción, asegúrate de:

1. **Variables de entorno**: Configurar todas las variables en el servidor
2. **Logs**: Configurar rotación de logs
3. **Monitoreo**: Configurar alertas para errores de email
4. **Backup**: Configurar backup de mensajes de contacto

## Comandos Útiles

```bash
# Probar configuración de email
python manage.py test_email --to tu-email@ejemplo.com

# Ver logs de email
tail -f logs/email.log

# Ver logs generales
tail -f logs/django.log

# Verificar configuración actual
python manage.py shell -c "from django.conf import settings; print('EMAIL_HOST:', settings.EMAIL_HOST); print('EMAIL_HOST_PASSWORD configured:', bool(settings.EMAIL_HOST_PASSWORD))"
```

## Contacto de Soporte

Si tienes problemas con la configuración:

1. Revisar logs en `logs/email.log`
2. Ejecutar comando de prueba
3. Verificar configuración de variables de entorno
4. Contactar soporte técnico con los logs de error

