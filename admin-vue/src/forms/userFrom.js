import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import DocumentListComp from '@/components/subComponents/fieldsComps/documentListComp.vue'
import SelectComp from '@/components/subComponents/fieldsComps/selectComp.vue'
import DateComp from '@/components/subComponents/fieldsComps/dateComp.vue'
import CheckboxComp from '@/components/subComponents/fieldsComps/checkboxComp.vue'

const userStatusOptions = [
  { value: 'pending', label: 'Pending' },
  { value: 'active', label: 'Active' },
  { value: 'inoperative', label: 'Inoperative' },
  { value: 'processing', label: 'Processing' },
  { value: 'in activation', label: 'In Activation' },
]

export const userSchema = {
  endpoint: '/users',
  filters: [
    {
      key: 'status',
    },
  ],
  fields: [
    {
      key: 'id',
      label: 'ID',
      type: 'number',
      readonly: true,
      component: NumberComp,
      group: 'personal',
    },
    {
      key: 'created_at',
      label: 'Отметка времени',
      type: 'date',
      readonly: true,
      component: DateComp,
      group: 'personal',
    },
    {
      key: 'name',
      label: 'Имя фамилия',
      type: 'string',
      copyable: true,
      component: StringComp,
      group: 'personal',
    },
    {
      key: 'city',
      label: 'Город',
      type: 'string',
      copyable: true,
      component: StringComp,
      group: 'logistics',
    },
    {
      key: 'phone',
      label: 'Номер телефона',
      type: 'string',
      copyable: true,
      component: StringComp,
      group: 'contacts',
    },
    {
      key: 'email',
      label: 'Электронная почта',
      type: 'string',
      copyable: true,
      component: StringComp,
      group: 'contacts',
    },
    {
      key: 'birth_date',
      label: 'Дата рождения',
      type: 'date',
      copyable: true,
      component: DateComp,
      group: 'personal',
    },
    {
      key: 'address',
      label: 'Адрес проживания',
      type: 'string',
      copyable: true,
      component: StringComp,
      group: 'logistics',
    },
    {
      key: 'telegram',
      label: 'Telegram',
      type: 'string',
      component: StringComp,
      group: 'contacts',
    },
    {
      key: 'whatsapp',
      label: 'Whatsapp',
      type: 'string',
      component: StringComp,
      group: 'contacts',
    },
    {
      key: 'desired_transport',
      label: 'Тип транспорта',
      type: 'string',
      component: StringComp,
      group: 'logistics',
    },
    {
      key: 'invoice',
      label: 'Номер счета',
      type: 'string',
      component: StringComp,
      group: 'logistics',
    },
    {
      key: 'citizenship',
      label: 'Гражданство',
      type: 'string',
      component: StringComp,
      group: 'personal',
    },
    {
      key: 'consent',
      label: 'Обработка данных',
      type: 'boolean',
      component: CheckboxComp,
      group: 'personal',
    },
    {
      key: 'work_in',
      label: 'Работает в',
      type: 'string',
      component: StringComp,
      group: 'logistics',
    },
    {
      key: 'how_found_it',
      label: 'Как нас нашел',
      type: 'string',
      component: StringComp,
      group: 'logistics',
    },
    {
      key: 'status',
      label: 'Статус',
      type: 'string',
      readonly: false,
      component: SelectComp,
      options: userStatusOptions,
      group: 'logistics',
    },
    {
      key: 'documents',
      label: 'Documents',
      type: 'object',
      component: DocumentListComp,
      group: 'documents',
    },
  ],
}

export const userCreateSchema = {
  endpoint: '/users',
  fields: [
    {
      key: 'name',
      label: 'Имя фамилия',
      type: 'string',
      required: true,
      component: StringComp,
    },
    {
      key: 'city',
      label: 'Город',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'phone',
      label: 'Номер телефона',
      type: 'string',
      required: true,
      component: StringComp,
    },
    {
      key: 'email',
      label: 'Электронная почта',
      type: 'string',
      required: true,
      component: StringComp,
    },
    {
      key: 'birth_date',
      label: 'Дата рождения',
      type: 'date',
      component: DateComp,
    },
    {
      key: 'address',
      label: 'Адрес проживания',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'telegram',
      label: 'Telegram',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'whatsapp',
      label: 'WhatsApp',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'desired_transport',
      label: 'Тип транспорта для доставки',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'invoice',
      label: 'Укажите номер счета чешского банка либо укажите другой тип оплаты',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'citizenship',
      label: 'Гражданство',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'consent',
      label: 'Согласие на обработку персональных данных',
      type: 'boolean',
      required: true,
      component: CheckboxComp,
    },
    {
      key: 'work_in',
      label: 'Работает в',
      type: 'string',
      required: true,
      component: StringComp,
    },
    {
      key: 'how_found_it',
      label: 'Как нас нашел',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'status',
      label: 'Статус',
      type: 'string',
      readonly: false,
      component: SelectComp,
      options: userStatusOptions,
    },
  ],
}
