---
template_type: backup_storage_quota_alert
category: Backups
---

# Email Template: backup_storage_quota_alert

## Subject
🚨 Cuota de almacenamiento de respaldo crítica - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef2f2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#dc2626" align="center">
          🚨 Cuota de Almacenamiento Crítica
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>URGENTE:</strong> Su almacenamiento de respaldo está críticamente bajo. Los respaldos futuros pueden fallar si no se libera espacio de almacenamiento.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              Estado del Almacenamiento:
            </mj-text>
            <mj-text color="#7f1d1d">
              <strong>Usado:</strong> {{ storage_used }} de {{ storage_total }}<br/>
              <strong>Utilización:</strong> {{ storage_percentage }}%<br/>
              <strong>Disponible:</strong> {{ storage_available }}<br/>
              <strong>Estado:</strong> <span style="color: #dc2626; font-weight: bold;">{{ storage_status }}</span>
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              Acciones Inmediatas Requeridas:
            </mj-text>
            <mj-text color="#92400e">
              1. Eliminar respaldos antiguos que ya no sean necesarios<br/>
              2. Archivar respaldos en almacenamiento externo<br/>
              3. Aumentar cuota de almacenamiento/capacidad<br/>
              4. Revisar la política de retención de respaldos<br/>
              5. Monitorear el almacenamiento diariamente hasta que se resuelva
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          Administrar Almacenamiento Ahora
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🚨 CUOTA DE ALMACENAMIENTO CRÍTICA

Hola {{ admin_name }},

URGENTE: Su almacenamiento de respaldo está críticamente bajo. Los respaldos futuros pueden fallar si no se libera espacio de almacenamiento.

ESTADO DEL ALMACENAMIENTO:
- Usado: {{ storage_used }} de {{ storage_total }}
- Utilización: {{ storage_percentage }}%
- Disponible: {{ storage_available }}
- Estado: {{ storage_status }}

ACCIONES INMEDIATAS REQUERIDAS:
1. Eliminar respaldos antiguos que ya no sean necesarios
2. Archivar respaldos en almacenamiento externo
3. Aumentar cuota de almacenamiento/capacidad
4. Revisar la política de retención de respaldos
5. Monitorear el almacenamiento diariamente hasta que se resuelva

Administrar almacenamiento ahora: {{ admin_backup_url }}