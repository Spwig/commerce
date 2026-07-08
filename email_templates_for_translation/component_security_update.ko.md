---
template_type: component_security_update
category: Component Updates
---

# Email Template: component_security_update

## Subject
🔒 긴급: {{ component_name }}용 보안 업데이트 가능

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#fee2e2">
      <mj-column>
        <mj-text font-size="22px" font-weight="bold" color="#991b1b" align="center">
          🔒 보안 업데이트 필요
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          중대한 보안 패치
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          {{ component_name }}에서 보안 취약점이 발견되었습니다. 가게를 보호하기 위해 즉시 업데이트해 주세요.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#fee2e2" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-weight="bold" color="#991b1b" font-size="16px">
              ⚠️ 보안 정보
            </mj-text>
            <mj-text color="#991b1b">
              <strong>성분:</strong> {{ component_name }}<br/>
              <strong>현재 버전:</strong> {{ current_version }}<br/>
              <strong>패치된 버전:</strong> {{ patched_version }}<br/>
              <strong>중요도:</strong> {{ severity_level }}<br/>
              <strong>CVE ID:</strong> {{ cve_id }}
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          취약점 세부 사항:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ vulnerability_description }}
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          잠재적 영향:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}" line-height="1.8">
          {{ impact_description }}
        </mj-text>

        {% if mitigation_steps %}
        <mj-spacer height="30px" />
        <mj-section background-color="#fef3c7" border-radius="8px" padding="15px">
          <mj-column>
            <mj-text font-size="14px" color="#92400e" font-weight="bold">
              일시적 완화
            </mj-text>
            <mj-text font-size="14px" color="#92400e" line-height="1.6">
              {{ mitigation_steps }}
            </mj-text>
          </mj-column>
        </mj-section>
        {% endif %}

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          필요한 조치: 즉시 업데이트 설치
        </mj-text>

        <mj-spacer height="20px" />

        <mj-button href="{{ update_url }}" background-color="#dc2626" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          보안 패치 설치
        </mj-button>

        <mj-spacer height="10px" />

        <mj-button href="{{ advisory_url }}" background-color="#6b7280" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
          보안 가이드라인 읽기
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          도움이 필요하시면 즉시 Spwig 지원팀에 연락주세요.
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🔒 보안 업데이트 필요

중대한 보안 패치

{{ component_name }}에서 보안 취약점이 발견되었습니다. 가게를 보호하기 위해 즉시 업데이트해 주세요.

⚠️ 보안 정보:
- 성분: {{ component_name }}
- 현재 버전: {{ current_version }}
- 패치된 버전: {{ patched_version }}
- 중요도: {{ severity_level }}
- CVE ID: {{ cve_id }}

취약점 세부 사항:
{{ vulnerability_description }}

잠재적 영향:
{{ impact_description }}

{% if mitigation_steps %}
일시적 완화:
{{ mitigation_steps }}
{% endif %}

필요한 조치: 즉시 업데이트 설치

보안 패치 설치: {{ update_url }}
보안 가이드라인 읽기: {{ advisory_url }}

도움이 필요하시면 즉시 Spwig 지원팀에 연락주세요.