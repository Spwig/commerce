---
template_type: admin_payment_sdk_failure
category: Admin Notifications
---

# Email Template: admin_payment_sdk_failure

## Subject
Problema con el Proveedor de Pago - SDK de {{ provider_name }} No Cargado

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.warning|default:'#f59e0b' }}">
          Problema con el Proveedor de Pago
        </mj-text>
        <mj-text>
          El SDK de pago de {{ provider_name }} no se cargó para un cliente durante el proceso de pago. Esto puede indicar una interrupción de servicio con el proveedor.
        </mj-text>
        <mj-text>
          <strong>Proveedor:</strong> {{ provider_name }}
        </mj-text>
        <mj-text>
          <strong>Tipo de Error:</strong> {{ error_type }}
        </mj-text>
        <mj-text>
          <strong>Hora:</strong> {{ timestamp }}
        </mj-text>
        <mj-text>
          <strong>Cantidad de Fallos (última hora):</strong> {{ failure_count }}
        </mj-text>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" />
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}">
          Esta notificación está limitada por tasa a una por proveedor por hora. Si el problema persiste, revise el panel del proveedor o contacte su soporte.
        </mj-text>
        <mj-button href="{{ admin_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}">
          Ver Configuración de Pago
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
Problema con el Proveedor de Pago

El SDK de pago de {{ provider_name }} no se cargó para un cliente durante el proceso de pago. Esto puede indicar una interrupción de servicio con el proveedor.

Proveedor: {{ provider_name }}
Tipo de Error: {{ error_type }}
Hora: {{ timestamp }}
Cantidad de Fallos (última hora): {{ failure_count }}

Esta notificación está limitada por tasa a una por proveedor por hora. Si el problema persiste, revise el panel del proveedor o contacte su soporte.

Ver configuración de pago: {{ admin_url }}