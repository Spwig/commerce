---
template_type: backup_restore_failed
category: Backups
---

# Email Template: backup_restore_failed

## Subject
🚨 CRÍTICO: Fallo en la restauración de copia de seguridad - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#dc2626" align="center">
          🚨 CRÍTICO: Fallo en la restauración de copia de seguridad
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#1f2937' }}" font-weight="bold">
          Hola {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Una operación de restauración de copia de seguridad crítica ha fallado. Su tienda puede estar en un estado inconsistente y requiere atención inmediata.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Detalles de restauración:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Archivo de copia de seguridad:</strong> {{ backup_filename }}<br/>
              <strong>Iniciado:</strong> {{ restore_started_at }}<br/>
              <strong>Fallido:</strong> {{ restore_failed_at }}<br/>
              <strong>Duración:</strong> {{ restore_duration }}
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

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              🚨 ACCIÓN INMEDIATA REQUERIDA:
            </mj-text>
            <mj-text color="#92400e">
              1. <strong>NO</strong> haga cambios en la tienda<br/>
              2. Verifique la conectividad e integridad de la base de datos<br/>
              3. Revise los registros de errores para obtener el rastro de pila detallado<br/>
              4. Póngase en contacto con el soporte técnico de inmediato<br/>
              5. Considere retroceder a un estado conocido bueno
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ver registros de restauración
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#92400e" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Contactar soporte de emergencia
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 CRÍTICO: FALLO EN LA RESTAURACIÓN DE COPIA DE SEGURIDAD

Hola {{ admin_name }},

Una operación de restauración de copia de seguridad crítica ha fallado. Su tienda puede estar en un estado inconsistente y requiere atención inmediata.

DETALLES DE RESTAURACIÓN:
- Archivo de copia de seguridad: {{ backup_filename }}
- Iniciado: {{ restore_started_at }}
- Fallido: {{ restore_failed_at }}
- Duración: {{ restore_duration }}

DETALLES DEL ERROR:
{{ error_message }}

🚨 ACCIÓN INMEDIATA REQUERIDA:
1. NO haga cambios en la tienda
2. Verifique la conectividad e integridad de la base de datos
3. Revise los registros de errores para obtener el rastro de pila detallado
4. Póngase en contacto con el soporte técnico de inmediato
5. Considere retroceder a un estado conocido bueno

Ver registros de restauración: {{ admin_backup_url }}
Contactar soporte de emergencia: {{ support_url }}