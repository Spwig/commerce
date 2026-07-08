---
template_type: backup_size_warning
category: Backups
---

# Email Template: backup_size_warning

## Subject
⚠️ Advertencia de Tamaño de Copia de Seguridad - {{ shop_name }}

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ Advertencia de Tamaño de Copia de Seguridad
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Hola {{ admin_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          Su copia de seguridad reciente para {{ shop_name }} ha superado el umbral de tamaño recomendado. Esto podría indicar necesidades crecientes de almacenamiento de datos.
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              Información de Copia de Seguridad:
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>Tamaño Actual:</strong> {{ backup_size }}<br/>
              <strong>Umbral de Advertencia:</strong> {{ size_threshold }}<br/>
              <strong>Crecimiento Desde la Semana Pasada:</strong> {{ size_increase }}<br/>
              <strong>Fecha de Copia de Seguridad:</strong> {{ backup_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          Acciones Recomendadas:
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          1. Revisar la política de retención de copias de seguridad<br/>
          2. Considerar el archivo de copias de seguridad antiguas<br/>
          3. Revisar archivos grandes innecesarios en la biblioteca de medios<br/>
          4. Evaluar las necesidades de capacidad de almacenamiento<br/>
          5. Monitorear la tendencia de crecimiento de copias de seguridad
        </mj-text>

        <mj-spacer height="30px" />

        <mj-button href="{{ admin_backup_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" border-radius="6px" padding="12px 30px">
          Administrar Copias de Seguridad
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ ADVERTENCIA DE TAMAÑO DE COPIA DE SEGURIDAD

Hola {{ admin_name }},

Su copia de seguridad reciente para {{ shop_name }} ha superado el umbral de tamaño recomendado. Esto podría indicar necesidades crecientes de almacenamiento de datos.

INFORMACIÓN DE COPIA DE SEGURIDAD:
- Tamaño Actual: {{ backup_size }}
- Umbral de Advertencia: {{ size_threshold }}
- Crecimiento Desde la Semana Pasada: {{ size_increase }}
- Fecha de Copia de Seguridad: {{ backup_date }}

ACCIONES RECOMENDADAS:
1. Revisar la política de retención de copias de seguridad
2. Considerar el archivo de copias de seguridad antiguas
3. Revisar archivos grandes innecesarios en la biblioteca de medios
4. Evaluar las necesidades de capacidad de almacenamiento
5. Monitorear la tendencia de crecimiento de copias de seguridad

Administrar copias de seguridad: {{ admin_backup_url }}