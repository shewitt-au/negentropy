{%- if title -%}
---
title: {{title}}
---
{% endif %}

{%- macro comment_before(i) -%}
{%- if i.comment_before -%}
{%- for line in i.comment_before.splitlines() -%}
; {{line | mdescape}}  
{% endfor -%}
{%- endif -%}
{%- endmacro -%}

{%- macro comment_after(i) -%}
{%- if i.comment_after -%}
{%- for line in i.comment_after.splitlines() -%}
; {{line | mdescape}}  
{% endfor -%}
{%- endif -%}
{%- endmacro -%}

{%- macro comment_inline(i) -%}
{%- if i.comment -%}
; {{i.comment | mdescape}}  
{%- endif -%}
{%- endmacro -%}

{%- macro label(i) -%}
{%- if i.label -%}
**{{i.label | mdescape}}**  
{% endif -%}
{%- endmacro -%}

{%- macro anchor(i) -%}
{%- if i.is_destination -%}
<a name="{{"{:04x}".format(i.address)}}"></a>
{%- endif -%}
{%- endmacro -%}

{%- macro address(i) -%}
**{{"{:04x}".format(i.address)}}**
{%- endmacro -%}

{%- macro tabs() %}   {% endmacro -%}

{%-macro operand(i)-%}
{%-if i.instruction.is_source-%}
[
{%-endif-%}
{{-i.instruction.operand | mdescape-}}
{%-if i.instruction.is_source-%}
](#{{"{:04x}".format(i.instruction.target)}})
{{-i.instruction.op_adjust-}}
{%-endif-%}
{%- endmacro -%}

{%- macro instruction(i) -%}
{{i.instruction.mnemonic}} {{i.instruction.pre}}{{operand(i)}}{{i.instruction.post}}
{%- endmacro -%}

{#- ----------------section handlers---------------- -#}

{#- ----------------prefix---------------- -#}
{%- macro prefix_handler(section) -%}
{{- anchor(section) -}}
{{- comment_before(section) -}}
{{- label(section) -}}
{{- comment_after(section) -}}
{%- if section.authoring_info -%}
{{section.authoring_info.type}} section @
{{-address_range(section.authoring_info)-}} 
{%- endif -%}
{%- endmacro -%}

{%- macro code_handler(section) -%}
{%- for i in section.lines -%}
{{anchor(i)}}{{address(i)}}{{tabs()}}{{i.bytes|seq2str("{:02x}",w=8)}}{{tabs()}}{{instruction(i)-}}
{{-comment_inline(i)}}  
{% endfor -%}
{%- endmacro -%}

{#- ----------------data---------------- -#}
{%- macro data_handler(section) -%}
{%- for i in section.lines -%}
{{anchor(i)}}{{address(i)}}{{tabs()}}{{i.bytes|seq2str("{:02x}", s=[(1," "), (4, "  ")])}}  
{% endfor -%}
{%- endmacro -%}

{#- ----------------ptr16---------------- -#}
{%- macro ptr16_handler(section) %}
{% for i in section.lines -%}
{{address(i)}}    |
{%- for v in i.vals -%}
{%- if v.is_source -%}[{%- endif -%}
{{- v.val -}}
{%- if v.is_source -%}](#{{"{:04x}".format(v.target)}}){%- endif -%}
|
{%- endfor %}  
{% endfor %}
{% endmacro -%}

{#- ----------------basic---------------- -#}
{%- macro basic_handler(section) -%}
{%- for ln in section.lines -%}
{{- anchor(ln) -}}
{%- for tkn in ln.tokens -%}
{{- tkn.type|cbmbasic_dispatch(tkn) -}}
{%- endfor %}  
{% endfor -%}
{%- endmacro -%}

{%- macro cbmbasic_line_num_handler(tkn) -%}
{{ tkn.val }} {% endmacro -%}

{%- macro cbmbasic_text_handler(tkn) -%}
{{ tkn.val }}
{%- endmacro -%}

{%- macro cbmbasic_command_handler(tkn) -%}
{{ tkn.val }}
{%- endmacro -%}

{%- macro cbmbasic_quoted_handler(tkn) -%}
{{ tkn.val }}
{%- endmacro -%}

{%- macro cbmbasic_line_ref_handler(tkn) -%}
{%- if tkn.is_source %}[{% endif -%}
{{- tkn.val -}}
{%- if tkn.is_source -%}
](#{{"{:04x}".format(tkn.target)}})
{%- endif -%}
{%- endmacro -%}

{%- macro cbmbasic_address_handler(tkn) -%}
{%- if tkn.is_source %}[{% endif -%}
{{- tkn.val -}}
{%- if tkn.is_source -%}
](#{{"{:04x}".format(tkn.target)}})
{%- endif -%}
{%- endmacro -%}

{#- ----------------chars---------------- -#}
{%- macro chars_handler(section) -%}
**{{"{:04x}".format(section.address)}}**  
![]({{section.generate()}})
{% endmacro -%}

{#- ----------------sections---------------- -#}
{%- for section in items -%}
{{ section.type|dispatch(section) }}
{%- endfor -%}
