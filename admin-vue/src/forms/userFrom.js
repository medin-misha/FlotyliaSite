import StringComp from '@/components/subComponents/fieldsComps/stringComp.vue'
import NumberComp from '@/components/subComponents/fieldsComps/numberComp.vue'
import DocumentListComp from '@/components/subComponents/fieldsComps/documentListComp.vue'
import SelectComp from '@/components/subComponents/fieldsComps/selectComp.vue'
import DateComp from '@/components/subComponents/fieldsComps/dateComp.vue'
import CheckboxComp from '@/components/subComponents/fieldsComps/checkboxComp.vue'
import stringCreateComp from '@/components/subComponents/createComps/stringCreateComp.vue'
import SelectCreateComp from '@/components/subComponents/createComps/selectCreateComp.vue'
import DateCreateComp from '@/components/subComponents/createComps/dateCreateComp.vue'

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
    },
    {
      key: 'created_at',
      label: 'Отметка времени',
      type: 'date',
      readonly: true,
      component: DateComp,
    },
    {
      key: 'name',
      label: 'Имя фамилия',
      type: 'string',
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
      component: StringComp,
    },
    {
      key: 'email',
      label: 'Электронная почта',
      type: 'string',
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
      label: 'Whatsapp',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'desired_transport',
      label: 'Тип транспорта',
      type: 'string',
      component: StringComp,
    },
    {
      key: 'invoice',
      label: 'Номер счета',
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
      label: 'Обработка данных',
      type: 'boolean',
      component: CheckboxComp,
    },
    {
      key: 'work_in',
      label: 'Работает в',
      type: 'string',
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
    {
      key: 'documents',
      label: 'Documents',
      type: 'object',
      component: DocumentListComp,
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
      component: stringCreateComp,
    },
    {
      key: 'city',
      label: 'Город',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'phone',
      label: 'Номер телефона',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'email',
      label: 'Электронная почта',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'birth_date',
      label: 'Дата рождения',
      type: 'date',
      component: DateCreateComp,
    },
    {
      key: 'address',
      label: 'Адрес проживания',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'telegram',
      label: 'Telegram',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'whatsapp',
      label: 'WhatsApp',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'desired_transport',
      label: 'Тип транспорта для доставки',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'invoice',
      label: 'Укажите номер счета чешского банка либо укажите другой тип оплаты',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'citizenship',
      label: 'Гражданство',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'consent',
      label: 'Согласие на обработку персональных данных',
      type: 'boolean',
      component: stringCreateComp,
    },
    {
      key: 'work_in',
      label: 'Работает в',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'how_found_it',
      label: 'Как нас нашел',
      type: 'string',
      component: stringCreateComp,
    },
    {
      key: 'status',
      label: 'Статус',
      type: 'string',
      readonly: false,
      component: SelectCreateComp,
      options: userStatusOptions,
    },
  ],
}
