from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.resources import resource_add_path
from kivy.core.text import LabelBase
import os
from datetime import datetime

resource_add_path(os.path.dirname(os.path.abspath(__file__)))

try:
    LabelBase.register(name='SimHei', fn_regular='fonts/simhei.ttf')
    CHINESE_FONT = 'SimHei'
except:
    CHINESE_FONT = 'Roboto'

Window.size = (400, 700)


class ReceiptGenerator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        self.input_fields = {}
        
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        content.bind(minimum_height=content.setter('height'))
        
        title = Label(
            text='收据生成器',
            size_hint_y=None,
            height=50,
            font_size=24,
            font_name=CHINESE_FONT,
            bold=True
        )
        content.add_widget(title)
        
        self.create_input_field(content, 'number', '编号', '')
        self.create_input_field(content, 'date', '入账日期 (YYYY年MM月DD日)', datetime.now().strftime('%Y年%m月%d日'))
        self.create_input_field(content, 'payer', '交款单位', '')
        self.create_input_field(content, 'payment_method', '收款方式', '')
        self.create_input_field(content, 'amount', '金额 (元)', '0.00')
        self.create_input_field(content, 'reason', '收款事由', '')
        self.create_input_field(content, 'accountant', '财会主管', '')
        self.create_input_field(content, 'bookkeeper', '记账', '')
        self.create_input_field(content, 'cashier', '出纳', '')
        self.create_input_field(content, 'auditor', '审核', '')
        self.create_input_field(content, 'handler', '经办', '')
        
        generate_btn = Button(
            text='生成收据',
            size_hint=(1, None),
            height=60,
            font_size=20,
            font_name=CHINESE_FONT,
            background_color=(0.2, 0.6, 1, 1)
        )
        generate_btn.bind(on_press=self.generate_receipt)
        content.add_widget(generate_btn)
        
        scroll.add_widget(content)
        self.add_widget(scroll)
    
    def create_input_field(self, parent, field_name, label_text, default_value):
        box = BoxLayout(orientation='vertical', size_hint_y=None, height=80, spacing=5)
        label = Label(text=label_text, size_hint_y=None, height=25, font_size=14, font_name=CHINESE_FONT, halign='left')
        label.bind(texture_size=label.setter('size'))
        text_input = TextInput(
            text=default_value,
            size_hint=(1, None),
            height=45,
            font_size=16,
            font_name=CHINESE_FONT,
            multiline=False,
            padding=[10, 10]
        )
        box.add_widget(label)
        box.add_widget(text_input)
        parent.add_widget(box)
        self.input_fields[field_name] = text_input
    
    def number_to_chinese(self, num):
        chinese_nums = ['零', '壹', '贰', '叁', '肆', '伍', '陆', '柒', '捌', '玖']
        chinese_units = ['', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿']
        
        try:
            num_float = float(num)
            if num_float == 0:
                return '零元整'
            
            integer_part = int(num_float)
            decimal_part = round((num_float - integer_part) * 100)
            
            result = ''
            
            if integer_part == 0:
                result = '零'
            else:
                num_str = str(integer_part)
                length = len(num_str)
                
                for i, digit in enumerate(num_str):
                    digit_int = int(digit)
                    pos = length - i - 1
                    
                    if digit_int != 0:
                        result += chinese_nums[digit_int] + chinese_units[pos]
                    else:
                        if i < length - 1 and int(num_str[i+1]) != 0:
                            result += chinese_nums[0]
            
            result += '元'
            
            if decimal_part > 0:
                jiao = decimal_part // 10
                fen = decimal_part % 10
                
                if jiao > 0:
                    result += chinese_nums[jiao] + '角'
                if fen > 0:
                    result += chinese_nums[fen] + '分'
            else:
                result += '整'
            
            return result
        except:
            return '零元整'
    
    def generate_receipt(self, instance):
        try:
            number = self.input_fields['number'].text
            date_str = self.input_fields['date'].text
            payer = self.input_fields['payer'].text
            payment_method = self.input_fields['payment_method'].text
            amount = self.input_fields['amount'].text
            reason = self.input_fields['reason'].text
            accountant = self.input_fields['accountant'].text
            bookkeeper = self.input_fields['bookkeeper'].text
            cashier = self.input_fields['cashier'].text
            auditor = self.input_fields['auditor'].text
            handler = self.input_fields['handler'].text
            
            svg_template_path = os.path.join(os.path.dirname(__file__), '收据.svg')
            
            with open(svg_template_path, 'r', encoding='utf-8') as f:
                svg_content = f.read()
            
            chinese_amount = self.number_to_chinese(amount)
            
            temp_svg = svg_content
            
            font_style = '''
      @font-face {
        font-family: 'STXINGKA';
        src: url('fonts/STXINGKA.TTF') format('truetype');
      }
      .cls-new {
        fill: #000;
        font-size: 9px;
        font-family: 'STXINGKA', sans-serif;
      }
'''
            
            temp_svg = temp_svg.replace('</style>', font_style + '</style>')
            
            temp_svg = temp_svg.replace('</svg>', f'<text class="cls-new" transform="translate(430 50)"><tspan x="0" y="0">{number}</tspan></text></svg>')
            
            temp_svg = temp_svg.replace('入账日期：    年    月    日', f'入账日期：{date_str}')
            
            temp_svg = temp_svg.replace(
                '<text class="cls-5" transform="translate(49.04 108.13)"><tspan x="0" y="0">交款单位</tspan></text>',
                f'<text class="cls-5" transform="translate(49.04 108.13)"><tspan x="0" y="0">交款单位</tspan></text><text class="cls-new" transform="translate(130 108.13)"><tspan x="0" y="0">{payer}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-5" transform="translate(306.99 108.13)"><tspan x="0" y="0">收款方式</tspan></text>',
                f'<text class="cls-5" transform="translate(306.99 108.13)"><tspan x="0" y="0">收款方式</tspan></text><text class="cls-new" transform="translate(385 108.13)"><tspan x="0" y="0">{payment_method}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-8" transform="translate(49.04 133.64)"><tspan class="cls-14" x="0" y="0">人 民 币</tspan><tspan class="cls-12" x="72" y="0">(</tspan><tspan class="cls-13" x="77.5" y="0">大写 </tspan><tspan class="cls-12" x="96.75" y="0">)</tspan></text>',
                f'<text class="cls-8" transform="translate(49.04 133.64)"><tspan class="cls-14" x="0" y="0">人 民 币</tspan><tspan class="cls-12" x="72" y="0">(</tspan><tspan class="cls-13" x="77.5" y="0">大写 </tspan><tspan class="cls-12" x="96.75" y="0">)</tspan></text><text class="cls-new" transform="translate(160 133.64)"><tspan x="0" y="0">{chinese_amount}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-9" transform="translate(355.51 131.92)"><tspan x="0" y="0">¥</tspan></text>',
                f'<text class="cls-9" transform="translate(355.51 131.92)"><tspan x="0" y="0">¥</tspan></text><text class="cls-new" transform="translate(385 131.92)"><tspan x="0" y="0">{amount}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-5" transform="translate(49.04 159.15)"><tspan x="0" y="0">收款事由</tspan></text>',
                f'<text class="cls-5" transform="translate(49.04 159.15)"><tspan x="0" y="0">收款事由</tspan></text><text class="cls-new" transform="translate(130 159.15)"><tspan x="0" y="0">{reason}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-6" transform="translate(283.4 205.24)"><tspan x="0" y="0">财会主管</tspan></text>',
                f'<text class="cls-6" transform="translate(283.4 205.24)"><tspan x="0" y="0">财会主管</tspan></text><text class="cls-new" transform="translate(310 225)"><tspan x="0" y="0">{accountant}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-6" transform="translate(340.16 205.8)"><tspan x="0" y="0">记</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">账</tspan></text>',
                f'<text class="cls-6" transform="translate(340.16 205.8)"><tspan x="0" y="0">记</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">账</tspan></text><text class="cls-new" transform="translate(367 225)"><tspan x="0" y="0">{bookkeeper}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-6" transform="translate(396.85 205.8)"><tspan x="0" y="0">出</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">纳</tspan></text>',
                f'<text class="cls-6" transform="translate(396.85 205.8)"><tspan x="0" y="0">出</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">纳</tspan></text><text class="cls-new" transform="translate(423 225)"><tspan x="0" y="0">{cashier}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-6" transform="translate(453.54 205.8)"><tspan x="0" y="0">审</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">核</tspan></text>',
                f'<text class="cls-6" transform="translate(453.54 205.8)"><tspan x="0" y="0">审</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">核</tspan></text><text class="cls-new" transform="translate(480 225)"><tspan x="0" y="0">{auditor}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-6" transform="translate(510.24 205.8)"><tspan x="0" y="0">经</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">办</tspan></text>',
                f'<text class="cls-6" transform="translate(510.24 205.8)"><tspan x="0" y="0">经</tspan><tspan x="0" y="14.31" xml:space="preserve">          </tspan><tspan class="cls-15" x="0" y="41.81">办</tspan></text><text class="cls-new" transform="translate(537 225)"><tspan x="0" y="0">{handler}</tspan></text>'
            )
            
            temp_svg = temp_svg.replace(
                '<text class="cls-2" transform="translate(429.8 194.72)"><tspan x="0" y="0" xml:space="preserve">    年    月    日</tspan></text>',
                f'<text class="cls-2" transform="translate(429.8 194.72)"><tspan x="0" y="0" xml:space="preserve">    {date_str[0:4]}年{date_str[5:7]}月{date_str[8:10]}日</tspan></text>'
            )
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            svg_filename = f'receipt_{timestamp}.svg'
            
            with open(svg_filename, 'w', encoding='utf-8') as f:
                f.write(temp_svg)
            
            popup = Popup(
                title='成功',
                content=Label(text=f'收据已生成：\n{svg_filename}', font_size=18, font_name=CHINESE_FONT),
                size_hint=(0.8, 0.3)
            )
            popup.open()
            
        except Exception as e:
            import traceback
            error_msg = f'生成失败：\n{str(e)}\n\n详细信息：\n{traceback.format_exc()}'
            popup = Popup(
                title='错误',
                content=Label(text=error_msg, font_size=12, font_name=CHINESE_FONT),
                size_hint=(0.9, 0.5)
            )
            popup.open()


class ReceiptApp(App):
    def build(self):
        return ReceiptGenerator()


if __name__ == '__main__':
    ReceiptApp().run()
