---
template_type: blog_subscriber_welcome
category: Blog
---

# Email Template: blog_subscriber_welcome

## Subject
🎉 {{ blog_name }}에 오신 것을 환영합니다!

## HTML Content
<mjml>
  <mj-body>
    <mj-section>
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" align="center">
          🎉 {{ blog_name }}에 오신 것을 환영합니다!
        </mj-text>

        <mj-spacer height="20px" />

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          안녕하세요 {{ subscriber_name }},
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          구독해 주셔서 감사합니다! 최신 콘텐츠를 함께 나누게 되어 기쁩니다.
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="#065f46">
              기대할 내용:
            </mj-text>
            <mj-text font-size="14px" color="#065f46" line-height="1.8">
              ✓ 이메일로 새 게시물이 전달됩니다<br/>
              ✓ 독점적인 구독자 전용 콘텐츠<br/>
              ✓ {{ publish_frequency }} 업데이트<br/>
              ✓ 스팸 없음, 언제든지 구독 해지 가능
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          시작하세요:
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          인기 기사 확인:
        </mj-text>

        <mj-spacer height="15px" />

        {% for post in popular_posts %}
        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="15px">
          <mj-column width="30%">
            <mj-image src="{{ post.featured_image }}" alt="{{ post.title }}" border-radius="4px" />
          </mj-column>
          <mj-column width="70%">
            <mj-text font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              {{ post.title }}
            </mj-text>
            <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}">
              {{ post.reading_time }} 분 읽기
            </mj-text>
            <mj-text font-size="14px">
              <a href="{{ post.url }}" style="color: {{ theme.color.primary|default:'#2563eb' }};">지금 읽기 →</a>
            </mj-text>
          </mj-column>
        </mj-section>
        <mj-spacer height="10px" />
        {% endfor %}

        <mj-spacer height="30px" />

        <mj-button href="{{ blog_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          모든 기사 탐색
        </mj-button>

        <mj-spacer height="30px" />

        <mj-text font-size="13px" color="{{ theme.color.text_secondary|default:'#6b7280' }}" align="center">
          구독 설정 관리: <a href="{{ preferences_url }}">이메일 설정</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎉 {{ blog_name }}에 오신 것을 환영합니다!

안녕하세요 {{ subscriber_name }},

구독해 주셔서 감사합니다! 최신 콘텐츠를 함께 나누게 되어 기쁩니다.

기대할 내용:
✓ 이메일로 새 게시물이 전달됩니다
✓ 독점적인 구독자 전용 콘텐츠
✓ {{ publish_frequency }} 업데이트
✓ 스팸 없음, 언제든지 구독 해지 가능

시작하세요 - 인기 기사:
{% for post in popular_posts %}
- {{ post.title }} ({{ post.reading_time }} 분 읽기)
  {{ post.url }}
{% endfor %}

모든 기사를 탐색하세요: {{ blog_url }}

구독 설정 관리: {{ preferences_url }}