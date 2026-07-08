---
template_type: shipping_exception
category: Shipping
---

# Email Template: shipping_exception

## Subject
运输异常 - 订单 #{{ order_number }} 需要处理

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fef3c7">
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="#92400e" align="center">
          ⚠️ 运输异常
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          你好 {{ customer_name }}，
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          我们写信是为了告知你有关你的运输出现异常。我们正在尽最大努力尽快解决这个问题。
        </mj-text>

        <mj-spacer height="20px" />

        <mj-section background-color="#fef3c7" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#92400e">
              异常详情：
            </mj-text>
            <mj-text color="#92400e">
              <strong>异常类型：</strong> {{ exception_type }}<br/>
              <strong>描述：</strong> {{ exception_description }}<br/>
              <strong>发生时间：</strong> {{ exception_date }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="20px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              订单信息：
            </mj-text>
            <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
              <strong>订单编号：</strong> {{ order_number }}<br/>
              <strong>跟踪编号：</strong> {{ tracking_number }}<br/>
              <strong>承运商：</strong> {{ carrier_name }}<br/>
              <strong>当前位置：</strong> {{ current_location }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          接下来会发生什么？
        </mj-text>

        <mj-text color="{{ theme.color.text|default:'#4b5563' }}">
          {{ resolution_steps }}
        </mj-text>

        <mj-spacer height="20px" />

        {% if action_required %}
        <mj-section background-color="#fee2e2" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b">
              ⚠️ 需要操作：
            </mj-text>
            <mj-text color="#7f1d1d">
              {{ action_required_description }}
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="20px" />
        {% endif %}

        <mj-button href="{{ tracking_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          跟踪您的订单
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ support_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          联系支持
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
⚠️ 运输异常

你好 {{ customer_name }}，

我们写信是为了告知你有关你的运输出现异常。我们正在尽最大努力尽快解决这个问题。

异常详情：
- 异常类型： {{ exception_type }}
- 描述： {{ exception_description }}
- 发生时间： {{ exception_date }}

订单信息：
- 订单编号： {{ order_number }}
- 跟踪编号： {{ tracking_number }}
- 承运商： {{ carrier_name }}
- 当前位置： {{ current_location }}

接下来会发生什么？
{{ resolution_steps }}

{% if action_required %}
⚠️ 需要操作：
{{ action_required_description }}
{% endif %}

跟踪您的订单： {{ tracking_url }}
联系支持： {{ support_url }}