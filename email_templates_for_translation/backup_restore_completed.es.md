---
template_type: backup_restore_completed
category: Backups
---

# Email Template: backup_restore_completed

## Subject
✓ Restauración de copia de seguridad completada - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#f0fdf4">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#059669" align="center">
          ✓ Restauración de copia de seguridad completada
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Su operación de restauración de copia de seguridad se ha completado con éxito. Los datos de su tienda han sido restaurados.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Detalles de la restauración:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Archivo de copia de seguridad:</strong> {{ backup_filename }}<br/>
              <strong>Fecha de copia de seguridad:</strong> {{ backup_date }}<br/>
              <strong>Iniciado:</strong> {{ restore_started_at }}<br/>
              <strong>Completado:</strong> {{ restore_completed_at }}<br/>
              <strong>Duración:</strong> {{ restore_duration }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              ⚠️ Pasos importantes siguientes:
            </mj-text>
            <mj-text font-size="14px" color="#92400e">
              1. Verifique que su tienda funcione correctamente<br/>
              2. Revise los datos clave (productos, pedidos, clientes)<br/>
              3. Limpie la caché si es necesario<br/>
              4. Pruebe los flujos de trabajo críticos (checkout, acceso al administrador)
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_dashboard_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Ir al panel de administración
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
✓ BACKUP RESTORE COMPLETED

Hola {{ admin_name }},

Su operación de restauración de copia de seguridad se ha completado con éxito. Los datos de su tienda han sido restaurados.

RESTORE DETAILS:
- Backup File: {{ backup_filename }}
- Backup Date: {{ backup_date }}
- Started: {{ restore_started_at }}
- Completed: {{ restore_completed_at }}
- Duration: {{ restore_duration }}

⚠️ IMPORTANT NEXT STEPS:
1. Verify your store is functioning correctly
2. Check key data (products, orders, customers)
3. Clear cache if needed
4. Test critical workflows (checkout, admin access)

Go to admin dashboard: {{ admin_dashboard_url }}