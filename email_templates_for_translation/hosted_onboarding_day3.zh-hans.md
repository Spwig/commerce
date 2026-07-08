---
template_type: hosted_onboarding_day3
category: License
---

# Email Template: hosted_onboarding_day3

## Subject
构建您的商品目录 - {{ store_name }}

## HTML Content
<mjml>
  <mj-head>
    <mj-attributes>
      <mj-all font-family="'Helvetica Neue', Helvetica, Arial, sans-serif" />
      <mj-text font-size="14px" color="#333333" line-height="20px" />
      <mj-section background-color="{{ theme.color.background|default:'#ffffff' }}" padding="20px" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}">
    <!-- Header -->
    <mj-section background-color="{{ theme.color.primary|default:'#2563eb' }}" padding="30px 20px">
      <mj-column>
        <mj-text font-size="28px" font-weight="bold" color="#ffffff" align="center">
          入门指南：您的商品
        </mj-text>
        <mj-text font-size="16px" color="#ffffffcc" align="center" padding-top="10px">
          为 {{ store_name }} 构建一个出色的商品目录
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Greeting -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px">
          你好 {{ name|default:'there' }},
        </mj-text>
        <mj-text>
          您的店铺 <strong>{{ store_name }}</strong> 已经设置完成。现在是时候构建您的商品目录了。以下是一些入门建议。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 1 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          从 CSV 导入商品
        </mj-text>
        <mj-text font-size="14px">
          已经有商品列表了吗？前往 <strong>管理 > 商品目录 > 导入</strong>，从 CSV 文件批量导入您的商品。这是最快的方式为您的店铺填充商品。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 2 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          通过分类和筛选器进行整理
        </mj-text>
        <mj-text font-size="14px">
          创建分类和属性筛选器，以便客户轻松浏览并找到他们想要的商品。组织良好的商品目录可以提高转化率。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 3 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          撰写有吸引力的商品描述
        </mj-text>
        <mj-text font-size="14px">
          优秀的描述能促进销售。关注商品带来的好处，而不仅仅是功能。告诉客户他们为什么需要您的商品，以及它如何解决他们的问题。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 4 -->
    <mj-section>
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          上传高质量的商品图片
        </mj-text>
        <mj-text font-size="14px">
          清晰专业的图片会产生巨大影响。上传多个角度的图片并使用一致的灯光。Spwig 会自动优化图片以实现快速加载。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- Tip 5 -->
    <mj-section background-color="{{ theme.color.background_secondary|default:'#f9fafb' }}" padding="20px" border-radius="8px">
      <mj-column>
        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.primary|default:'#2563eb' }}" padding-bottom="5px">
          设置商品变体
        </mj-text>
        <mj-text font-size="14px">
          如果您的商品有不同尺寸、颜色或款式，创建变体，以便客户可以选择他们想要的精确商品。每个变体可以有自己的价格、库存和图片。
        </mj-text>
      </mj-column>
    </mj-section>

    <!-- CTA -->
    {% include 'email_system/mjml_components/cta_button.mjml' with url=admin_url text="管理您的商品" %}

    <!-- Support -->
    {% include 'email_system/mjml_components/support_block.mjml' %}
  </mj-body>
</mjml>

## Text Content
入门指南：您的商品 - {{ store_name }}

你好 {{ name|default:'there' }},

您的店铺 {{ store_name }} 已经设置完成。现在是时候构建您的商品目录了。以下是一些入门建议。

1. 从 CSV 导入商品
已经拥有商品列表了吗？前往 管理 > 商品目录 > 导入，从 CSV 文件批量导入您的商品。

2. 通过分类和筛选器进行整理
创建分类和属性筛选器，以便客户轻松浏览并找到他们想要的商品。

3. 撰写有吸引力的商品描述
优秀的描述能促进销售。关注商品带来的好处，而不仅仅是功能。告诉客户他们为什么需要您的商品。

4. 上传高质量的商品图片
清晰专业的图片会产生巨大影响。上传多个角度的图片并使用一致的灯光。

5. 设置商品变体
如果您的商品有不同尺寸、颜色或款式，创建变体，以便客户可以选择他们想要的精确商品。

管理您的商品：{{ admin_url }}

需要帮助？请联系 {{ support_email }}