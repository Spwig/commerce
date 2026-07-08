---
template_type: loyalty_referral_bonus
category: Loyalty Program
---

# Email Template: loyalty_referral_bonus

## Subject
🎁 {{ referee_name }}を紹介していただいたボーナスポイント！

## HTML Content
<mjml>
  <mj-body>
    <mj-section background-color="#dcfce7">
      <mj-column>
        <mj-text font-size="24px" font-weight="bold" color="#065f46" align="center">
          🎁 ご紹介ボーナスを獲得しました！
        </mj-text>
      </mj-column>
    </mj-section>

    <mj-section>
      <mj-column>
        <mj-text font-size="20px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご共有ありがとうございます、{{ customer_name }}！
        </mj-text>

        <mj-text font-size="16px" line-height="1.6" color="{{ theme.color.text|default:'#4b5563' }}">
          グッドニュース！{{ referee_name }}がご紹介を通じてロイヤルティプログラムにご加入されました。ボーナスポイントを獲得しました！
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="#f0fdf4" border-radius="8px" padding="25px">
          <mj-column>
            <mj-text font-size="18px" font-weight="bold" color="#065f46" align="center">
              獲得したポイント
            </mj-text>
            <mj-text font-size="36px" font-weight="bold" color="#047857" align="center">
              +{{ bonus_points }} ポイント
            </mj-text>
            <mj-text font-size="14px" color="#065f46" align="center">
              {{ referee_name }}をご紹介したため
            </mj-text>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
          ご更新された残高：
        </mj-text>

        <mj-text font-size="15px" color="{{ theme.color.text|default:'#4b5563' }}">
          <strong>ポイント残高：</strong>{{ total_points }} ポイント<br/>
          <strong>紹介ボーナス：</strong>+{{ bonus_points }} ポイント<br/>
          <strong>ご紹介した友人：</strong>{{ total_referrals }}
        </mj-text>

        <mj-spacer height="30px" />

        <mj-section background-color="{{ theme.color.surface|default:'#f9fafb' }}" border-radius="8px" padding="20px">
          <mj-column>
            <mj-text font-size="16px" font-weight="bold" color="{{ theme.color.text|default:'#1f2937' }}">
              ご紹介を続けるとポイントを獲得し続けられます！
            </mj-text>
            <mj-text font-size="14px" color="{{ theme.color.text|default:'#4b5563' }}">
              友人が参加するごとに{{ points_per_referral }}ポイントを獲得できます。上限なし！
            </mj-text>
            <mj-spacer height="15px" />
            <mj-button href="{{ referral_url }}" background-color="{{ theme.color.primary|default:'#2563eb' }}" color="#ffffff" font-size="14px" border-radius="6px" padding="10px 25px">
              ご紹介リンクを共有
            </mj-button>
          </mj-column>
        </mj-section>

        <mj-spacer height="30px" />

        <mj-button href="{{ shop_url }}" background-color="#059669" color="#ffffff" font-size="16px" font-weight="bold" border-radius="6px" padding="15px 40px">
          ショッピングを開始する
        </mj-button>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>

## Text Content
🎁 ご紹介ボーナス獲得！

ご共有ありがとうございます、{{ customer_name }}！

グッドニュース！{{ referee_name }}がご紹介を通じてロイヤルティプログラムにご加入されました。ボーナスポイントを獲得しました！

獲得したポイント：
+{{ bonus_points }} ポイント
{{ referee_name }}をご紹介したため

ご更新された残高：
- ポイント残高：{{ total_points }} ポイント
- 紹介ボーナス：+{{ bonus_points }} ポイント
- 紹介した友人：{{ total_referrals }}

ご紹介を続けるとポイントを獲得し続けられます！
友人が参加するごとに{{ points_per_referral }}ポイントを獲得できます。上限なし！

ご紹介リンクを共有：{{ referral_url }}
ショッピングを開始する：{{ shop_url }}