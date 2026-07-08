---
template_type: dev_account_approved
category: Developer Portal
---

# Email Template: dev_account_approved

## Subject
歡迎加入 Spwig 開發者計劃，{{ developer_name }}！

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-text font-family="Arial, sans-serif" line-height="1.6" />
      <mj-all font-family="Arial, sans-serif" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}">
    <!-- Header with Success Accent -->
    <mj-section background-color="{{ theme.color.success|default:'#10b981' }}" padding="40px 20px">
      <mj-column>
        <mj-text font-size="32px" font-weight="bold" color="{{ theme.color.background|default:'#ffffff' }}" align="center">
          歡迎加入 Spwig！
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.background|default:'#ffffff' }}" align="center" padding-top="10px">
          您的開發者申請已獲批准
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Content -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          請問 {{ developer_name }}，
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-top="20px">
          恭喜！您的開發者申請已獲批准。您現在可以完全訪問 Spwig 開發者門戶。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Free License Section -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px 20px 0">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          您的免費開發者許可證正在等待中
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          作為已批准的開發者，您將獲得 <strong>免費的 Spwig 商店 + POS 安裝</strong>，並享有永久更新。請領取您的許可證，在您的伺服器上安裝 Spwig，並立即開始構建組件。
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="15px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ license_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          領取免費許可證
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Get Started Section -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="18px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="15px">
          開始使用：
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>1.</strong> 領取您的免費開發者許可證
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>2.</strong> 在您的伺服器上安裝 Spwig
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}" padding-bottom="10px">
          <strong>3.</strong> 使用我們的 SDKs 建立您的第一個組件
        </mj-text>
        <mj-text font-size="16px" color="{{ theme.color.text|default:'#1f2937' }}">
          <strong>4.</strong> 從您的儀表板提交
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA Button -->
    <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="30px 20px">
      <mj-column>
        <mj-button background-color="{{ theme.color.success|default:'#10b981' }}" color="{{ theme.color.background|default:'#ffffff' }}" href="{{ dashboard_url }}" border-radius="6px" font-size="16px" font-weight="bold" padding="15px 30px">
          前往儀表板
        </mj-button>
      </mj-column>
    </mj-section>

    <!-- Footer -->
    <mj-section background-color="{{ theme.color.background_secondaryondary|default:'#f9fafb' }}" padding="30px 20px">
      <mj-column>
        <mj-divider border-color="{{ theme.color.border|default:'#e5e7eb' }}" padding-bottom="20px"></mj-divider>
        <mj-text font-size="14px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center">
          <strong>Spwig 開發者門戶</strong>
        </mj-text>
        <mj-text font-size="12px" color="{{ theme.color.text_muted|default:'#6b7280' }}" align="center" padding-top="10px">
          有問題嗎？請聯繫開發者支援
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
您好 {{ developer_name }}，

恭喜！您的開發者申請已獲批准。您現在可以完全訪問 Spwig 開發者門戶。

您的免費開發者許可證正在等待中
作為已批准的開發者，您將獲得免費的 Spwig 商店 + POS 安裝，並享有永久更新。請領取您的許可證，在您的伺服器上安裝 Spwig，並立即開始構建組件。

領取您的免費許可證：{{ license_url }}

開始使用：
1. 領取您的免費開發者許可證：{{ license_url }}
2. 在您的伺服器上安裝 Spwig
3. 使用我們的 SDKs 建立您的第一個組件
4. 從您的儀表板提交

前往儀表板：{{ dashboard_url }}

---
Spwig 開發者門戶