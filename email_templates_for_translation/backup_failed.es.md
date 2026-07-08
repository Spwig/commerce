---
template_type: backup_failed
category: Backups
---

# Email Template: backup_failed

## Subject
🚨 URGENTE: Error de copia de seguridad - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          ⚠️ Error de copia de seguridad
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}">
          Hola {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Una operación de copia de seguridad crítica ha fallado para su tienda {{ shop_name }}. Se requiere una acción inmediata para garantizar la protección de los datos.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Detalles de la copia de seguridad:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Tipo de copia de seguridad:</strong> {{ backup_type }}<br/>
              <strong>Comenzado:</strong> {{ backup_started_at }}<br/>
              <strong>Fallido:</strong> {{ backup_failed_at }}<br/>
              <strong>Duración:</strong> {{ backup_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Detalles del error:
        </mj-text>

        <mj-section background-color="#f9fafb" border-radius="4px" padding="15px">
          <mj-column>
            <mj-text font-family="'Courier New', monospace" font-size="13px" color="#dc2626">
              {{ error_message }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones recomendadas:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Verificar el espacio en disco disponible en su servidor<br/>
          2. Verificar la conectividad de la base de datos<br/>
          3. Revisar el registro de errores para obtener una traza de pila detallada<br/>
          4. Volver a intentar la copia de seguridad manualmente o esperar la próxima ejecución programada<br/>
          5. Póngase en contacto con el soporte si el problema persiste
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver registros de copia de seguridad
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ retry_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Volver a intentar la copia de seguridad ahora
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="14px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
          <strong>Última copia de seguridad exitosa:</strong> {{ last_successful_backup }}<br/>
          <strong>Próxima copia de seguridad programada:</strong> {{ next_scheduled_backup }}
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 URGENTE: COPIA DE SEGURIDAD FALLIDA

Hola {{ admin_name }},

Una operación de copia de seguridad crítica ha fallado para su tienda {{ shop_name }}. Se requiere una acción inmediata para garantizar la protección de los datos.

DETALLES DE LA COPIA DE SEGURIDAD:
- Tipo de copia de seguridad: {{ backup_type }}
- Comenzado: {{ backup_started_at }}
- Fallido: {{ backup_failed_at }}
- Duración: {{ backup_duration }}

DETALLES DEL ERROR:
{{ error_message }}

ACCIONES RECOMENDADAS:
1. Verificar el espacio en disco disponible en su servidor
2. Verificar la conectividad de la base de datos
3. Revisar el registro de errores para obtener una traza de pila detallada
4. Volver a intentar la copia de seguridad manualmente o esperar la próxima ejecución programada
5. Póngase en contacto con el soporte si el problema persiste

Ver registros de copia de seguridad: {{ admin_backup_url }}
Volver a intentar la copia de seguridad ahora: {{ retry_backup_url }}

Última copia de seguridad exitosa: {{ last_successful_backup }}
Próxima copia de seguridad programada: {{ next_scheduled_backup }}

---
Este es un aviso crítico del sistema para los administradores de {{ shop_name }}.